from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Score(Resource):
    def get(self):
        return {"score" : "288"}

class Transactions(Resource):
    def get(self):
        return {"13/05/2021" : "Ultima consulta de situação no CPF do cliente."}

class Debts(Resource):
    def get(self):
        return {"14/06/2014" : "Pendencia na Loja A"}

api.add_resource(Score, '/score')
api.add_resource(Transactions, '/transactions')
api.add_resource(Debts, '/debts')


if __name__ == '__main__':
    app.run(debug=True)
