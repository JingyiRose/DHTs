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

random.seed(1001)


def test_hard(cold_filename, hot_filename, m):
    # t = time sleep after new nodes are made -- this is for debugging purpose. set t=0 to turns it off.
    t=2
    rep_filename = "empty.txt"
    dht = Chord4(m, is_cheating = False)
    controller = ControllerColdHot(cold_filename, hot_filename, dht, rep_filename, 
                                   is_cheating = False, makenode_sleep=t)
    controller.execute()
    time.sleep(300)
    for id in dht.nodes:
        node = dht.nodes[id]
        print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
        print(node.finger)
        print(node.keyvals)
        print("==============================================================================")      


if __name__ == "__main__":
    # (cold,hot) = (3,11) (5,20) (6,40) (10,100) (20,500)
    # test_coldhot(6, 40, m = 10)
    cold_filename = "cold_n5_k10.txt"
    hot_filename = "hot30.txt"
    test_hard(cold_filename, hot_filename, m=12)

