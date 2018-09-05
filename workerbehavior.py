from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *
import requests

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))
linkedin_timeout_in_seconds = 1210000


def find_node_type(job):
    session = driver.session()

    cypher = """MATCH (n)
    WHERE id(n) = {id}
    RETURN n"""

    result = session.run(cypher,id=job)

    session.close()

    return result


def do_work(job, type):
    if type == "LinkedInAccount":
        session = driver.session()

        cypher = """MATCH (n)
        WHERE id(n) = {id} AND exists(n.LastSeenByLinkedIn)
        RETURN duration.inSeconds(n.LastSeenByLinkedIn, datetime()) """

        result = session.run(cypher, id=job)

        if result >= linkedin_timeout_in_seconds:
            name = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.name", id=job)
            json = requests.get('127.0.0.1/get/linkedin/employees/%s' % (name))

            query = """WITH {json} as data
            UNWIND data.items as item
            MERGE (p:Person {firstname: item.firstname, lastname: item.lastname})
            ON CREATE SET p.created = datetime(), p.createdBy = 'LinkedIn'
            ON MATCH SET p.LastSeenByLinkedIn = datetime()
            MATCH (c)
            WHERE id(c) = {id}
            MERGE (p)-[:WORKS_AT]->(c)
            MERGE (la:LinkedInAccount {address: item.LinkedInAccount})
            ON CREATE SET la.created = datetime(), la.createdBy = 'LinkedIn'
            ON MATCH SET la.LastSeenByLinkedIn = datetime()
            MERGE (p)-[:HAS_ACCOUNT]->(la)"""

            session.run(query, json=json, id=job)

        session.close()