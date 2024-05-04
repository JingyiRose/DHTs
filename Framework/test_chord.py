import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from Chord.chord import *
from Chord.chord_node import *
from Framework.controller_v2 import *
# from controller import *
import random
from Chord.chord5 import *
from Framework.make_commands_v2 import *



def test_hard(start_filename, normal_ops_filename, m):
    # t = time sleep after new nodes are made -- this is for debugging purpose. set t=0 to turns it off.
    t=5
    rep_filename = "empty.txt"
    dht = Chord5(m, is_cheating = False)
    controller = ControllerV2(start_filename, normal_ops_filename, dht, rep_filename, makenode_sleep=t)
    controller.execute()
    time.sleep(5)
    for id in dht.nodes:
        node = dht.nodes[id]
        print("Node={}\npos={}\nsuccessor={}\npredecessor={}\nstatus={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor, node.active))
        print(node.finger)
        print(node.keyvals)
        print("==============================================================================")      


if __name__ == "__main__":


    num_start_nodes = 2
    num_start_keys = 10
    num_ops = 4
    p_nodejoin = 0.0
    p_insertkey = 1
    p_lookups = 0.0
    start_filename = "init.txt"
    normal_ops_filename = "normal_ops.txt"

    stable_start = True

    l = 8

    maketest_v2(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                start_filename, normal_ops_filename, node_id_length = l, node_ip_length = 12, 
                node_port_length = 5, key_length = l, key_base= 2, val_length = 16, stable_start=stable_start)

    test_hard(start_filename, normal_ops_filename, m = l)