import logging
import sys

from flask import Flask
from flask_redis import FlaskRedis
from flask_cors import CORS
from flask_restful import reqparse, Api

from bookies.bet365 import CheckNickname
from bookies.bet365 import Register as Bet352Register



app = Flask(__name__)

redis_client = FlaskRedis(app)
CORS(app)
api = Api(app)


api.add_resource(CheckNickname, '/bet365/nickname')
api.add_resource(Bet352Register, '/bet365/register')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
