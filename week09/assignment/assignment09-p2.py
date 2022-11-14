"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Jaxon Hamm

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

Each thread would be in a threading class. This class would store its path
and whether it reached the end. Each class would check its children if
they had reached the end. If the child had reached the end then the two paths
would be compared, spliced to merge at the right position and then the class
would set itself to saying it had reached the end. This would back out building
the list out of segments until it was finally just output. I'm not entirely sure
if this would be the best but I feel like it would stop the copying of the same
path list hundreds of times, and hopefully keep memory usage down.

Why would it work?

Because it is effectively just backing out of a recursive function that had
multiple paths being checked at once. The path is assembled as the backing out
occurs.

Category: 4
This program meets the program requirements to the best of my knowledge.

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 600
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
thread_count_lock = threading.Lock()
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def _solve(maze, x, y, color, maze_lock):
    global thread_count
    global thread_count_lock
    # Check to see if we have a color. If not, get a color.
    # Just in case to make sure nothing breaks
    if color == None:
        color = get_color()

    # Check to see if we can move to the new square.
    # If we can move to the square, move to it.
    # Because we are checking if we can move to a square and moving there potentially
    # we need to acquire the lock to make sure that no other thread performs those operations
    # and moves there first.
    maze_lock.acquire()
    if maze.can_move_here(x, y):
        maze.move(x, y, color)
    maze_lock.release()

    # KILL THEM ALL if we're at the end.
    # I'm unsure if this is a critical section considering only one thread will
    # ever edit this.
    global stop
    if maze.at_end(x, y):
        stop = True
        return
    elif stop == True:
        return

    # Recur/Threading options
    threads = []
    moves = maze.get_possible_moves(x, y)
    for i in range(len(moves)):
        # Recur on the final move.
        if i == len(moves) - 1:
            _solve(maze, moves[i][0], moves[i][1], color, maze_lock)
        # Otherwise new thread created
        else:
            thread = threading.Thread(target=_solve, args=(maze, moves[i][0], moves[i][1], get_color(), maze_lock))
            # Add to the thread count
            thread_count_lock.acquire()
            thread_count += 1
            thread_count_lock.release()
            
            # Start the thread and append it
            thread.start()
            threads.append(thread)

    # If we hit the end and can't recur, wait until all children are done
    # before killing them all and exiting.
    for t in threads:
        t.join()

def solve_find_end(maze):
    maze_lock = threading.Lock()
    global stop
    global thread_count
    thread_count = 0
    stop = False

    
    # Get the process going
    start = maze.get_start_pos()
    _solve(maze, start[0], start[1], get_color(), maze_lock)


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()