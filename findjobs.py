from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))
linkedin_timeout_in_seconds = 1210000

def find_jobs():
    jobs = []

    results = look_for_companies()
    for job in results:
        jobs.append(job)

    return jobs


def look_for_companies():

    session = driver.session()
    cypher = """MATCH (c:Company)
    RETURN
        CASE WHEN exists(c.LastSeenByLinkedIn) AND duration.inSeconds(c.LastSeenByLinkedIn, datetime()).seconds > {time}
        THEN id(c)
        WHEN NOT exists(c.LastSeenByLinkedIn)
        THEN id(c)
        END AS job"""
    query = session.run(cypher, time=linkedin_timeout_in_seconds)
    session.close()

    results = [job["job"] for job in query]

    return results