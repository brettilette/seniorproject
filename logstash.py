from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *
import json
import requests

# Host and port of Logstash so the program knows where to send the data.
# If the host IP or the port Logstash is listening to changes it must be changed here.
URL = 'http://10.0.51.31:9200'
HEADER = {'content-type': 'application/json'}

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))


def grab_data():
    """Grab the data from the Neo4J database and store it in a JSON"""

    session = driver.session()
    # TODO Come up with appropriate cypher query
    cypher = """MATCH (t:Tweet) WHERE NOT t.polarity = "0.0" return t.polarity as polarity"""
    query = session.run(cypher)
    session.close()

    results = [polarity["polarity"] for polarity in query]
    somejson = """{"sentiment": ["""
    for result in results:
        some_string = """{"polarity": %s}""" % (result)
        somejson += some_string

    somejson += """]}"""
    return json.loads(somejson)  # TODO put in JSON format before returning


def send_to_logstash(payload):
    """Send the JSON of data from Neo4J to Logstash so it can be sent to kibana"""

    r = requests.post(URL,json=payload,headers=HEADER)
    return r.json()


def update_kibana():
    print(send_to_logstash(grab_data()))


if __name__ == '__main__':
    # update_kibana()
    print(grab_data())