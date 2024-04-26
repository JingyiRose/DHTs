import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from Clique.clique import *
from Clique.clique_node import *
from controller import *



controller = Controller(commandfile = "command_small.txt", dht = Clique(), rep_filename = "clique_reply_small.txt")
controller.execute()

