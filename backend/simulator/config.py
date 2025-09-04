from pydantic import BaseModel
from config import app_config


class AppConfig(BaseModel):
    displayer_ports: dict | None = None

SimulatorSettings = AppConfig(**app_config['simulator'])
