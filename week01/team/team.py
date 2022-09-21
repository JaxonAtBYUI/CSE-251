"""
Course: CSE 251
Lesson Week: 01 - Team Acvitiy
File: team.py
Author: Brother Comeau

Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review team acvitiy details in I-Learn

"""

from datetime import datetime, timedelta
import threading


# Include cse 251 common Python files
from cse251 import *

# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0

def is_prime(n: int) -> bool:
    global numbers_processed
    numbers_processed += 1

    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO 1) Get this program running
    # TODO 2) move the following for loop into 1 thread
    # TODO 3) change the program to divide the for loop into 10 threads

    # Parameters set to determine what each thread will be checking.
    start = 10000000000
    range_count = 100000
    thread_count = 10
    thread_range = range_count // thread_count

    # Create an array to hold the threads.
    threads = []

    # Define the behavior of a thread.
    def thread_function(start, thread_range):
        global prime_count
        for i in range(start, start + thread_range):
            if is_prime(i):
                prime_count += 1
                # print(i, end=', ', flush=True)
        print(flush=True)

    # Create each thread
    for i in range(thread_count):
        threads.append(threading.Thread(target=thread_function, args=(start + (i * thread_range), thread_range)))

    for t in range(thread_count):
        threads[t].start()
    
    for t in range(thread_count):
        threads[t].join()



    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')


