from flask import Flask
from flask_restful import Resource, Api
import json
from LinkedIn import FindEmployees
from haveIbeenPawned import is_breached
from twitter import getTweets
from sentiment import sentiment_analysis
from logstash import update_kibana
from Glassdoor import glassdoor_reviews

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


class GetUpdateKibana(Resource):
    def get(self):
        update_kibana()
        results = """{"status": "completed"}"""
        return json.loads(results)


class GetGlassdoorReviews(Resource):
    def get(self, company_name):
        results = glassdoor_reviews(company_name)
        results = """{"items": """ + results + "}"
        return json.loads(results)


api.add_resource(GetLinkedInEmployees, '/linkedin/employees/<company_name>')
api.add_resource(HaveIBeenPwned, '/HIBP/email/<email>')
api.add_resource(GetTweetsSince, '/twitter/tweetssince/<handle>/<date>')
api.add_resource(GetTweets, '/twitter/tweets/<handle>')
api.add_resource(GetSentiment, '/sentiment/<text>')
api.add_resource(GetUpdateKibana, '/kibana/update')
api.add_resource(GetGlassdoorReviews, '/glassdoor/reviews/<company_name>')


if __name__ == '__main__':
    app.run(port='8000')