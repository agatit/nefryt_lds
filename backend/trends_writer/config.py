import sys
import yaml
import pathlib
import os
import logging

cofnig = {}

path = pathlib.Path(__file__).parent.resolve()
with open(os.path.join(path, "config.yaml")) as f:
    config = yaml.load(f, Loader=yaml.Loader)
if config is None:
    config = {}

logging.basicConfig(stream=sys.stdout, level=config.get("verbosity","INFO"), force=True)