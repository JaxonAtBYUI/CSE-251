"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py

It seems to me to follows all of the laid out rules.
Because of this I feel that I recieved a 4.
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

def cleaner(id, room_key, cleaned_count):
    end_time = time.time() + TIME
    while time.time() < end_time:
        cleaner_waiting()
        
        room_key.acquire()
        
        print(STARTING_CLEANING_MESSAGE, flush=True)
        cleaner_cleaning(id)
        cleaned_count.value += 1
        print(STOPPING_CLEANING_MESSAGE, flush=True)
        
        room_key.release()
    
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """

def guest(id, room_key, doorway, guest_count, party_count):
    end_time = time.time() + TIME
    while time.time() < end_time:
        guest_waiting()

        # Check for party
        doorway.acquire()
        # If there's no party, wait to start one
        if guest_count.value == 0:
            room_key.acquire()
            print(STARTING_PARTY_MESSAGE, flush=True)
            guest_count.value += 1
            party_count.value += 1
        # Otherwise join the party
        else:
            guest_count.value += 1
        # Get out of the doorway
        doorway.release()

        # P A R T Y   H A R D
        guest_partying(id)

        # Go to doorway after partying
        doorway.acquire()
        # If we are the last partier, close up the room
        if guest_count.value == 1:
            guest_count.value  -= 1
            print(STOPPING_PARTY_MESSAGE, flush=True)
            room_key.release()
        # Otherwise just leave
        else:
            guest_count.value -= 1
        
        doorway.release()
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    pass

def main():
    # Start time of the running of the program. 
    # start_time = time.time()

    # TODO - add any variables, data structures, processes you need
    staff = []
    guests = []

    room_key = mp.Lock()
    doorway = mp.Lock()
    guest_count = mp.Value('i', 0)
    party_count = mp.Value('i', 0)
    cleaned_count = mp.Value('i', 0)
    room_key, doorway, guest_count, party_count
    # TODO - add any arguments to cleaner() and guest() that you need
    
    # Hire some cleaners
    for i in range(CLEANING_STAFF):
        staff.append(mp.Process(target=cleaner, args=(i, room_key, cleaned_count)))

    # Invite guests into the hotel motel holiday inn
    for i in range(HOTEL_GUESTS):
        guests.append(mp.Process(target=guest, args=(i, room_key, doorway, guest_count, party_count)))

    # Start and finish the stay
    for p in staff:
        p.start()
    
    for p in guests:
        p.start()
    
    for p in staff:
        p.join()
    
    for p in guests:
        p.join()


    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()

