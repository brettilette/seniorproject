from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))

linkedin_timeout_in_seconds = 1210000
twitter_timeout_in_seconds = 86400


def find_jobs():
    jobs = []

    results = look_for_companies()
    for result in results:
        if result != None:
            job = []
            job.append(result)
            job.append("LinkedIn")
            jobs.append(job)

    results = look_for_new_twitter_accounts()
    for result in results:
        if result != None:
            job = []
            job.append(result)
            job.append("TwitterNew")
            jobs.append(job)

    results = look_for_tweet_sentiment()
    for result in results:
        if result != None:
            job = []
            job.append(result)
            job.append("Sentiment")
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


def look_for_new_twitter_accounts():

    session = driver.session()
    cypher = """MATCH (t:TwitterAccount)
        WHERE NOT exists(t.LastSeenByTwitter)
        RETURN id(t)
        AS job"""
    query = session.run(cypher, time=twitter_timeout_in_seconds)
    session.close()

    results = [job["job"] for job in query]

    return results


def look_for_tweet_sentiment():

    session = driver.session()

    cypher = """MATCH (t:Tweet)
            WHERE NOT exists(t.LastSeenBySentiment)
            RETURN id(t)
            AS job"""

    query = session.run(cypher, time=twitter_timeout_in_seconds)
    session.close()

    results = [job["job"] for job in query]

    return results