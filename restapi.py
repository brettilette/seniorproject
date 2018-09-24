from flask import Flask, jsonify
from flask_restful import Resource, Api
import json
from LinkedIn import FindEmployees



# Connect to neo4j
app = Flask(__name__) #initializing web framework
api = Api(app)         #creating api


class Config(object):                       # Config for FLASK
    JSONIFY_PRETTYPRINT_REGULAR = True      # JSONIFY will indent and space if true


app.config.from_object(Config)


class GetLinkedInEmployees(Resource):
    def get(self, company_name):
        results = FindEmployees(company_name)
        results = """{"items": """ + results + "}"
        return json.loads(results)


api.add_resource(GetLinkedInEmployees, '/get/linkedin/employees/<company_name>')


if __name__ == '__main__':  # run api on 127.0.0.1:5002
    app.run(port='80')