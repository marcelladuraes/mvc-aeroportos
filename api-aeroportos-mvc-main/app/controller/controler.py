
from app.models.model import app, db, AeroportoDataBaseSchema, AeroportoDataBase, parser, api
from flask_restful import Resource

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

        aeroporto_schema = AeroportoDataBaseSchema(
            only=['id_aeroporto', 'nome_aeroporto', 'cidade', 'codigo_pais_iso', 'codigo_iata', 'latitude', 'longitude',
                  'altitude'])
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
            aeroportoDataBase = AeroportoDataBase(aeroporto['id_aeroporto'], aeroporto['nome_aeroporto'],
                                                  aeroporto['cidade'], aeroporto['codigo_pais_iso'],
                                                  aeroporto['codigo_iata'], aeroporto['latitude'],
                                                  aeroporto['longitude'], aeroporto['altitude'])
            resp = aeroporto_schema.dump(aeroportoDataBase.create())
            return {"estacao": resp}, 201
        except Exception as e:
            return {"msg": e.args[0]}, 400

class Teste(Resource):
    def get(self):
        return {'msg': 'olá mundo'}

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)





