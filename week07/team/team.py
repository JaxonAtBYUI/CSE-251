"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 05 Team Activity

Instructions:

- Make a copy of your assignment 2 program.  Since you are working in a team,
  you can design which assignment 2 program that you will use for the team
  activity.
- Convert the program to use a process pool and use apply_async() with a
  callback function to retrieve data from the Star Wars website.

"""


from concurrent.futures import process
from datetime import datetime, timedelta
from tkinter import TOP
from turtle import title
import multiprocessing as mp
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0
characters = []
planets = []
starships = []
vehicles = []
species = []
'planets', 'starships', 'vehicles', 'species'

# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    # Work smarter not harder, rip code from a previous assignment where you already solved the same problem.
    
    # Constructor
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.data = {}
        self.success = False
    
    # Behavior of the thread
    def run(self):
        # Get data from server
        req = requests.get(self.url)
        if req.status_code == 200:
            self.data = req.json()
            self.success = True
        else:
            print(f"\tFailure: {req.status_code}")

# TODO Add any functions you need here

# This is just for single calls
def get_url_data(url):
  global call_count
  thread = Request_thread(url)
  thread.start()
  call_count += 1
  thread.join()
  return thread.data



def get_url_data_with_key(url, key):
  # print(f'Getting from: {key} at {url}')
  global call_count
  thread = Request_thread(url)
  thread.start()
  call_count += 1
  thread.join()
  return (key, thread.data['name'])

def append_to_list(tuple):
  global characters
  global planets
  global starships
  global vehicles
  global species

  if tuple[0] == 'characters':
    characters.append(tuple[1])
  if tuple[0] == 'planets':
    planets.append(tuple[1])
  if tuple[0] == 'starships':
    starships.append(tuple[1])
  if tuple[0] == 'vehicles':
    vehicles.append(tuple[1])
  if tuple[0] == 'species':
    species.append(tuple[1])
  
# This is for batch creation
def create_thread(url):
  return Request_thread(url)

# This is for batch start
def start_thread(thread):
  global call_count
  thread.start()
  call_count += 1 

# This is for batch join
def join_thread(thread):
  thread.join()

# This is for extracting the names
def get_name(thread):
  return thread.data["name"]

# This is the print function
def print_info(info):
  
  global characters
  global planets
  global starships
  global vehicles
  global species

  # print(characters)
  # print(planets)
  # print(starships)
  # print(vehicles)
  # print(species)

  print("Title   :", info['title'])
  print("Director:", info['director'])
  print("Producer:", info['producer'])
  print("Released:", info['release'],'\n')

  print("Characters:", len(characters))
  print(", ".join(sorted(characters)), '\n')

  print("Planets:", len(planets))
  print(", ".join(sorted(planets)), '\n')

  print("Starships:", len(starships))
  print(", ".join(sorted(starships)), '\n')

  print("Vehicles:", len(vehicles))
  print(", ".join(sorted(vehicles)), '\n')

  print("Species:", len(species))
  print(", ".join(sorted(species)), '\n')



def main(process_count):
  log = Log(show_terminal=True)
  log.start_timer('Starting to retrieve data from the server')

  # TODO Retrieve Top API urls
  directory = get_url_data(TOP_API_URL)

  # TODO Retrieve Details on film 6
  film6 = get_url_data(directory["films"] + '6')
  
  # Set up the dictionary to be used for threads
  # I understand that I could probably just use the film6 json that comes through
  # but I had enough issues with this that this was a sanity choice. I'm writing
  # the final version of this at 4:04 in the morning.
  info = {
    'title': film6["title"],
    'director': film6["director"],
    'producer': film6["producer"],
    'release': film6["release_date"],
    'characters': film6["characters"],
    'planets': film6["planets"],
    'starships': film6["starships"],
    'vehicles': film6["vehicles"],
    'species': film6["species"]
  }

  # Create, start, and join all the threads.
  # Unfortunately it seems that map wasn't working. I feel like that would be prettier solution.
  processes = mp.Pool(process_count)
  keys = ['characters', 'planets', 'starships', 'vehicles', 'species']
  
  for key in keys:
    for i in range(len(info[key])):
      processes.apply_async(get_url_data_with_key, args=(info[key][i], key), callback=append_to_list)
  
  processes.close()
  processes.join()

  print_info(info)
  

  log.stop_timer('Total Time To complete')
  log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    for i in range(20):
      main(i+1)
