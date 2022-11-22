"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Jaxon Hamm

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  
  
- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:
I feel that I got a 4. I got it working with 2 sempahores and 1 lock 
and it meets the requirements as best as I can tell.

The wording of how values were being passed were somewhat confusing.
"""
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

def write(sl, write_slots, read_slots, lock, items_to_send):
    while True:

        # Get open write slot
        write_slots.acquire()
        
        # Touching list is a critical section
        lock.acquire()

        # Figure out where we are writing
        index = sl[-3] % BUFFER_SIZE
        
        # Check if we are done sending values
        if sl[-3] == items_to_send:
            # Let readers know we are done
            sl[index] = None
            read_slots.release()
            lock.release()
            return

        # Otherwise write value to the circular queue and signal that it is readable
        else:
            sl[index] = sl[-3] + 1
            read_slots.release()

        # Update index/count
        sl[-3] += 1
        lock.release()

def read(sl, write_slots, read_slots, lock):
    while True:
        # Get open read slot
        read_slots.acquire()

        # Touching the list is a critical section
        lock.acquire()

        # Figure out where we are reading
        index = sl[-2] % BUFFER_SIZE

        # Check if we are done reading
        if sl[index] == None:
            # Let other things into list and exit
            lock.release()
            write_slots.release()
            return
        
        # Otherwise retrieve value
        value = sl[index]

        # Update index and recieved count
        sl[-2] +=1
        sl[-1] +=1

        # Signal the value has been read
        write_slots.release()

        # Let other things in
        lock.release()

        # Process Data in Parallel
        print(value, end=', ', flush=True)


def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    sl = smm.ShareableList([0] * (BUFFER_SIZE + 3))

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    write_slots = mp.Semaphore(BUFFER_SIZE)
    read_slots = mp.Semaphore(0)

    lock = mp.Lock()

    # TODO - create reader and writer processes
    writers = []
    for _ in range(WRITERS):
        writers.append(mp.Process(target=write, args=(sl, write_slots, read_slots, lock, items_to_send)))
    
    readers = []
    for _ in range(READERS):
        readers.append(mp.Process(target=read, args=(sl, write_slots, read_slots, lock)))

    
    # TODO - Start the processes and wait for them to finish
    for p in writers:
        p.start()
    for p in readers:
        p.start()

    for p in writers:
        p.join()
    for p in readers:
        p.join()
    print()
    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    print(f'{sl[-1]} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()
