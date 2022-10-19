"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: Jaxon Hamm

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

I feel that I got a 4 becaust I completed the assignment and fullfilled the requirements
with the criteria given.

"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')

# Only use put and get
class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, cars_available, available_spaces, barrier, car_queue, factory_number, factory_count, dealer_count, log):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        threading.Thread.__init__(self)
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        self.cars_available = cars_available
        self.available_spaces = available_spaces
        self.car_queue = car_queue
        self.barrier = barrier
        self.factory_number = factory_number
        self.factory_count =  factory_count
        self.dealer_count = dealer_count
        self.log = log


    def run(self):
        for i in range(self.cars_to_produce):
            # Go put a car on the queue
            new_car = Car()
            self.available_spaces.acquire()
            self.car_queue.put(new_car)
            # self.log.write(f"{threading.get_ident()} FACTORY: New vehicle added")
            self.cars_available.release()

        # signal the dealer that there there are not more cars
        # self.log.write("FACTORY: No more vehicles")

        # TODO "Wake up/signal" the dealerships one more time.  Select one factory to do this
        self.barrier.wait()
        if self.factory_number == self.factory_count:
            for _ in range(self.dealer_count):
                self.available_spaces.acquire()
                self.car_queue.put("NO MORE CARS")
                self.cars_available.release()
            # self.log.write("FACTORY: All Dealers notified.")

class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, cars_available, available_spaces, car_queue, log):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        threading.Thread.__init__(self)
        self.cars_available = cars_available
        self.available_spaces = available_spaces
        self.car_queue = car_queue
        self.log = log
        self.sold = 0

    def run(self):
        while True:
            # TODO Add your code here
            self.cars_available.acquire()
            car = self.car_queue.get()
            self.available_spaces.release()

            if car == "NO MORE CARS":
                # self.log.write("DEALER: No more vehicles to sell.")
                break
            
            # self.log.write("DEALER: New vechicle sold.")
            self.sold += 1
            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))

def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    # TODO Create semaphore(s)
    cars_available = threading.Semaphore(0)
    available_spaces = threading.Semaphore(10)

    # TODO Create queue
    car_queue = Queue251()

    # TODO Create lock(s)
    # No locks this time around

    # TODO Create barrier(s)
    barrier = threading.Barrier(factory_count)

    # This is used to track the number of cars received by each dealer
    # dealer_stats = list([0] * dealer_count) This was breaking so i tried something else
    dealer_stats = []

    # TODO create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    # CARS_TO_CREATE_PER_FACTORY doesn't exist anywhere in this file
    # The closest thing is the random int set in the __init__ of the factories.
    factories = []
    for i in range(factory_count):
        factories.append(Factory(cars_available, available_spaces, barrier, car_queue, i + 1, factory_count, dealer_count, log))

    dealers = []
    # TODO create your dealerships
    for _ in range(dealer_count):
        dealers.append(Dealer(cars_available, available_spaces, car_queue, log))

    log.start_timer()

    # TODO Start all dealerships
    for d in dealers:
        d.start()

    time.sleep(1)   # make sure all dealers have time to start

    # TODO Start all factories
    for f in factories:
        f.start()

    # TODO Wait for factories and dealerships to complete
    for d in dealers:
        d.join()

    for f in factories:
        f.join()

    factory_stats = [f.cars_to_produce for f in factories]
    dealer_stats = [d.sold for d in dealers]

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats   : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)


