"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
from nturl2path import url2pathname
from operator import truediv
import threading
from urllib.request import Request
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    
    # Constructor
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.data = {}
    
    # Behavior of the thread
    def run(self):
        # Get data from server
        promise = requests.get(self.url)

        # Check for success code in response.
        if promise.status_code == 200:
            self.data = promise.json()
        else:
            print(f"\tFailure: {promise.status_code}")


class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        res = Request_thread(f"http://deckofcardsapi.com/api/deck/{deck_id}/shuffle/")
        res.start()
        res.join()

    def draw_card(self):
        # Put in the request to draw the card.
        draw = Request_thread(f"http://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1")
        draw.start()
        draw.join()

        # Check to see if that card is valid
        if draw.data == {}:
            return 'ERROR'
        
        # Set the remaining cards and the card value
        self.remaining = draw.data["remaining"]
        return draw.data["cards"][0]["code"]

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'ftehn41j7v27'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

