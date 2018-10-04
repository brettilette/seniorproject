from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *
import requests

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))
linkedin_timeout_in_seconds = 1210000


def find_node_type(job):
    session = driver.session()

    cypher = """MATCH (n)
    WHERE id(n) = {id}
    RETURN labels(n) AS type"""

    result = session.run(cypher,id=job)

    session.close()

    results = [type["type"] for type in result]

    #print(results[0])

    return results[0]


def do_work(job, type):
    if str(type) == "['Company']":
        session = driver.session()
        cypher = """MATCH (n)
        WHERE id(n) = {id}
        RETURN
            CASE WHEN exists(n.LastSeenByLinkedIn) THEN duration.inSeconds(n.LastSeenByLinkedIn, datetime()).seconds
            ELSE -1 END as duration"""

        result = session.run(cypher, id=job)
        results = [duration["duration"] for duration in result]
        if results[0] >= linkedin_timeout_in_seconds or results[0] == -1:
            name = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.name", id=job)
            names = [result["n.name"] for result in name]
            json = requests.get('http://127.0.0.1/get/linkedin/employees/%s' % (names[0]))

            query = """WITH {json} as data
            UNWIND data.items as person
            MATCH (c)-[:HAS_TAG]->(t:Tag)
            WHERE id(c) = {id}
            MERGE (la:LinkedInAccount {address: person.URL})
            ON CREATE SET la.created = datetime(), la.createdBy = 'LinkedIn'
            ON MATCH SET la.LastSeenByLinkedIn = datetime()
            MERGE (la)-[:HAS_TAG]->(t)
            MERGE (p:Person {firstname: person.FirstName, lastname: person.LastName})
            ON CREATE SET p.created = datetime(), p.createdBy = 'LinkedIn'
            ON MATCH SET p.LastSeenByLinkedIn = datetime()
            MERGE (p)-[:HAS_TAG]->(t)
            MERGE (p)-[:HAS_ACCOUNT]->(la)
            MERGE (co:Company {name: person.Company})
            ON CREATE SET co.created = datetime(), co.createdBy = 'LinkedIn'
            ON MATCH SET co.LastSeenByLinkedIn = datetime()
            MERGE (co)-[:HAS_TAG]->(t)       
            MERGE (p)-[:WORKS_AT]->(co)"""

            session.run(query, json=json.json(), id=job)

        session.close()
