import multiprocessing
import pathlib
import logging.config
import sys
from pydantic import BaseModel
from config import app_config
import platform

path = pathlib.Path(__file__).parent.resolve()
default_manager_handler_filename = path/'default_log.log'


def set_manager_handler(default_manager_handler: dict) -> dict:
    global default_manager_handler_filename
    if platform.system() == 'Windows':
        default_manager_handler['class'] = 'logging.handlers.NTEventLogHandler'
        default_manager_handler['appname'] = 'NefrytLDS_Trends_Writer'
        default_manager_handler_filename = path/default_manager_handler.pop('filename', 'default_log.log')
    elif platform.system() in ['Darwin', 'Linux']:
        default_manager_handler['class'] = 'logging.handlers.SysLogHandler'
        default_manager_handler['address'] = '/dev/log' if platform.system() == 'Linux' else '/var/run/syslog'
        default_manager_handler_filename = path/default_manager_handler.pop('filename', 'default_log.log')
    return default_manager_handler


def reset_manager_handler(manager_handler: dict) -> dict:
    if 'pytest' in sys.modules:
        return {
            'class': 'logging.NullHandler'
        }
    else:
        return {
            'class': 'logging.FileHandler',
            'filename': default_manager_handler_filename,
            'level': manager_handler['level']
        }


class AppConfig(BaseModel):
    db_uri: str
    modbus_port: int = 502
    log_profiler: bool = False
    use_past_trend_data: bool = True
    profiler_filename: str = 'profiler.log'


_logging_config = app_config['trends_writer']['logging']
_logging_config['handlers']['manager'] = set_manager_handler(_logging_config['handlers']['manager'])
for logger_name, logger_config in _logging_config['loggers'].items():
    level = logger_config.get('level', 'NOTSET')
    if level == 'DEBUG':
        logger_config['handlers'] = ['console']
try:
    logging.config.dictConfig(_logging_config)
except Exception as e:
    if multiprocessing.current_process().name == 'MainProcess':
        logging.warning(f'Config: Cannot configurate logger with given parameters: {e}', exc_info=True)
    _logging_config['handlers']['manager'] = reset_manager_handler(_logging_config['handlers']['manager'])
    logging.config.dictConfig(_logging_config)

app_config['trends_writer'].update(app_config)
TrendsWriterSettings = AppConfig(**app_config['trends_writer'])
