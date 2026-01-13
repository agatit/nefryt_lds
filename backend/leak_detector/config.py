import multiprocessing
import pathlib
import logging.config
import sys
from pydantic import BaseModel
from config import app_config, Settings
import platform

path = pathlib.Path(__file__).parent.resolve()
default_manager_handler_filename = path/'default_log.log'


def set_manager_handler(default_manager_handler: dict) -> dict:
    global default_manager_handler_filename
    if platform.system() == 'Windows':
        default_manager_handler['class'] = 'logging.handlers.NTEventLogHandler'
        default_manager_handler['appname'] = 'NefrytLDS_Leak_Detector'
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


def setup_leak_detector_logging():
    for name in logging.root.manager.loggerDict:
        if name.startswith('leak_detector'):
            logger = logging.getLogger(name)
            logger.setLevel(Settings.verbosity)


class AppConfig(BaseModel):
    plot_heatmap: bool = False
    optimizer_method_id: int | None = None
    optimizer_pipeline_id: int | None = None


_logging_config = app_config['leak_detector']['logging']
_logging_config['handlers']['manager'] = set_manager_handler(_logging_config['handlers']['manager'])
for logger_name, logger_config in _logging_config['loggers'].items():
    level = logger_config.get('level', 'NOTSET')
    if level == 'DEBUG':
        logger_config['handlers'] = ['console']
try:
    logging.config.dictConfig(_logging_config)
except Exception as e:
    if multiprocessing.current_process().name == 'MainProcess':
        logging.warning(f'LeakDetector config: Cannot configurate logger with given parameters: {e}', exc_info=True)
    _logging_config['handlers']['manager'] = reset_manager_handler(_logging_config['handlers']['manager'])
    logging.config.dictConfig(_logging_config)

app_config['leak_detector'].update(app_config)
LeakDetectorSettings = AppConfig(**app_config['leak_detector'])
