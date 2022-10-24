"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

After you can copy a text file word by word exactly
- Change the program to be faster (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp
import multiprocessing 

# Include cse 251 common Python files
from cse251 import *

def sender(conn, filename):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(filename, 'rb') as f:
        # Grab file line by line
        for line in f:
            # Grab line word by word
            for word in line:
                conn.send(word)

        conn.send(None)
        conn.close()



def receiver(conn, count, filename):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(filename, 'w') as f:
        while True:
            word = conn.recv()
            if word == None:
                break
            
            count.value += 1
            f.write(word)
        conn.close()


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    copy_conn, paste_conn = multiprocessing.Pipe()

    # TODO create variable to count items sent over the pipe
    count = Value('i', 0)

    # TODO create processes
    copier = Process(target=sender, args=(copy_conn, filename1))
    paster = Process(target=receiver, args=(paste_conn, count, filename2))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes
    copier.start()
    paster.start()
    
    # TODO wait for processes to finish
    copier.join()
    paster.join()

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {count.value}: ')
    log.write(f'items / second = {count.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    copy_file(log, 'bom.txt', 'bom-copy.txt')

