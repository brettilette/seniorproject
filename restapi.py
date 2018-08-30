from flask import Flask, jsonify
from flask_restful import Resource, Api
# import neo4j


# Connect to neo4j
app = Flask(__name__) #initializing web framework
api = Api(app)         #creating api


class CompanyInfo(Resource):
    def get(self, company_name):
        # create neo4j connection variable
        # pass company_name to the web scraper
        # result = store web scraper info
        # store result in neo4j
        # result = "firstName = 'Jimmothy',lastName = 'Simmons',companyName = %s" %company_name # dummy result
        return jsonify(firstName = 'Jimmothy',lastName = 'Simmons',companyName = company_name)      # return result in json format


api.add_resource(CompanyInfo, '/companyinfo/<company_name>')


if __name__ == '__main__':  # run api on 127.0.0.1:5002
    app.run(port='5002')