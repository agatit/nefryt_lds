import os
import subprocess
import sys
from typing import Annotated
from fastapi import APIRouter, Depends, Body
from starlette import status
from starlette.responses import Response, JSONResponse
from api.routers.utils import get_user_token
from api.schemas import api
from pathlib import Path as PathlibPath


router = APIRouter(prefix="/leak_detector", tags=["leak_detector"], dependencies=[Depends(get_user_token)])


@router.post('/run_past_detector', response_model=None | api.Error)
async def run_past_detector(process_config: Annotated[api.PastDetectorConfig, Body()]):
    try:
        filepath=str(PathlibPath(__file__).resolve().parents[2]) + '/leak_detector/past_detector/past_detector.log'
        args = [sys.executable, "-m", "leak_detector.past_detector"]
        for key, value in process_config.model_dump(exclude_none=True).items():
            values = [v for v in ([str(value)] if type(value) == int else str(value)[1:-1].split(', '))]
            args.extend([f'--{key}'] + values)
        if os.name == "nt":
            subprocess.Popen(args, stdout=open(filepath, "a", encoding='utf-8'), stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            subprocess.Popen(args, stdout=open(filepath, "a", encoding='utf-8'), stderr=subprocess.STDOUT, start_new_session=True)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Failed to start past detector process: ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
