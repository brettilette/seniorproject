from flask import Flask, jsonify
from flask_restful import Resource, Api
from neo4j.v1 import GraphDatabase, basic_auth


driver = GraphDatabase.driver("bolt://hobby-egcmkjgcconogbkekpcmcobl.dbs.graphenedb.com:24786", auth=basic_auth("csa-laptop", "b.xAEJfrSq4KEn.tTSqgx0mSYCQq2Vx"))


# Connect to neo4j
app = Flask(__name__) #initializing web framework
api = Api(app)         #creating api


class Config(object):                       # Config for FLASK
    JSONIFY_PRETTYPRINT_REGULAR = True      # JSONIFY will indent and space if true


app.config.from_object(Config)

class GetLinkedInEmployees(Resource):
    def get(self, project_name,company_name):
        session = driver.session()
        cypher = "MERGE ( %s:Tag { name: %s } )\n" % (project_name, project_name)
        cypher += "ON CREATE SET %s.created = timestamp() + 'LinkedIn'\n" % (project_name)
        cypher += "ON MATCH SET %s.LinkedInModded = timestamp()\n" % (project_name)
        cypher += "RETURN %s.name, %s.created, %s.LinkedInModded" % (project_name)
        result = session.run(cypher)
        session.close()
        return jsonify(result)      # replace w/result


api.add_resource(GetLinkedInEmployees, '/get/linkedin/employees/<project_name>/<company_name>')


if __name__ == '__main__':  # run api on 127.0.0.1:5002
    app.run(port='5002')