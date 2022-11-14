"""
Course: CSE 251
Lesson Week: 09
File: team1.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks after you get it working for 5.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat
"""

import time
import random
import threading

PHILOSOPHERS = 5
TIMES_TO_EAT = PHILOSOPHERS * 5
DELAY = 1

# TODO - run program for 30 seconds instead of number of times eating

meal_count = 0

class Philosopher(threading.Thread):
 
    def __init__(self, id, lock_meals, left, right):
        threading.Thread.__init__(self)
        self.id = id
        self.left = left
        self.right = right
        self.lock_meals = lock_meals
 
    def run(self):
        global meal_count
        done = False
        while not done:
            with self.lock_meals:
                if meal_count >= TIMES_TO_EAT:
                    done = True
                    continue

            # try to eat
            self.left.acquire()
            if not self.right.acquire(blocking=False):
                # we can't grab the right fork, so let left go and try again
                self.left.release()
                self.left, self.right = self.right, self.left
                continue

            self.dining()

            with self.lock_meals:
                meal_count += 1

            self.left.release()
            self.right.release()

            self.thinking()

        pass

    def dining(self):
        print ("Philosopher", self.id, " starts to eat.")
        time.sleep(random.uniform(1, 3) / DELAY)
        print ("Philosopher", self.id, " finishes eating and leaves to think.")

    def thinking(self):
        time.sleep(random.uniform(1, 3) / DELAY)


def main():
    global meal_count

    meal_count = 0

    forks = [threading.Lock() for _ in range(PHILOSOPHERS)]

    lock_meals = threading.Lock()

    philosophers = [Philosopher(i, lock_meals, forks[i % PHILOSOPHERS], forks[(i + 1) % PHILOSOPHERS]) for i in range(PHILOSOPHERS)]
 
    for p in philosophers: 
        p.start()

    for p in philosophers: 
        p.join()

    print('All Done:', meal_count)


if __name__ == '__main__':
    main()