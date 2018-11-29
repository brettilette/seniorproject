from neo4j.v1 import GraphDatabase, basic_auth


driver = GraphDatabase.driver("bolt://10.0.51.31:7687", auth=basic_auth("neo4j", 'N48Wk2w,=NE"A{SK'))


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

    query = """MATCH (t:Tag {name: {tag}})
    MERGE (w:TwitterAccount {handle: {handle}})-[:HAS_TAG]->(t)"""

    session.run(query, tag=tag, handle=handle)

    session.close()


def insertEmailAccount(tag, address):

    session = driver.session()

    query = """MATCH (t:Tag {name: {tag}})
    MERGE (e:EmailAccount{address:{address}})-[:HAS_TAG]->(t)"""

    session.run(query, tag=tag, address=address)

    session.close()


def insertLinkedInAccount(tag, address):

    session = driver.session()

    query = """MATCH (t:Tag {name: {tag}})
    MERGE (e:LinkedInAccount{address:{address}})-[:HAS_TAG]->(t)"""

    session.run(query, tag=tag, address=address)

    session.close()


if __name__ == '__main__':
    createProject("test2","Wal-mart")
    print(getTags())