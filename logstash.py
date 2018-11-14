from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *
import json
import requests

#Host and port of Logstash so the program knows where to send the data.
#If the host IP or the port Logstash is listening to changes it must be changed here.
HOST = '10.0.51.31'
PORT = 9200

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))

#Grab the data from the Neo4J database and store it in a JSON
def grab_data():

    session = driver.session()
    #Come up with appropriate cypher query
    cypher = """"""
    query = session.run(cypher)
    session.close()

    results = [job["job"] for job in query]

    return results

#Send the JSON of data from Neo4J to Logstash so it can be sent to kibana
def send_to_logstash():

    #Thomas put things here