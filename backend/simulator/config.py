from pydantic import BaseModel
from config import app_config


class AppConfig(BaseModel):
    displayer_port: int | None = None

SimulatorSettings = AppConfig(**app_config['simulator'])
