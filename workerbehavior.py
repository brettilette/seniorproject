from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *
import requests
import bs4
import nltk

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))


def do_work(job):
    if job[1] == "LinkedIn":
        linkedin_module(job[0])

    if job[1] == "TwitterNew":
        twitter_new_module(job[0])

    if job[1] == "Sentiment":
        sentiment_module(job[0])

    if job[1] == "Glassdoor":
        glassdoor_module(job[0])

    if job[1] == "SentimentReview":
        sentiment_review_module(job[0])

    if job[1] == "WorkhistoryBrett":
        workhistory_brett_module(job[0])

    if job[1] == "WorkhistoryJames":
        workhistory_james_module(job[0])


def linkedin_module(job):
    session = driver.session()

    name = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.name", id=job)
    names = [result["n.name"] for result in name]
    json = requests.get('http://127.0.0.1:8000/linkedin/employees/%s' % (names[0]))

    query = """WITH {json} as data
            UNWIND data.items as person
            MATCH (c)-[:HAS_TAG]->(t:Tag)
            WHERE id(c) = {id}
            SET c.LastSeenByLinkedIn = datetime()
            MERGE (la:LinkedInAccount {address: person.URL, workhistory: person.DatesEmployed})
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

    session.run(query, id=job)

    query = """MATCH (p:Person)-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(c:Company)
                    WHERE NOT p.company = c.name
                    MERGE (p)-[:WORKED_FOR]->(c)"""

    session.run(query, id=job)

    session.close()


def twitter_new_module(job):
    session = driver.session()

    handle = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.handle", id=job)
    handles = [result["n.handle"] for result in handle]
    json = requests.get('http://127.0.0.1:8000/twitter/tweets/%s' % (handles[0]))

    query = """WITH {json} as data
            UNWIND data.items as tweet
            MATCH (c)-[:HAS_TAG]->(t:Tag)
            WHERE id(c) = {id}
            SET c.LastSeenByTwitter = datetime()
            MERGE (tw:Tweet {id: tweet.id, text: tweet.text})
            ON CREATE SET tw.created = datetime(), tw.createdBy = 'TwitterNew', tw.LastSeenByTwitter = datetime()
            ON MATCH SET tw.LastSeenByTwitter = datetime()
            MERGE (tw)-[:HAS_TAG]->(t)
            MERGE (c)-[:HAS_TWEET]->(tw)"""

    session.run(query, json=json.json(), id=job)

    session.close()


def sentiment_module(job):
    session = driver.session()

    text = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.text", id=job)
    texts = [result["n.text"] for result in text]

    if texts[0] != None:
        soup = bs4.BeautifulSoup(texts[0],'lxml').get_text()
        input = nltk.Text(soup)

        json = requests.get('http://127.0.0.1:8000/sentiment/%s' % (input.concordance))

        if json.status_code == 200:
            query = """WITH {json} as data
                    UNWIND data.items as sentiment
                    MATCH (c)-[:HAS_TAG]->(t:Tag)
                    WHERE id(c) = {id}
                    SET c.LastSeenBySentiment = datetime(),
                    c.polarity = sentiment.polarity,
                    c.subjectivity = sentiment.subjectivity"""

            session.run(query, json=json.json(), id=job)

        if json.status_code == 404:
            query = """MATCH (c)-[:HAS_TAG]->(t:Tag)
                    WHERE id(c) = {id}
                    SET c.LastSeenBySentiment = datetime(),
                    c.error = "Sentiment404"
                    """

            session.run(query, id=job)

    session.close()


def glassdoor_module(job):
    session = driver.session()

    name = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.name", id=job)
    names = [result["n.name"] for result in name]
    json = requests.get('http://127.0.0.1:8000/glassdoor/reviews/%s' % (names[0]))

    if json.status_code == 200:
        query = """WITH {json} as data
            UNWIND data.items as review
            MATCH (c)-[:HAS_TAG]->(t:Tag)
            WHERE id(c) = {id}
            SET c.LastSeenByGlassdoor = datetime()
            MERGE (r:Review {pros: review.Pros, cons: review.Cons})
            ON CREATE SET r.created = datetime(), r.createdBy = 'Glassdoor'
            ON MATCH SET r.LastSeenByGlassdoor = datetime()
            MERGE (r)-[:HAS_TAG]->(t)
            MERGE (c)-[:HAS_REVIEW]->(r)"""

        session.run(query, json=json.json(), id=job)

    session.close()


def sentiment_review_module(job):
    session = driver.session()

    text = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.pros", id=job)
    texts = [result["n.pros"] for result in text]

    if texts[0] != None:
        soup = bs4.BeautifulSoup(texts[0],'lxml').get_text()
        input = nltk.Text(soup)

        json = requests.get('http://127.0.0.1:8000/sentiment/%s' % (input.concordance))

        if json.status_code == 200:
            query = """WITH {json} as data
                    UNWIND data.items as sentiment
                    MATCH (c)-[:HAS_TAG]->(t:Tag)
                    WHERE id(c) = {id}
                    SET c.LastSeenBySentiment = datetime(),
                    c.proPolarity = sentiment.polarity,
                    c.proSubjectivity = sentiment.subjectivity"""

            session.run(query, json=json.json(), id=job)

    text = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.cons", id=job)
    texts = [result["n.cons"] for result in text]

    if texts[0] != None:
        soup = bs4.BeautifulSoup(texts[0],'lxml').get_text()
        input = nltk.Text(soup)

        json = requests.get('http://127.0.0.1:8000/sentiment/%s' % (input.concordance))

        if json.status_code == 200:
            query = """WITH {json} as data
                        UNWIND data.items as sentiment
                        MATCH (c)-[:HAS_TAG]->(t:Tag)
                        WHERE id(c) = {id}
                        SET c.LastSeenBySentiment = datetime(),
                        c.conPolarity = sentiment.polarity,
                        c.conSubjectivity = sentiment.subjectivity"""

            session.run(query, json=json.json(), id=job)

    session.close()


def workhistory_brett_module(job):
    session = driver.session()

    text = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.workhistory", id=job)
    texts = [result["n.workhistory"] for result in text]

    if texts[0] != None:
        json = requests.get('http://127.0.0.1:8000/workhistory/brett/%s' % (texts[0]))

        if json.status_code == 200:
            query = """WITH {json} as data
                    UNWIND data.items as history
                    MATCH (c)-[:HAS_TAG]->(t:Tag)
                    WHERE id(c) = {id}
                    SET c.LastSeenByWorkhistoryBrett = datetime(),
                    c.averageDaysWorked = history.averageDaysWorked,
                    c.stdDev = history.stdDev,
                    c.anomalies = history.anomalies"""

            session.run(query, json=json.json(), id=job)

        if json.status_code == 404:
            query = """MATCH (c)-[:HAS_TAG]->(t:Tag)
                    WHERE id(c) = {id}
                    SET c.LastSeenByWorkhistoryBrett = datetime(),
                    c.error = "WorkhistoryBrett404"
                    """

            session.run(query, id=job)

    session.close()


def workhistory_james_module(job):
    session = driver.session()

    text = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.workhistory", id=job)
    history = [result["n.workhistory"] for result in text]

    text = session.run("MATCH (n)\nWHERE id(n) = {id}\nRETURN n.targetSignifier", id=job)
    target = [result["n.targetSignifier"] for result in text]

    if history[0] != None and target[0] != None:
        json = requests.get('http://127.0.0.1:8000/workhistory/james/%s/%s' % (history[0],target[0]))

        if json.status_code == 200:
            query = """WITH {json} as data
                    UNWIND data.items as history
                    MATCH (c)-[:HAS_TAG]->(t:Tag)
                    WHERE id(c) = {id}
                    SET c.LastSeenByWorkhistoryJames = datetime(),
                    c.hasAnomaly = history.hasAnomaly"""

            session.run(query, json=json.json(), id=job)

        if json.status_code == 404:
            query = """MATCH (c)-[:HAS_TAG]->(t:Tag)
                    WHERE id(c) = {id}
                    SET c.LastSeenByWorkhistoryJames = datetime(),
                    c.error = "WorkhistoryJames404"
                    """

            session.run(query, id=job)

    session.close()