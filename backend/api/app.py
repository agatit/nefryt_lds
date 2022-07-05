import connexion
from flask_cors import CORS

from .config import config
from .encoder import JSONEncoder






app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'Nefryt LDS API'},
            pythonic_params=True)

app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"future": True, "echo": False}

CORS(app.app)