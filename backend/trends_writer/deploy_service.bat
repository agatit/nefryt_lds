@echo off
echo Installing dependencies...
uv venv --python 3.10.11 --clear
uv sync --extra service

echo Installing service...
uv run python trends_writer_service.py install

echo Setting up pywin32...
uv run python deploy_helper.py

echo Starting service...
uv run python trends_writer_service.py start

echo Done!
pause