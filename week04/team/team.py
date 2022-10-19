"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(jobs, urls, log):  # TODO add arguments
    """ Process values from the data_queue """
    jobs.acquire()
    url = urls.get()

    # TODO check to see if anything is in the queue
    while (url != NO_MORE_VALUES):
        # TODO process the value retrieved from the queue
        promise = requests.get(url)
        if promise.status_code == 200:
            log.write(promise.JSON()['name'])
        else:
            print(f"\tFailure: {promise.status_code}")

        jobs.acquire()
        url = urls.get()

         
        



def file_reader(urls, jobs, log): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    f = open("./week04/team/urls.txt", "r")

    fout = f.readlines()
    print(fout)

    for url in fout:
        urls.put(url)
        jobs.release()
    
    for threads in range(RETRIEVE_THREADS):
        urls.put(NO_MORE_VALUES)
        jobs.release()

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"



def main():
    """ Main function """
    log = Log(show_terminal=True)

    # TODO create queue
    urls = queue.Queue()

    # TODO create semaphore (if needed)
    jobs = threading.Semaphore(0)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    threads = []
    threads.append(threading.Thread(target=file_reader, args=(urls, jobs, log)))
    for i in range(RETRIEVE_THREADS):
        threads.append(threading.Thread(target=retrieve_thread, args=(jobs, urls, log)))

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    for thread in threads:
        thread.start()

    # TODO Wait for them to finish - The order doesn't matter
    for thread in threads:
        thread.join()

    log.stop_timer('Time to process all URLS')

if __name__ == '__main__':
    main()




