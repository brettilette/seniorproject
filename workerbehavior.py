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

        name = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.name", id=job)
        names = [result["n.name"] for result in name]
        json = requests.get('http://127.0.0.1/get/linkedin/employees/%s' % (names[0]))

        query = """WITH {json} as data
        UNWIND data.items as person
        MATCH (c)-[:HAS_TAG]->(t:Tag)
        WHERE id(c) = {id}
        SET c.LastSeenByLinkedIn = datetime()
        MERGE (la:LinkedInAccount {address: person.URL, workhistory: person.JobLength})
        ON CREATE SET la.created = datetime(), la.createdBy = 'LinkedIn'
        ON MATCH SET la.LastSeenByLinkedIn = datetime()
        MERGE (la)-[:HAS_TAG]->(t)
        MERGE (p:Person {firstname: person.FirstName, lastname: person.LastName,company: person.Company})
        ON CREATE SET p.created = datetime(), p.createdBy = 'LinkedIn'
        ON MATCH SET p.LastSeenByLinkedIn = datetime()
        MERGE (p)-[:HAS_TAG]->(t)
        MERGE (p)-[:HAS_ACCOUNT]->(la)"""

        session.run(query, json=json.json(), id=job)

        query = """MATCH (p:Person)-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(c:Company)
        WHERE p.company = c.name
        MERGE (p)-[:WORKS_FOR]->(c)"""

        session.run(query,id=job)

        query = """MATCH (p:Person)-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(c:Company)
                WHERE NOT p.company = c.name
                MERGE (p)-[:WORKED_FOR]->(c)"""

        session.run(query, id=job)

        session.close()
