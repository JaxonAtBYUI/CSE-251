"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: Jaxon Hamm

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 50000
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

            # Display the car that has just be created in the terminal
            self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, cars_available, available_spaces, car_queue, log):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        threading.Thread.__init__(self)
        self.cars_available = cars_available
        self.available_spaces = available_spaces
        self.car_queue = car_queue
        self.log = log


    def run(self):
        for i in range(CARS_TO_PRODUCE):
            # Go put a car on the queue
            new_car = Car()
            self.available_spaces.acquire()
            self.car_queue.put(new_car)
            self.log.write("FACTORY: New vehicle added")
            self.cars_available.release()

        # signal the dealer that there there are not more cars
        self.available_spaces.acquire()
        self.car_queue.put("NO MORE CARS")
        self.log.write("FACTORY: No more vehicles")
        self.cars_available.release()


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, cars_available, available_spaces, car_queue, log, queue_stats):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        threading.Thread.__init__(self)
        self.cars_available = cars_available
        self.available_spaces = available_spaces
        self.car_queue = car_queue
        self.log = log
        self.queue_stats = queue_stats

    def run(self):
        while True:
            # TODO Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            self.cars_available.acquire()
            queue_size = self.car_queue.size()
            car = self.car_queue.get()
            self.available_spaces.release()

            if car == "NO MORE CARS":
                self.log.write("DEALER: No more vehicles to sell.")
                break

            self.queue_stats[queue_size - 1] += 1
            
            self.log.write("DEALER: New vechicle sold.")
            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    cars_available = threading.Semaphore(0)
    available_spaces = threading.Semaphore(10)
    
    # TODO Create queue251
    car_queue = Queue251()

    # TODO Create lock(s) ?
    #       N O O O O O O O O O O O

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    threads = []

    # TODO create your one factory
    threads.append(Factory(cars_available, available_spaces, car_queue, log))

    # TODO create your one dealership
    threads.append(Dealer(cars_available, available_spaces, car_queue, log, queue_stats))

    log.start_timer()

    # TODO Start factory and dealership
    [thread.start() for thread in threads]

    # TODO Wait for factory and dealership to complete
    [thread.join() for thread in threads]

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
