import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from Chord.chord import *
from Chord.chord_node import *
from controller import *



controller = Controller(commandfile = "command_small.txt", dht = Chord(m = 30, is_cheating = True), 
                        rep_filename = "chord_reply_small.txt", is_cheating = True)
controller.execute()

