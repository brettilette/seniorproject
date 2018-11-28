from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *
import json
import requests

# Host and port of Logstash so the program knows where to send the data.
# If the host IP or the port Logstash is listening to changes it must be changed here.
URL = 'http://127.0.0.1:9200/sentiment/all/1' # TODO have the 1 change to a datetime object
HEADER = {'content-type': 'application/json'}

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))
# TODO comment this bad boy

def grab_data(tag):
    """Grab the data from the Neo4J database and store it in a JSON"""

    somejson = """{"""

    somejson += grab_twitter_sentiment(tag)
    somejson += grab_review_sentiment(tag)
    somejson += grab_total_workhistory(tag)

    if somejson[-1] == ",":
        somejson = somejson[:-1]
    print(somejson)
    return json.loads(somejson)


def grab_twitter_sentiment(tag):
    session = driver.session()
    cypher = """MATCH (t:Tweet)-[:HAS_TAG]->(:Tag {name: {tag}}) return t.polarity as polarity"""
    query = session.run(cypher, tag=tag)
    session.close()

    results = [polarity["polarity"] for polarity in query]
    somejson = """"tweetSentiment": ["""
    for result in results:
        if result != None:
            some_string = """%s,""" % (result)
            somejson += some_string
    if somejson[-1] == ",":
        somejson = somejson[:-1]
    somejson += """],"""
    return somejson


def grab_review_sentiment(tag):
    session = driver.session()
    cypher = """MATCH (t:Review)-[:HAS_TAG]->(:Tag {name: {tag}}) return t.conPolarity, t.proPolarity as polarity"""
    query = session.run(cypher, tag=tag)
    session.close()

    results = [polarity["polarity"] for polarity in query]
    somejson = """"reviewSentiment": ["""
    for result in results:
        some_string = """%s,""" % (result)
        somejson += some_string
    if somejson[-1] == ",":
        somejson = somejson[:-1]
    somejson += """],"""
    return somejson


def grab_total_workhistory(tag):
    somejson = """"totalWorkhistory": ["""

    session = driver.session()
    cypher = """MATCH (t:LinkedInAccount)-[:HAS_TAG]->(:Tag {name: {tag}}) WHERE exists(t.averageDaysWorked) return t.averageDaysWorked as thing"""
    query = session.run(cypher, tag=tag)
    session.close()

    results = [thing["thing"] for thing in query]
    somejson += """{"averageDaysWorked": ["""
    for result in results:
        some_string = """%s,""" % (result)
        somejson += some_string
    if somejson[-1] == ",":
        somejson = somejson[:-1]
    somejson += """]},"""

    session = driver.session()
    cypher = """MATCH (t:LinkedInAccount)-[:HAS_TAG]->(:Tag {name: {tag}}) WHERE exists(t.stdDev) return t.stdDev as thing"""
    query = session.run(cypher, tag=tag)
    session.close()

    results = [thing["thing"] for thing in query]
    somejson += """{"standardDeviations": ["""
    for result in results:
        some_string = """%s,""" % (result)
        somejson += some_string
    if somejson[-1] == ",":
        somejson = somejson[:-1]
    somejson += """]},"""

    session = driver.session()
    cypher = """MATCH (t:LinkedInAccount)-[:HAS_TAG]->(:Tag {name: {tag}}) WHERE exists(t.anomalies) return size(t.anomalies) as thing"""
    query = session.run(cypher, tag=tag)
    session.close()

    results = [thing["thing"] for thing in query]
    somejson += """{"totalAnomalies": ["""
    for result in results:
        some_string = """%s,""" % (result)
        somejson += some_string
    if somejson[-1] == ",":
        somejson = somejson[:-1]
    somejson += """]},"""

    session = driver.session()
    cypher = """MATCH (t:LinkedInAccount)-[:HAS_TAG]->(:Tag {name: {tag}}) WHERE exists(t.hasAnomaly) AND t.hasAnomaly = True return t.hasAnomaly as thing"""
    query = session.run(cypher, tag=tag)
    session.close()

    results = [thing["thing"] for thing in query]
    somejson += """{"relevantAnomalies": ["""
    for result in results:
        some_string = """%s,""" % (result)
        somejson += some_string
    if somejson[-1] == ",":
        somejson = somejson[:-1]
    somejson += """]},"""

    if somejson[-1] == ",":
        somejson = somejson[:-1]
    somejson += """]},"""
    return somejson


def send_to_logstash(payload):
    """Send the JSON of data from Neo4J to Logstash so it can be sent to kibana"""

    r = requests.put(URL,json=payload,headers=HEADER)
    return r.json()


def update_kibana(tag):
    print(send_to_logstash(grab_data(tag)))


if __name__ == '__main__':
    update_kibana("test")
