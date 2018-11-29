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

    results = look_for_reviews()
    for result in results:
        if result != None:
            job = []
            job.append(result)
            job.append("Glassdoor")
            jobs.append(job)

    results = look_for_review_sentiment()
    for result in results:
        if result != None:
            job = []
            job.append(result)
            job.append("SentimentReview")
            jobs.append(job)

    results = look_for_workhistory_brett()
    for result in results:
        if result != None:
            job = []
            job.append(result)
            job.append("WorkhistoryBrett")
            jobs.append(job)

    results = look_for_workhistory_james()
    for result in results:
        if result != None:
            job = []
            job.append(result)
            job.append("WorkhistoryJames")
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


def look_for_reviews():

    session = driver.session()
    cypher = """MATCH (c:Company)
    RETURN
        CASE WHEN exists(c.LastSeenByGlassdoor) AND duration.inSeconds(c.LastSeenByGlassdoor, datetime()).seconds > {time}
        THEN id(c)
        WHEN NOT exists(c.LastSeenByGlassdoor)
        THEN id(c)
        END AS job"""
    query = session.run(cypher, time=linkedin_timeout_in_seconds)
    session.close()

    results = [job["job"] for job in query]

    return results


def look_for_review_sentiment():

    session = driver.session()

    cypher = """MATCH (t:Review)
            WHERE NOT exists(t.LastSeenBySentiment)
            RETURN id(t)
            AS job"""

    query = session.run(cypher)
    session.close()

    results = [job["job"] for job in query]

    return results


def look_for_workhistory_brett():

    session = driver.session()

    cypher = """MATCH (t:LinkedInAccount)
            WHERE NOT exists(t.LastSeenByWorkhistoryBrett)
            RETURN id(t)
            AS job"""

    query = session.run(cypher)
    session.close()

    results = [job["job"] for job in query]

    return results

def look_for_workhistory_james():

    session = driver.session()

    cypher = """MATCH (t:LinkedInAccount)
            WHERE NOT exists(t.LastSeenByWorkhistoryJames) AND exists(t.targetSignifier)
            RETURN id(t)
            AS job"""

    query = session.run(cypher)
    session.close()

    results = [job["job"] for job in query]

    return results


def look_for_emails():
    session = driver.session()

    cypher = """MATCH (t:EmailAccount)
                WHERE NOT exists(t.LastSeenByHIBP)
                RETURN id(t)
                AS job"""

    query = session.run(cypher)
    session.close()

    results = [job["job"] for job in query]

    return results