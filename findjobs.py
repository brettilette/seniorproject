from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))


def find_jobs():
    jobs = []

    results = look_for_companies()
    for job in results:
        jobs.append(job)

    return jobs


def look_for_companies():
    results = []

    session = driver.session()
    query = session.run("Match (c)-[:HAS_TAG]->(t)\nWHERE c:Company AND t:Tag AND size((c)-[:]-()) = 1\nRETURN id(c)")
    session.close()

    for job in query:
        results.append(job)

    return results