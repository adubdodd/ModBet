from flask import Flask
from flask_restful import Resource, Api
from test import get_odd_json

app = Flask(__name__)
api = Api(app)

class Team(Resource):
    def get(self):
        return get_odd_json()

api.add_resource(Team, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
