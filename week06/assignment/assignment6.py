"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Jaxon Hamm
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.

I believe that all requirements have been fullfilled as specified in the assignment.
Because of this I feel that this assignment falls under category 4.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *
from matplotlib import colors

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'

class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, connection, marble_count, delay):
        mp.Process.__init__(self)
        self.connection = connection
        self.marble_count = marble_count
        self.delay = delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        
        random.seed()
        # Create random marble and send it away
        for i in range(self.marble_count):
            marble = self.colors[random.randint(0, len(self.colors) - 1)]
            self.connection.send(marble)
            time.sleep(self.delay)

        
        # Send end message and close the pipe.
        self.connection.send(None)
        self.connection.close()

class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, from_conn, to_conn, marble_count, bags, delay):
        mp.Process.__init__(self)
        self.from_conn = from_conn
        self.to_conn = to_conn
        self.bag_size = int(marble_count / bags) + (marble_count % bags > 0) # This is rounding up the number.
        self.delay = delay


    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''

        # Our initial bag
        bag = Bag()

        while True:
            # Get marble and see if we still need to run.
            marble = self.from_conn.recv()
            if marble == None:
                break
    
            bag.add(marble)

            # If the bag is full (or somehow more than full) send the bag through the pipe
            # and get a new bag.
            if bag.get_size() >= self.bag_size:
                self.to_conn.send(bag)
                bag = Bag()

            # Its not totally clear where we are supposed to sleep here.
            # Do we only sleep when we send something to the wrapper, or every loop?
            time.sleep(self.delay)

        # Send over final bag, let the wrapper know, and clean up.
        self.from_conn.close()
        self.to_conn.send(bag)
        self.to_conn.send(None)
        self.to_conn.close()

class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, from_conn, to_conn, delay):
        mp.Process.__init__(self)
        self.from_conn = from_conn
        self.to_conn = to_conn
        self.delay = delay

    def run(self):
        random.seed()
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            # Get bag from pipe and see if we are still running or not.
            bag = self.from_conn.recv()
            if bag == None:
                break

            # Create a large Marble
            rand = random.randint(0, len(self.marble_names) - 1)
            large_marble = self.marble_names[rand]

            # Package into gift
            gift = Gift(large_marble, bag)

            # Send on pipe
            self.to_conn.send(gift)

            # Delay
            time.sleep(self.delay)

        # Clean up
        self.from_conn.close()
        self.to_conn.send(None)
        self.to_conn.close()

class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, from_conn, filename, delay, count):
        mp.Process.__init__(self)
        self.from_conn = from_conn
        self.filename = filename
        self.delay = delay
        self.count = count

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.filename, 'w') as f:
            
            while True:
                gift = self.from_conn.recv()
                if gift == None:
                    break
                
                self.count.value += 1
                f.write(f'Created - {datetime.now().time()}: {gift}\n')
                time.sleep(self.delay)

            self.from_conn.close()

def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')

def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    marble_in, marble_out = mp.Pipe()
    bag_in, bag_out = mp.Pipe()
    gift_in, gift_out = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    # Do we not need the Value to keep the count?
    count = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    processes = []
    processes.append(Marble_Creator(marble_in, settings[MARBLE_COUNT], settings[CREATOR_DELAY]))
    processes.append(Bagger(marble_out, bag_in, settings[MARBLE_COUNT], settings[BAG_COUNT], settings[BAGGER_DELAY]))
    processes.append(Assembler(bag_out, gift_in, settings[ASSEMBLER_DELAY]))
    processes.append(Wrapper(gift_out, BOXES_FILENAME, settings[WRAPPER_DELAY], count))

    log.write('Starting the processes')
    # TODO add code here
    for p in processes:
        p.start()

    log.write('Waiting for processes to finish')
    # TODO add code 
    for p in processes:
        p.join()

    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.
    log.write(f'Total Gifts Created: {count.value}')



if __name__ == '__main__':
    main()

