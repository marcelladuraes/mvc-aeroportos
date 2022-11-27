'''
from flask import Flask
from flask_restful import reqparse, Api, Resource, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields


app = Flask(__name__)
postgresql = False
if not postgresql:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:enmvst1c@localhost/aeroporto'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/postgres'

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
CORS(app)

class AeroportoDataBase(db.Model):
    __tablename__ = "Dados"
    id_aeroporto = db.Column(db.Integer)
    nome_aeroporto = db.Column(db.String(256), unique = True, nullable = False)
    cidade = db.Column(db.String(256), nullable = False)
    pais = db.Column(db.CHAR(2), nullable = False)
    codigo_iata = db.Column(db.CHAR(3), unique = False, nullable = False, primary_key = True)
    latitude = db.Column(db.String(256), nullable = False)
    longitude = db.Column(db.String(256), nullable = False)
    altitude = db.Column(db.String(256), nullable = False)

    def __init__(self, id_aeroporto, nome_aeroporto, cidade, codigo_pais_iso, codigo_iata, latitude, longitude, altitude):
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

    id_aeroporto = fields.Number()#dump_only=True)
    nome_aeroporto = fields.String(required=True)
    cidade =  fields.String(required=True)
    codigo_pais_iso = fields.String(required=True)
    codigo_iata = fields.String(required=True)
    latitude = fields.String(required=True)
    longitude = fields.String(required=True)
    altitude = fields.String(required=True)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('id_aeroporto', type=int, help='identificador do aeroporto')
parser.add_argument('nome_aeroporto', type=str, help='nome do aeroporto')
parser.add_argument('cidade', type=str, help='cidade do aeroporto')
parser.add_argument('codigo_pais_iso', type=str, help='país do aeroporto')
parser.add_argument('codigo_iata', type=str, help='código IATA do aeroporto')
parser.add_argument('latitude', type=str, help='latitude do aeroporto')
parser.add_argument('longitude', type=str, help='longitude do aeroporto')
parser.add_argument('altitude', type=str, help='altitude do aeroporto')

class Aeroporto(Resource):
    def get(self, codigo_iata):
        aeroporto = AeroportoDataBase.query.get(codigo_iata)
        aeroporto_schema = AeroportoDataBaseSchema()
        resp = aeroporto_schema.dump(aeroporto)
        if aeroporto is None:
            return {"msg": "Nenhum Aeroporo encontrado"}, 404
        return {"aeroporto": [resp]}, 200

    def delete(self, codigo_iata):
        aeroporto = AeroportoDataBase.query.get(codigo_iata)
        db.session.delete(aeroporto)
        db.session.commit()
        return '', 204

    def put(self, codigo_iata):
        aeroporto_json = parser.parse_args()
        aeroporto = AeroportoDataBase.query.get(codigo_iata)
        if aeroporto is None:
            return {"msg": "Aeroporto inexistente para edição"}, 404

        if aeroporto_json.get('id_aeroporto'):
            aeroporto.id_aeroporto = aeroporto_json.id_aeroporto
        if aeroporto_json.get('nome_aeroporto'):
            aeroporto.nome_aeroporto = aeroporto_json.nome_aeroporto
        if aeroporto_json.get('cidade'):
            aeroporto.cidade = aeroporto_json.cidade
        if aeroporto_json.get('codigo_pais_iso'):
            aeroporto.codigo_pais_iso = aeroporto_json.codigo_pais_iso
        if aeroporto_json.get('latitude'):
            aeroporto.latitude = aeroporto_json.latitude
        if aeroporto_json.get('longitude'):
            aeroporto.longitude = aeroporto_json.longitude
        if aeroporto_json.get('altitude'):
            aeroporto.altitude = aeroporto_json.altitude

        db.session.add(aeroporto)
        db.session.commit()

        aeroporto_schema = AeroportoDataBaseSchema(only=['id_aeroporto', 'nome_aeroporto', 'cidade', 'codigo_pais_iso', 'codigo_iata', 'latitude' , 'longitude', 'altitude'])
        resp = aeroporto_schema.dump(aeroporto)
        return {"aeroporto": resp}, 200



class ListaAeroporto(Resource):
    def get(self):
        aeroportos = AeroportoDataBase.query.all()
        aeroporto_schema = AeroportoDataBaseSchema(many=True)
        resp = aeroporto_schema.dump(aeroportos)
        return {"aeroporto": resp}, 200

    def post(self):
        aeroporto_json = parser.parse_args()
        aeroporto_schema = AeroportoDataBaseSchema()
        aeroporto = aeroporto_schema.load(aeroporto_json)
        try:
            aeroportoDataBase = AeroportoDataBase(aeroporto['id_aeroporto'], aeroporto['nome_aeroporto'], aeroporto['cidade'], aeroporto['codigo_pais_iso'], aeroporto['codigo_iata'], aeroporto['latitude'], aeroporto['longitude'], aeroporto['altitude'])
            resp = aeroporto_schema.dump(aeroportoDataBase.create())
            return {"estacao": resp}, 201
        except Exception as e:
            return {"msg": e.args[0]}, 400


api.add_resource(Aeroporto, '/api/v1/aeroportos/<string:codigo_iata>')
api.add_resource(ListaAeroporto, '/api/v1/aeroportos')
'''


from app.controller.controler import app, api, Aeroporto, ListaAeroporto, db
if __name__ == '__main__':
  api.add_resource(Aeroporto, '/api/v1/aeroportos/<string:codigo_iata>')
  api.add_resource(ListaAeroporto, '/api/v1/aeroportos')
  with app.app_context():
    db.create_all()
  app.run(debug=True)