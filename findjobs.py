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

    session = driver.session()
    cypher = """MATCH (c:Company)
    RETURN id(c) AS job"""
    query = session.run(cypher)
    session.close()

    results = [job["job"] for job in query]

    return results