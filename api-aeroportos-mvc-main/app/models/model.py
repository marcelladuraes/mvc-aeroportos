from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from marshmallow import fields
from flask_restful import Api, reqparse
from app.models.connection import user, password, database

app = Flask(__name__)
postgresql = False
if not postgresql:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@localhost/{database}'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/postgres'

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
CORS(app)
api = Api(app)

class AeroportoDataBase(db.Model):
    __tablename__ = "Dados"
    id_aeroporto = db.Column(db.Integer)
    nome_aeroporto = db.Column(db.String(256), unique=True, nullable=False)
    cidade = db.Column(db.String(256), nullable=False)
    pais = db.Column(db.CHAR(2), nullable=False)
    codigo_iata = db.Column(db.CHAR(3), unique=False, nullable=False, primary_key=True)
    latitude = db.Column(db.String(256), nullable=False)
    longitude = db.Column(db.String(256), nullable=False)
    altitude = db.Column(db.String(256), nullable=False)

    def __init__(self, id_aeroporto, nome_aeroporto, cidade, codigo_pais_iso, codigo_iata, latitude, longitude,
                 altitude):
        self.id_aeroporto = id_aeroporto
        self.nome_aeroporto = nome_aeroporto
        self.cidade = cidade
        self.codigo_pais_iso = codigo_pais_iso
        self.codigo_iata = codigo_iata
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.id_aeroporto, self.nome_aeroporto, self.cidade, self.codigo_pais_iso, self.codigo_iata, self.latitude, self.longitude, self.altitude}"


class AeroportoDataBaseSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = AeroportoDataBase
        sqla_session = db.session

    id_aeroporto = fields.Number()  # dump_only=True)
    nome_aeroporto = fields.String(required=True)
    cidade = fields.String(required=True)
    codigo_pais_iso = fields.String(required=True)
    codigo_iata = fields.String(required=True)
    latitude = fields.String(required=True)
    longitude = fields.String(required=True)
    altitude = fields.String(required=True)





parser = reqparse.RequestParser()
parser.add_argument('id_aeroporto', type=int, help='identificador do aeroporto')
parser.add_argument('nome_aeroporto', type=str, help='nome do aeroporto')
parser.add_argument('cidade', type=str, help='cidade do aeroporto')
parser.add_argument('codigo_pais_iso', type=str, help='país do aeroporto')
parser.add_argument('codigo_iata', type=str, help='código IATA do aeroporto')
parser.add_argument('latitude', type=str, help='latitude do aeroporto')
parser.add_argument('longitude', type=str, help='longitude do aeroporto')
parser.add_argument('altitude', type=str, help='altitude do aeroporto')


