import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from Chord.chord import *
from Chord.chord_node import *
from framework_v2.controller_v2 import *
# from controller import *
import random
from Chord.chord2 import *
from Chord.chord3 import *
from Chord.chordbb import *
from Chord.chord4 import *
from make_commands_v2 import *



def test_hard(cold_filename, hot_filename, m):
    # t = time sleep after new nodes are made -- this is for debugging purpose. set t=0 to turns it off.
    t=5
    rep_filename = "empty.txt"
    dht = Chord4(m, is_cheating = False)
    controller = ControllerColdHot(cold_filename, hot_filename, dht, rep_filename, 
                                   is_cheating = False, makenode_sleep=t)
    controller.execute()
    time.sleep(60)
    for id in dht.nodes:
        node = dht.nodes[id]
        print("Node={}\npos={}\nsuccessor={}\npredecessor={}\nstatus={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor, node.active))
        print(node.finger)
        print(node.keyvals)
        print("==============================================================================")      


if __name__ == "__main__":


    # num_cold_nodes = 20
    # num_cold_keys = 100
    # cmd_length = 500
    # p_nodejoin = 0.03
    # p_insertkey = 0.37
    # p_lookups = 0.6

    num_cold_nodes = 10
    num_cold_keys = 20
    cmd_length = 100
    p_nodejoin = 0.08
    p_insertkey = 0.30
    p_lookups = 0.62
    cold_fname = "cold_n{}_k{}.txt".format(num_cold_nodes, num_cold_keys)
    hot_fname =  "hot{}.txt".format(cmd_length)
    keyvalfile = "empty.txt"
    maketest_hotcold(num_cold_nodes, num_cold_keys, cmd_length,  p_nodejoin, p_insertkey, p_lookups, 
                     cold_fname, hot_fname, keyvalfile, node_id_length = 8, node_ip_length = 12, 
                     node_port_length = 5, key_length = 8, val_length = 16, contact = False)
    test_hard(cold_fname, hot_fname, m=12)

