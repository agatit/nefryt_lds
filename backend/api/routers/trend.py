import struct
from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Query, Body, Path, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, and_, Engine, literal, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from .mapper import map_lds_trend_param_and_lds_trend_param_def_to_trend_param, map_dicts_to_trend_data_multiple, \
    map_tuple_to_trend_data_single
from .security import get_user_token
from .utils import strip_strings
from ..custom_page import CustomParams, CustomPage, use_custom_page
from ..db import get_engine
from ..schemas import Error, TrendDataMultiple, Information, UpdateTrend, TrendParamOut, TrendDataSingle, TrendBase
from database import lds

router = APIRouter(prefix="/trend", tags=['trend'], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.Trend] | Error)
async def list_trends(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                      _: Annotated[None, Depends(use_custom_page)], filter: Annotated[str | None, Query()] = None):
    try:
        statement = select(lds.Trend).order_by(lds.Trend.ID)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [strip_strings(lds_trend) for lds_trend in page.items]
        return page
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_trends(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Trend | Error)
async def create_trend(trend: Annotated[TrendBase, Body()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        trend = lds.Trend(**trend.model_dump())
        with Session(engine) as session:
            session.add(trend)
            session.commit()
            session.refresh(trend)
        content = strip_strings(trend).model_dump(by_alias=True)
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating trend')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_trend(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id_list}/current_data/{period}/{samples}', response_model=CustomPage[TrendDataMultiple] | Error)
async def get_trend_current_data(trend_id_list: Annotated[str, Path()], period: Annotated[int, Path()],
                                 samples: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)],
                                 params: Annotated[CustomParams, Depends()],
                                 _: Annotated[None, Depends(use_custom_page)]):
    timestamp = int(datetime.now(timezone.utc).timestamp())
    return await get_trend_data(trend_id_list, timestamp - period, timestamp, samples, engine, params, _)


@router.get('/{trend_id_list}/data/{begin}/{end}/{samples}', response_model=CustomPage[TrendDataMultiple] | Error)
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
            where(lds.TrendData.Time.in_(trend_timestamps)). # noqa
            where(lds.TrendData.TrendID.in_(trend_id_list)) # noqa
        )
        with Session(engine) as session:
            all_data_count = session.execute(statement).scalar()

        if all_data_count == 0:
            error = Error(code=status.HTTP_404_NOT_FOUND,
                          message='No data')
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        start_pos, pages = calculate_page_data(samples, params)
        trend_timestamps, trend_timestamps_ms = calculate_page_timestamps_lists(start_pos, trend_timestamps,
                                                                                trend_timestamps_ms, params.size)

        statement = (select(lds.TrendData).
                     where(lds.TrendData.Time.in_(trend_timestamps)). # noqa
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
                                                         * (one_second_data[trend_id][
                                                                -time_data[1] // 10 - 1]
                                                            - lds_trends_scales[trend_id]["RawMin"])
                                                         / (lds_trends_scales[trend_id]["RawMax"]
                                                            - lds_trends_scales[trend_id]["RawMin"])
                                                         + lds_trends_scales[trend_id]["ScaledMin"]),
                                                        time_data[0], time_data[1]))
                time_data = next(iter_time_data, None)
        result_lists = extend_trend_data_dicts(result_lists, trend_timestamps, trend_timestamps_ms)
        items = map_dicts_to_trend_data_multiple(zip(trend_timestamps, trend_timestamps_ms), result_lists)
        return CustomPage(items=items, total=samples, pages=pages, page=params.page, size=params.size)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_trend_data(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}/single_data/{begin}/{end}/{samples}', response_model=CustomPage[TrendDataSingle] | Error)
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
            where(lds.TrendData.Time.in_(trend_timestamps)). # noqa
            where(lds.TrendData.TrendID == literal(trend_id)) # noqa
        )
        with Session(engine) as session:
            all_data_count = session.execute(statement).scalar()

        if all_data_count == 0:
            error = Error(code=status.HTTP_404_NOT_FOUND,
                          message='No data')
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        start_pos, pages = calculate_page_data(samples, params)
        trend_timestamps, trend_timestamps_ms = calculate_page_timestamps_lists(start_pos, trend_timestamps,
                                                                                trend_timestamps_ms, params.size)
        statement = (select(lds.TrendData).
                     where(lds.TrendData.Time.in_(trend_timestamps)). # noqa
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
                                         * (one_second_data[-time_data[1] // 10 - 1] - lds_trend_scales["RawMin"])
                                         / (lds_trend_scales["RawMax"] - lds_trend_scales["RawMin"])
                                         + lds_trend_scales["ScaledMin"]),
                                        time_data[0], time_data[1]))
                time_data = next(iter_time_data, None)
        items = [map_tuple_to_trend_data_single(val) for val in result_list]
        return CustomPage(items=items, total=samples, pages=pages, page=params.page, size=params.size)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_single_trend_data(): ' + str(e))  # noqa
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{trend_id}', response_model=Information | Error)
async def delete_trend_by_id(trend_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            trend = session.get(lds.Trend, trend_id)
            if not trend:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend with id = ' + str(trend_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(trend)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_trend_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}', response_model=lds.Trend | Error)
async def get_trend_by_id(trend_id: int, engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_trend = session.get(lds.Trend, trend_id)
        if not lds_trend:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No trend with id = ' + str(trend_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return strip_strings(lds_trend)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_trend_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{trend_id}', response_model=lds.Trend | Error)
async def update_trend(trend_id: Annotated[int, Path()], updated_trend: Annotated[UpdateTrend, Body()],
                       engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            trend = session.get(lds.Trend, trend_id)
            if not trend:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend with id = ' + str(trend_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_trend_dict = updated_trend.model_dump(by_alias=True, exclude_unset=True)
            trend_params_ids = ['RawMin', 'RawMax', 'ScaledMax', 'ScaledMin']
            for k, v in updated_trend_dict.items():
                setattr(trend, k, v)
                if k in trend_params_ids:
                    trend_param_id = [char.upper() if char.islower() else '_' + char.upper() for char in k]
                    trend_param_id = ''.join(trend_param_id).lstrip('_')
                    await update_trend_param(trend_id, trend_param_id, str(v), engine)
            session.commit()
            session.refresh(trend)
        return strip_strings(trend)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_trend(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}/param', response_model=CustomPage[TrendParamOut] | Error)
async def list_trend_params(trend_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)],
                            params: Annotated[CustomParams, Depends()], _: Annotated[None, Depends(use_custom_page)],
                            filter: Annotated[str | None, Query()] = None):
    try:
        statement = select(1).where(lds.Trend.ID == literal(trend_id)) # noqa
        with Session(engine) as session:
            trend_exists = session.execute(statement).first()
        if not trend_exists:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No trend with id = ' + str(trend_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        statement = ((((select(lds.TrendParam, lds.Trend, lds.TrendParamDef)
                        .select_from(lds.Trend))
                       .join(lds.TrendParamDef, lds.Trend.TrendDefID == lds.TrendParamDef.TrendDefID)) # noqa
                      .join(lds.TrendParam, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID,
                                                 lds.Trend.ID == lds.TrendParam.TrendID))) # noqa
                     .where(lds.Trend.ID == literal(trend_id)) # noqa
                     .order_by(lds.Trend.ID)) # noqa
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [
            map_lds_trend_param_and_lds_trend_param_def_to_trend_param(lds_trend_param, lds_trend_param_def)
            for lds_trend_param, _, lds_trend_param_def in page.items
        ]
        return page
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_trend_params(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}/param/{trend_param_def_id}', response_model=TrendParamOut | Error)
async def get_trend_param_by_id(trend_id: Annotated[int, Path()], trend_param_def_id: Annotated[str, Path()],
                                engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = ((((select(lds.TrendParam, lds.Trend, lds.TrendParamDef)
                        .select_from(lds.Trend))
                       .outerjoin(lds.TrendParamDef, lds.Trend.TrendDefID == lds.TrendParamDef.TrendDefID)) # noqa
                      .outerjoin(lds.TrendParam, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID,
                                                      lds.Trend.ID == lds.TrendParam.TrendID))) # noqa
                     .where(lds.Trend.ID == literal(trend_id)) # noqa
                     .where(lds.TrendParam.TrendParamDefID == literal(trend_param_def_id)))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = Error(code=status.HTTP_404_NOT_FOUND,
                          message='No trend param for trend with id = ' + str(trend_id)
                                  + ' and trendParamDef with id = ' + trend_param_def_id.strip())
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_trend_param, _, lds_trend_param_def = results[0]
        return map_lds_trend_param_and_lds_trend_param_def_to_trend_param(lds_trend_param, lds_trend_param_def)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_trend_param_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{trend_id}/param/{trend_param_def_id}', response_model=TrendParamOut | Error)
async def update_trend_param(trend_id: Annotated[int, Path()], trend_param_def_id: Annotated[str, Path()],
                             updated_trend_value: Annotated[str, Body()],
                             engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = (select(lds.TrendParam).
                     where(lds.TrendParam.TrendParamDefID == literal(trend_param_def_id)). # noqa
                     where(lds.TrendParam.TrendID == literal(trend_id)))
        with Session(engine) as session:
            lds_trend_param = session.execute(statement).all()
            lds_trend = session.get(lds.Trend, trend_id)
            if not lds_trend_param or not lds_trend:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend param for trend with id = ' + str(trend_id)
                                      + ' and trendParamDef with id = ' + trend_param_def_id.strip())
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_trend_param = lds_trend_param[0][0]
            lds_trend_param.Value = updated_trend_value
            field_name = ''.join(word.capitalize() for word in trend_param_def_id.lower().split('_'))
            setattr(lds_trend, field_name, updated_trend_value)
            session.commit()
        return await get_trend_param_by_id(trend_id, trend_param_def_id, engine)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in update_trend_param(): ' + str(e))
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
