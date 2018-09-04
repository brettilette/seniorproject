from flask import Flask, jsonify
from flask_restful import Resource, Api



# Connect to neo4j
app = Flask(__name__) #initializing web framework
api = Api(app)         #creating api


class Config(object):                       # Config for FLASK
    JSONIFY_PRETTYPRINT_REGULAR = True      # JSONIFY will indent and space if true


app.config.from_object(Config)

class GetLinkedInEmployees(Resource):
    def get(self, project_name,company_name):
        results = "Call the scraper and get a result"
        return jsonify(results)      # replace w/result


api.add_resource(GetLinkedInEmployees, '/get/linkedin/employees/<project_name>/<company_name>')


if __name__ == '__main__':  # run api on 127.0.0.1:5002
    app.run(port='80')