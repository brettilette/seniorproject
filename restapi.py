from flask import Flask, jsonify
from flask_restful import Resource, Api
import json
from LinkedIn import FindEmployees
from haveIbeenPawned import is_breached
from twitter import getTweets

# Connect to neo4j
app = Flask(__name__) #initializing web framework
api = Api(app)         #creating api


class Config(object):                       # Config for FLASK
    JSONIFY_PRETTYPRINT_REGULAR = True      # JSONIFY will indent and space if true


app.config.from_object(Config)


class GetLinkedInEmployees(Resource):
    def get(self, company_name):
        results = FindEmployees(company_name)# """{"people":[{"fname":"Jimothy","lname":"Simmons","company":"%s","url":"linkedin.com/in/jimothy-simmons"},{"fname": "Simothy","lname":"Jimmons","company":"%s","url":"linkedin.com/in/simothy-jimmons"}]}""" % (company_name,company_name)
        results = """{"items": """ + results + "}"
        return json.loads(results)      # replace w/result


class HaveIBeenPwned(Resource):
    def get(self, email):
        if(is_breached(email)):
            results = """{
	"items": [{
		"pwned": "true"
	}]
}"""
            return json.loads(results)
        else:
            results = """{
	"items": [{
		"pwned": "false"
	}]
}"""
            return json.loads(results)


class GetTweetsSince(Resource):
    def get(self, handle, date):
        results = '{"items" :' + getTweets(handle,date,"") + '}'
        return json.loads(results)


class GetTweets(Resource):
    def get(self, handle):
        results = '{"items" :' + getTweets(handle,"","") + '}'
        return json.loads(results)


api.add_resource(GetLinkedInEmployees, '/get/linkedin/employees/<company_name>')
api.add_resource(HaveIBeenPwned, '/get/HIBP/email/<email>')
api.add_resource(GetTweetsSince, '/get/twitter/tweetssince/<handle>/<date>')
api.add_resource(GetTweets, '/get/twitter/tweets/<handle>')

if __name__ == '__main__':  # run api on 127.0.0.1:5002
    app.run(port='8000')