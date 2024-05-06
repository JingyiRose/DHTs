import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from Chord.chord import *
from Chord.chord_node import *
from Framework.controller_v2 import *
# from controller import *
import random
from Chord.chord5 import *
from Chord.chord6 import *
from Framework.make_commands_v2 import *



def test_hard(start_filename, normal_ops_filename, rep_filename, m):
    # t = time sleep after new nodes are made -- this is for debugging purpose. set t=0 to turns it off.
    t=5
    dht = Chord6(m, is_cheating = False)
    controller = ControllerV2(start_filename, normal_ops_filename, dht, rep_filename, makenode_sleep=t)
    controller.execute()
    time.sleep(120)
    for id in dht.nodes:
        node = dht.nodes[id]
        print("Node={}\npos={}\nsuccessor={}\npredecessor={}\nstatus={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor, node.active))
        print(node.finger)
        print(node.keyvals)
        print("==============================================================================")      


if __name__ == "__main__":


    # num_start_nodes = 4
    # num_start_keys = 10
    # num_ops = 20
    # p_nodejoin = 0
    # p_insertkey = 0.5
    # p_lookups = 0.5
    # start_filename = "init.txt"
    # normal_ops_filename = "normal_ops.txt"
    # rep_filename = "reply.txt"
    # stable_start = True
    # l = 10


    # num_start_nodes = 40
    # num_start_keys = 100
    # num_ops = 500
    # p_nodejoin = 0.02
    # p_insertkey = 0.28
    # p_lookups = 0.7
    # start_filename = "init.txt"
    # normal_ops_filename = "normal_ops.txt"
    # rep_filename = "reply.txt"
    # stable_start = True
    # l = 10

    num_start_nodes = 2
    num_start_keys = 0
    num_ops = 100
    p_nodejoin = 0.01
    p_insertkey = 0.99
    p_lookups = 0
    start_filename = "init.txt"
    normal_ops_filename = "normal_ops.txt"
    rep_filename = "reply.txt"
    stable_start = True
    l = 12

    maketest_v2(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                start_filename, normal_ops_filename, node_id_length = l, node_ip_length = 12, 
                node_port_length = 5, key_length = l, key_base= 2, val_length = 16, stable_start=stable_start)

    test_hard(start_filename, normal_ops_filename, rep_filename, m = l)