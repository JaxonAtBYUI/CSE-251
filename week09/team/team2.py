"""
Course: CSE 251
Lesson Week: 09
File: team2.py

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

- This is the same problem as last team activity.  However, you will implement a waiter.  
  When a philosopher wants to eat, it will ask the waiter if it can.  If the waiter 
  indicates that a philosopher can eat, the philosopher will pick up each fork and eat.  
  There must not be a issue picking up the two forks since the waiter is in control of 
  the forks and when philosophers eat.  When a philosopher is finished eating, it will 
  informs the waiter that he/she is finished.  If the waiter indicates to a philosopher
  that they can not eat, the philosopher will wait between 1 to 3 seconds and try again.

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- When a philosopher is not eating, it will think for 3 to 5 seconds.
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
import threading
import random

PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5
DELAY = 1
TIMES_TO_EAT = 5

PHILOSPHER_NAMES = ["Pythagoras", "Confucius ","Heracleitus ","Parmenides ","Zeno of Elea ","Socrates ","Democritus ","Plato ","Aristotle ","Mencius ","Zhuangzi ","Pyrrhon of Elis ","Epicurus ","Zeno of Citium ","Philo Judaeus ","Marcus Aurelius ","Nagarjuna ","Plotinus ","Sextus Empiricus ","Saint Augustine ","Hypatia ","Anicius Manlius Severinus Boethius ","Śaṅkara ","Yaqūb ibn Ishāq aṣ-Ṣabāḥ al-Kindī ","Al-Fārābī ","Avicenna ","Rāmānuja ","Ibn Gabirol ","Saint Anselm of Canterbury ","al-Ghazālī ","Peter Abelard ","Averroës ","Zhu Xi ","Moses Maimonides ","Ibn al-'Arabī ","Shinran ","Saint Thomas Aquinas ","John Duns Scotus ","William of Ockham ","Niccolò Machiavelli ","Wang Yangming ","Francis Bacon, Viscount Saint Alban (or Albans), Baron of Verulam ","Thomas Hobbes ","René Descartes ","John Locke ","Benedict de Spinoza ","Gottfried Wilhelm Leibniz ","Giambattista Vico ","George Berkeley ","Charles-Louis de Secondat, baron de La Brède et de Montesquieu ","David Hume ","Jean-Jacques Rousseau ","Immanuel Kant ","Moses Mendelssohn ","Marie-Jean-Antoine-Nicolas de Caritat, marquis de Condorcet ","Jeremy Bentham ","Georg Wilhelm Friedrich Hegel ","Arthur Schopenhauer ","Auguste Comte ","John Stuart Mill ","Søren Kierkegaard ","Karl Marx ","Herbert Spencer ","Wilhelm Dilthey ","William James ","Friedrich Nietzsche ","Friedrich Ludwig Gottlob Frege ","Edmund Husserl ","Henri Bergson ","John Dewey ","Alfred North Whitehead ","Benedetto Croce ","Nishida Kitarō ","Bertrand Russell ","G.E. Moore ","Martin Buber ","Ludwig Wittgenstein ","Martin Heidegger ","Rudolf Carnap ","Sir Karl Popper ","Theodor Wiesengrund Adorno ","Jean-Paul Sartre ","Hannah Arendt ","Simone de Beauvoir ","Willard Van Orman Quine ","Sir A.J. Ayer ","Wilfrid Sellars ","John Rawls ","Thomas S. Kuhn ","Michel Foucault ","Noam Chomsky ","Jürgeb Gabernas ","Sir Bernard Williams ","Jacques Derrida ","Richard Rorty ","Robert Nozick ","Saul Kripke ","David Kellogg Lewis ","Peter"]

class Philosopher(threading.Thread):
    # Initialize the philosopher
    def __init__(self, name, id, lock_meals, left, right):
        threading.Thread.__init__(self)
        self.id = id
        self.lock_meals = lock_meals
        self.left = left
        self.right = right
        self.name = name

    def run(self):
        global meals
        done = False
        while not done:
            if meals > TIMES_TO_EAT:
                done = True
                continue
            if self.watier.can_eat(self.id):
                self.dining()
                with self.lock:
                    meals += 1
                self.waiter.finished_eating(self.id)
                self.thinking()
            else:
                time.sleep(random.uniform(1, 3) / 10)
    
    def dining(self):
        print ("Philosopher", self.name, " starts to eat.")
        time.sleep(random.uniform(1, 3) / DELAY)
        print ("Philosopher", self.id, " finishes eating and leaves to think.")


def main():
    # TODO - create the waiter (A class would be best here)
    # TODO - create the forks
    # TODO - create PHILOSOPHERS philosophers
    # TODO - Start them eating and thinking
    # TODO - Display how many times each philosopher ate
    pass

if __name__ == '__main__':
    main()