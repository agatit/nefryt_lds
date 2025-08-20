import json
import struct
from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Path, Depends
from sqlalchemy import select, and_, Engine, literal, func, desc
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from api.routers.utils import map_dicts_to_trend_data_multiple, map_tuple_to_trend_data_single, get_user_token
from ..custom_page import CustomParams, CustomPage, use_custom_page
from db import get_engine
from ..schemas import api
from database import lds

router = APIRouter(prefix="/trend", tags=['trend_data'], dependencies=[Depends(get_user_token)])


@router.get('/{trend_id_list}/current_data/{period}/{samples}', response_model=CustomPage[api.CurrentTrendData] | api.Error)
async def get_trend_current_data(trend_id_list: Annotated[str, Path()], period: Annotated[int, Path()],
                                 samples: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)],
                                 params: Annotated[CustomParams, Depends()],
                                 _: Annotated[None, Depends(use_custom_page)]):
    timestamp = int(datetime.now(timezone.utc).timestamp())
    timestamp_delta = 0
    split_trend_id_list = trend_id_list.split(",")

    statement = (select(lds.Trend)
                 .where(and_(lds.Trend.ID.in_(split_trend_id_list), lds.Trend.TimeDelta > 0)) # noqa
                 .order_by(desc(lds.Trend.TimeDelta))) # noqa
    with Session(engine) as session:
        trends = session.execute(statement).fetchall()

        for trend in trends:
            trend = trend[0]
            statement = (select(lds.TrendData)
                         .where(and_(lds.TrendData.TrendID == literal(trend.ID),
                                     lds.TrendData.Time >= timestamp - trend.TimeDelta - 1)))
            trends_data = session.execute(statement).fetchall()
            if len(trends_data) > 0:
                timestamp_delta = trend.TimeDelta
                break

    response = await get_trend_data(trend_id_list, timestamp - period - timestamp_delta,
                                        timestamp - timestamp_delta, samples, engine, params, _)
    if response.status_code != status.HTTP_200_OK:
        return response
    else:
        response = CustomPage(**json.loads(response.body.decode()))
        return CustomPage(items=[api.CurrentTrendData(LastTimestamp=timestamp - timestamp_delta, Data=response.items)],
                   total=response.total, pages=response.pages, page=response.page, size=response.size)


@router.get('/{trend_id_list}/data/{begin}/{end}/{samples}', response_model=CustomPage[api.TrendDataMultiple] | api.Error)
async def get_trend_data(trend_id_list: Annotated[str, Path()], begin: Annotated[int, Path()],
                         end: Annotated[int, Path()], samples: Annotated[int, Path()],
                         engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                         _: Annotated[None, Depends(use_custom_page)]):
    try:
        lds_trends_scales = {}
        trend_id_list = trend_id_list.split(",")
        statement = select(lds.Trend).where(lds.Trend.ID.in_(trend_id_list)) # noqa
        with Session(engine) as session:
            lds_trends = session.execute(statement).all()

        params_ids = ['RawMin', 'RawMax', 'ScaledMin', 'ScaledMax']
        default_lds_trends_scale = {params_ids[0]: 0,
                                    params_ids[1]: 1,
                                    params_ids[2]: 0,
                                    params_ids[3]: 1}

        for lds_trend, in lds_trends:
            try:
                lds_trends_scales[lds_trend.ID] = {
                    param_id: getattr(lds_trend, param_id) for param_id in params_ids
                }
            except (AttributeError, TypeError):
                lds_trends_scales[lds_trend.ID] = default_lds_trends_scale

        samples, inc_samples = calculate_samples_count(samples, begin, end)
        trend_timestamps, trend_timestamps_ms = calculate_full_timestamps_lists(samples, begin, inc_samples)

        statement = (
            select(func.count()).
            select_from(lds.TrendData).
            where(lds.TrendData.Time.in_(list(set(trend_timestamps)))). # noqa
            where(lds.TrendData.TrendID.in_(trend_id_list)) # noqa
        )
        with Session(engine) as session:
            all_data_count = session.execute(statement).scalar()

        if all_data_count == 0:
            error = api.Error(code=status.HTTP_404_NOT_FOUND,
                          message='No data')
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        start_pos, pages = calculate_page_data(samples, params)
        trend_timestamps, trend_timestamps_ms = calculate_page_timestamps_lists(start_pos, trend_timestamps,
                                                                                trend_timestamps_ms, params.size)

        statement = (select(lds.TrendData).
                     where(lds.TrendData.Time.in_(list(set(trend_timestamps)))). # noqa
                     where(lds.TrendData.TrendID.in_(trend_id_list)). # noqa
                     order_by(lds.TrendData.Time)) # noqa
        with Session(engine) as session:
            lds_trends_data = session.execute(statement).all()

        if len(lds_trends_data) == 0 and len(trend_timestamps) == 0:
            return CustomPage(items=[], total=samples, pages=pages, page=params.page, size=params.size)

        lds_trends_data, iter_lds_data, iter_time_data, lds_data, time_data = (
            prepare_iterators_for_trend_data_getter(lds_trends_data, trend_timestamps, trend_timestamps_ms))
        result_lists = {str(lds_trend[0].ID): [] for lds_trend in lds_trends}

        while lds_data and time_data:
            while lds_data.Time < time_data[0]:
                lds_data = next(iter_lds_data)

            one_second_data = {}
            while lds_data and lds_data.Time == time_data[0]:
                if lds_trends_scales[lds_data.TrendID]["RawMin"] >= 0:
                    one_second_data[lds_data.TrendID] = struct.unpack("H" * 100, lds_data.Data)
                else:
                    one_second_data[lds_data.TrendID] = struct.unpack("h" * 100, lds_data.Data)
                lds_data = next(iter_lds_data, None)

            current_second = time_data[0]
            while time_data and time_data[0] == current_second:
                for trend_id in one_second_data.keys():
                    result_lists[str(trend_id)].append((((lds_trends_scales[trend_id]["ScaledMax"]
                                                          - lds_trends_scales[trend_id]["ScaledMin"])
                                                         * (one_second_data[trend_id][time_data[1] // 10]
                                                            - lds_trends_scales[trend_id]["RawMin"])
                                                         / (lds_trends_scales[trend_id]["RawMax"]
                                                            - lds_trends_scales[trend_id]["RawMin"])
                                                         + lds_trends_scales[trend_id]["ScaledMin"]),
                                                        time_data[0], time_data[1]))
                time_data = next(iter_time_data, None)
        result_lists = extend_trend_data_dicts(result_lists, trend_timestamps, trend_timestamps_ms)
        items = map_dicts_to_trend_data_multiple(zip(trend_timestamps, trend_timestamps_ms), result_lists)
        return JSONResponse(content=CustomPage(items=items, total=samples, pages=pages, page=params.page, size=params.size).model_dump(),
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_trend_data(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}/single_data/{begin}/{end}/{samples}', response_model=CustomPage[api.TrendDataSingle] | api.Error)
async def get_single_trend_data(trend_id: Annotated[str, Path()], begin: Annotated[int, Path()],
                                end: Annotated[int, Path()], samples: Annotated[int, Path()],
                                engine: Annotated[Engine, Depends(get_engine)],
                                _: Annotated[None, Depends(use_custom_page)],
                                params: Annotated[CustomParams, Depends()]):
    try:
        with Session(engine) as session:
            lds_trend = session.get(lds.Trend, trend_id)

        params_ids = ['RawMin', 'RawMax', 'ScaledMin', 'ScaledMax']
        default_lds_trends_scale = {params_ids[0]: 0,
                                    params_ids[1]: 1,
                                    params_ids[2]: 0,
                                    params_ids[3]: 1}

        try:
            lds_trend_scales = {
                param_id: getattr(lds_trend, param_id) for param_id in params_ids
            }
        except (AttributeError, TypeError):
            lds_trend_scales = default_lds_trends_scale

        samples, inc_samples = calculate_samples_count(samples, begin, end)
        trend_timestamps, trend_timestamps_ms = calculate_full_timestamps_lists(samples, begin, inc_samples)

        statement = (
            select(func.count()).
            select_from(lds.TrendData).
            where(lds.TrendData.Time.in_(list(set(trend_timestamps)))). # noqa
            where(lds.TrendData.TrendID == literal(trend_id)) # noqa
        )
        with Session(engine) as session:
            all_data_count = session.execute(statement).scalar()

        if all_data_count == 0:
            error = api.Error(code=status.HTTP_404_NOT_FOUND,
                          message='No data')
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        start_pos, pages = calculate_page_data(samples, params)
        trend_timestamps, trend_timestamps_ms = calculate_page_timestamps_lists(start_pos, trend_timestamps,
                                                                                trend_timestamps_ms, params.size)
        statement = (select(lds.TrendData).
                     where(lds.TrendData.Time.in_(list(set(trend_timestamps)))). # noqa
                     where(lds.TrendData.TrendID == literal(trend_id)). # noqa
                     order_by(lds.TrendData.Time)) # noqa
        with Session(engine) as session:
            lds_trends_data = session.execute(statement).all()

        if len(lds_trends_data) == 0:
            return CustomPage(items=[], total=samples, pages=pages, page=params.page, size=params.size)

        lds_trends_data, iter_lds_data, iter_time_data, lds_data, time_data = (
            prepare_iterators_for_trend_data_getter(lds_trends_data, trend_timestamps, trend_timestamps_ms))
        result_list = []

        while lds_data and time_data:
            while lds_data.Time < time_data[0]:
                lds_data = next(iter_lds_data)

            one_second_data = []
            while lds_data and lds_data.Time == time_data[0]:
                if lds_trend_scales["RawMin"] >= 0:
                    one_second_data = struct.unpack("H" * 100, lds_data.Data)
                else:
                    one_second_data = struct.unpack("h" * 100, lds_data.Data)
                lds_data = next(iter_lds_data, None)

            current_second = time_data[0]
            while time_data and time_data[0] == current_second:
                if len(one_second_data) != 0:
                    result_list.append((((lds_trend_scales["ScaledMax"] - lds_trend_scales["ScaledMin"])
                                         * (one_second_data[time_data[1] // 10] - lds_trend_scales["RawMin"])
                                         / (lds_trend_scales["RawMax"] - lds_trend_scales["RawMin"])
                                         + lds_trend_scales["ScaledMin"]),
                                        time_data[0], time_data[1]))
                time_data = next(iter_time_data, None)
        items = [map_tuple_to_trend_data_single(val) for val in result_list]
        return CustomPage(items=items, total=samples, pages=pages, page=params.page, size=params.size)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_single_trend_data(): ' + str(e))  # noqa
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def extend_trend_data_dicts(result_lists, trend_timestamps, trend_timestamps_ms):
    for trend_id in result_lists:
        result = result_lists[trend_id]
        timestamps_list = [(res[1], res[2]) for res in result]
        for counter, (trend_timestamp, trend_timestamp_ms) in enumerate(zip(trend_timestamps, trend_timestamps_ms)):
            if (trend_timestamp, trend_timestamp_ms) not in timestamps_list:
                result.insert(counter, (None, trend_timestamp, trend_timestamp_ms))

    return result_lists


def extend_trend_data_list(result_list, trend_timestamps, trend_timestamps_ms):
    timestamps_list = [(res[1], res[2]) for res in result_list]
    for counter, (trend_timestamp, trend_timestamp_ms) in enumerate(zip(trend_timestamps, trend_timestamps_ms)):
        if (trend_timestamp, trend_timestamp_ms) not in timestamps_list:
            result_list.insert(counter, (None, trend_timestamp, trend_timestamp_ms))

    return result_list


def calculate_samples_count(samples: int, begin: int, end: int) -> (int, int):
    samples = samples if samples > 0 else 1
    inc_samples = (100 * (end - begin + 1)) // samples
    inc_samples = inc_samples if inc_samples > 0 else 1
    samples = 100 * (end - begin + 1) // inc_samples
    return samples, inc_samples


def calculate_page_data(samples: int, params: CustomParams) -> (int, int):
    page_no = params.page
    page_size = params.size
    start_pos = (page_no - 1) * page_size
    pages = samples // page_size + 1 if samples % page_size != 0 else samples // page_size

    return start_pos, pages


def calculate_full_timestamps_lists(samples: int, begin: int, inc_samples: int) -> (list, list):
    trend_timestamps = []
    trend_timestamps_ms = []
    timestamp = begin
    sample_in_timestamp = 0
    for _ in range(samples):
        trend_timestamps.append(timestamp)
        trend_timestamps_ms.append(sample_in_timestamp * 10)
        timestamp += (sample_in_timestamp + inc_samples) // 100
        sample_in_timestamp = (sample_in_timestamp + inc_samples) % 100

    return trend_timestamps, trend_timestamps_ms


def calculate_page_timestamps_lists(start_pos: int, trend_timestamps: list, trend_timestamps_ms: list, page_size: int) \
        -> (list, list):
    if start_pos >= len(trend_timestamps):
        trend_timestamps = []
        trend_timestamps_ms = []
    else:
        end_pos = start_pos + page_size if start_pos + page_size < len(trend_timestamps) else None
        trend_timestamps = trend_timestamps[start_pos:end_pos] if end_pos else trend_timestamps[start_pos:]
        trend_timestamps_ms = trend_timestamps_ms[start_pos:end_pos] if end_pos else trend_timestamps_ms[start_pos:]

    return trend_timestamps, trend_timestamps_ms


def prepare_iterators_for_trend_data_getter(lds_trends_data, trend_timestamps: list, trend_timestamps_ms: list):
    lds_trends_data = [trend_data[0] for trend_data in lds_trends_data]

    iter_lds_data = iter(lds_trends_data)
    iter_time_data = zip(trend_timestamps, trend_timestamps_ms)

    lds_data = next(iter_lds_data, None)
    time_data = next(iter_time_data, None)

    return lds_trends_data, iter_lds_data, iter_time_data, lds_data, time_data
