"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
from tkinter import TOP
from turtle import title
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


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
  print("Title   :", info['title'])
  print("Director:", info['director'])
  print("Producer:", info['producer'])
  print("Released:", info['release'],'\n')

  print("Characters:", len(info['characters']))
  print(", ".join(info['characters']), '\n')

  print("Planets:", len(info['planets']))
  print(", ".join(info['planets']), '\n')

  print("Starships:", len(info['starships']))
  print(", ".join(info['starships']), '\n')

  print("Vehicles:", len(info['vehicles']))
  print(", ".join(info['vehicles']), '\n')

  print("Species:", len(info['species']))
  print(", ".join(info['species']), '\n')



def main():
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
  keys = ['characters', 'planets', 'starships', 'vehicles', 'species']
  for key in keys:
    for i in range(len(info[key])):
      info[key][i] = create_thread(info[key][i])
  
  for key in keys:
    for i in range(len(info[key])):
      start_thread(info[key][i])
  

  for key in keys:
    for i in range(len(info[key])):
      join_thread(info[key][i])

  for key in keys:
    for i in range(len(info[key])):
      info[key][i] = get_name(info[key][i])

  print_info(info)

  log.stop_timer('Total Time To complete')
  log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
