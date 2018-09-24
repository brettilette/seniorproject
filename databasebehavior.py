import logging
from queue import Queue
from threading import Thread
from findjobs import find_jobs
from workerbehavior import  find_node_type, do_work


logging.basicConfig(filename='databasebehaivor.log',level=logging.DEBUG)
numberOfThreads = 1


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
            except IndexError:
                return
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
