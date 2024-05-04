
from make_commands import *
from controller import *
from Kademlia.kademlia_dht import *

# make the commands and write to file
num_nodes = 5
num_keyvals = 10
num_lookups = 15
command_file = K_COMMAND_FILE
keyval_file = K_KEYVAL_FILE

maketest(num_keyvals, num_nodes, num_lookups, command_file, keyval_file)

# simulate a Kademlia DHT that processes the commands
controller = Controller(commandfile = command_file, dht = KademliaDHT(), 
                        rep_filename = "./kademlia_reply_small.txt")
controller.execute()