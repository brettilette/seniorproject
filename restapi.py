from flask import Flask, jsonify
from flask_restful import Resource, Api
import json
from LinkedIn import FindEmployees
from haveIbeenPawned import is_breached
from twitter import getTweets
from sentiment import sentiment_analysis

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


class GetSentiment(Resource):
    def get(self, text):
        result = sentiment_analysis(text)
        results = """{
	"items": [{
		"polarity": "%s",
		"subjectivity": "%s"
	}]
}
        """ % (result[0], result[1])
        return json.loads(results)


api.add_resource(GetLinkedInEmployees, '/get/linkedin/employees/<company_name>')
api.add_resource(HaveIBeenPwned, '/get/HIBP/email/<email>')
api.add_resource(GetTweetsSince, '/get/twitter/tweetssince/<handle>/<date>')
api.add_resource(GetTweets, '/get/twitter/tweets/<handle>')
api.add_resource(GetSentiment, '/get/sentiment/<text>')


if __name__ == '__main__':  # run api on 127.0.0.1:5002
    app.run(port='8000')