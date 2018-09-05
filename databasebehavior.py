import logging
from queue import Queue
from threading import Thread
from findjobs import find_jobs
from workerbehavior import  find_node_type, do_work


logging.basicConfig(filename='databasebehaivor.log',level=logging.DEBUG)
numberOfThreads = 3

# cypher = "Match (c)-[:HAS_TAG]->(t)\nWHERE c:Company AND t:Tag AND size((c)-[:]-()) = 1\nRETURN t.name, c.name"
#
# results = session.run(cypher)
# json = requests.get("127.0.0.1/get/linkedin/employees/%s/%s" % (results[0],results[1]))
#
# query = """WITH {json} as data
# UNWIND data.items as item
# MERGE (p:Person {firstname: item.firstname, lastname: item.lastname})
# ON CREATE SET p.created = timestamp() + ' by LinkedIn'
# ON MATCH SET p.LastSeenByLinkedIn = timestamp()
# MERGE (la:LinkedInAccount {address: item.LinkedInAccount})
# ON CREATE SET la.created = timestamp() + ' by LinkedIn'
# ON MATCH SET la.LastSeenByLinkedIn = timestamp()
# MERGE (p)-[:HAS_ACCOUNT]->(la)"""
#
# session.run(query,json=json)
#
# session.close()


class Worker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            job = self.queue.get()          # Get the id of the node that needs attention
            try:
                type = find_node_type(job)  # Get the type of the node that is being worked on
                do_work(job,type)           # Look in the database to get the rules for working on a node of that type
                                            # If permission is given, contact the api and request info
                                            # Finally, add any new information to the database
            finally:
                self.queue.task_done()





def main():
    while True:
        jobs = find_jobs()                  # Gets a list of node ids that need more information
        queue = Queue()                     # initialize the worker's queue

        for x in range(numberOfThreads):    # Create workers based on the numberOfThreads
            worker = Worker(queue)          # Pass the queue to each worker
            worker.daemon = True            # Allows to the program to continue while workers run concurrently
            worker.start()

        for job in jobs:                    #Puts jobs in the queue
            queue.put(job)

        queue.join()                        #Wait for workers to finish


if __name__ == '__main__':
    main()
