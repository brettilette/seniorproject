from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *
import requests
driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))

session = driver.session()

cypher = "Match (c)-[:HAS_TAG]->(t)\nWHERE c:Company AND t:Tag AND size((c)-[:]-()) = 1\nRETURN t.name, c.name"

results = session.run(cypher)
json = requests.get("127.0.0.1/get/linkedin/employees/%s/%s" % (results[0],results[1]))

query = """WITH {json} as data
UNWIND data.items as item
MERGE (p:Person {firstname: item.firstname, lastname: item.lastname})
ON CREATE SET p.created = timestamp() + ' by LinkedIn'
ON MATCH SET p.LastSeenByLinkedIn = timestamp()
MERGE (la:LinkedInAccount {address: item.LinkedInAccount})
ON CREATE SET la.created = timestamp() + ' by LinkedIn'
ON MATCH SET la.LastSeenByLinkedIn = timestamp()
MERGE (p)-[:HAS_ACCOUNT]->(la)"""

session.run(query,json=json)

session.close()