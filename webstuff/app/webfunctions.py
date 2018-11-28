from neo4j.v1 import GraphDatabase, basic_auth
from secrets import *

driver = GraphDatabase.driver(BOLT_ADDRESS, auth=basic_auth(DB_NAME, DB_AUTH))

def createProject(tag,company):
    session = driver.session()

    query = """Create (t:Tag{name:{tag}}),(c:Company{name:{company}}),(c)-[:HAS_TAG]->(t)"""

    session.run(query, tag=tag, company=company)


    session.close()


def getTags():
    session = driver.session()
    cypher = """MATCH (t:Tag)
        RETURN t.name as tag"""
    query = session.run(cypher)
    session.close()

    results = [tag["tag"] for tag in query]

    tags = []

    for result in results:
        if result != None:
            arr = []
            arr.append(result)
            arr.append(result)
            tags.append(arr)

    return tags

def insertTwitterAccount(tag, handle):
    if handle[0] != "@":
        handle = "@" + handle

    session = driver.session()

    query = """MERGE (t:Tag{name:{tag}}),(w:TwitterAccount{handle:{handle}}),(w)-[:HAS_TAG]->(t)"""

    session.run(query, tag=tag, handle=handle)

    session.close()


def insertEmailAccount(tag, address):

    session = driver.session()

    query = """MERGE (t:Tag{name:{tag}}),(e:EmailAccount{address:{address}}),(e)-[:HAS_TAG]->(t)"""

    session.run(query, tag=tag, address=address)

    session.close()

def insertLinkedInAccount(tag, address):

    session = driver.session()

    query = """MERGE (t:Tag{name:{tag}}),(e:LinkedInAccount{address:{address}}),(w)-[:HAS_TAG]->(t)"""

    session.run(query, tag=tag, address=address)

    session.close()

if __name__ == '__main__':
    createProject("test2","Wal-mart")
    print(getTags())