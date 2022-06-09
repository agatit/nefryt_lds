#!/usr/bin/env python3

import connexion
from flask_cors import CORS

from api import encoder
from database import db


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Nefryt LDS API'},
                pythonic_params=True)

    # app.app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:Onyks$us@serverdb:1447/NefrytLDSDemo'
    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?driver=ODBC+Driver+17+for+SQL+Server'
    
    app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"future": True}

    db.init_app(app.app)
    CORS(app.app)

    app.run(port=8080)


if __name__ == '__main__':
    main()
