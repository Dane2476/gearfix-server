from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
CORS(app)

items = [{'brand': 'Fender', 'model': 'Stratocaster'}]
items.append({'brand': 'Gibson', 'model': 'SG'})


class Buy(Resource):
    def get(self):
        return items


class Sell(Resource):
    def post(self):
        listing = request.get_json()
        print(listing)
        return {'you sent': listing}, 201


api.add_resource(Buy, '/buy')
api.add_resource(Sell, '/sell')

if __name__ == '__main__':
    app.run(debug=True)
