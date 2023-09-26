'''Note: To run this program first open this file directory in the command prompt and then type
"python Typing_speed.py" '''

import curses
from curses import wrapper
'''This wrapper will allow us to initialize the curses module cuz when we initialize the module 
what will happen is that it's going to take over the terminal and allow to run some different commands on it'''

import time     #This will time how long you've been typing for.
import random

'''STD stands for standard output and scr is screen. STD is the terminal where we write stuff. 
And what wrapper module does it is that it kind of take that over and give you a screen over top of it that allows
us to write stuff to the screen.'''

def start_screen(stdscr):
    #clearing the entire screen to remove the preexisting stuff
    stdscr.clear()

    #adding text to the screen
    stdscr.addstr("Welcome to the Typing Speed Test!")
    stdscr.addstr("\nPress any key to start")

    #refreshing the screen
    stdscr.refresh()

    #This will wait for the user to type something so that way it doesn't immediately show this and close the screen
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0,f"WPM: {wpm}")
    for i, char in enumerate(current):
        correct_char=target[i]
        color=curses.color_pair(1)
        if char != correct_char:
            color=curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


#Returning different test text to check your speed.
def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip() #Each line has \n at the end to remove this we are using .strip()
    

#Storing and printing the target text on to the screen
def wpm_test(stdscr):
    target_text=load_text()
    current_text=[]
    wpm=0
    start_time=time.time()
    stdscr.nodelay(True)    #if no key is entered the wpm will decrease.


    while True:   #To overlay the text we write over the pre-written text
        time_elapsed = max(time.time()-start_time, 1)  #if anything is less than 1, it will give 1.
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)  #assuming average words have 5 chars

        stdscr.clear()
        display_text(stdscr, target_text, current_text,wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:

            key=stdscr.getkey()     #if the user doesn't enter a key this will throw an exception, to counter 
                                    #this we use try and except
        except:
            continue

        if ord(key) == 27:  #if we press escape key it will break the loop
            break

#When we hit backspace it will delete the character "\b", "x7f" and "KEY_BACKSPACE" is used for backspacing
#in different operating systems.
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

         
'''
#If we run this code we'd have to press any key two times to run the code
        stdscr.clear()
        stdscr.addstr(target_text)

        #Displaying the current text
        for char in current_text:
            stdscr.addstr(char,curses.color_pair(1))
        
        stdscr.refresh() '''



def main(stdscr):

    #styling
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:     #This will run the program again if you wish to play more.
        wpm_test(stdscr)
        stdscr.addstr(2,0, "You've completed the test. Press any key to continue...")
        key=stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)