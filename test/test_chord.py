import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from Chord.chord import *
from Chord.chord_node import *
from controller_v2 import *
# from controller import *
import random
from Chord.chord2 import *
from Chord.chord3 import *
from Chord.chordbb import *
from Chord.chord4 import *

random.seed(1001)


# def test1():
#     controller = Controller(commandfile = "command_small.txt", dht = Chord(m = 30, is_cheating = True), 
#                             rep_filename = "chord_reply_small.txt", is_cheating = True)
#     controller.execute()

# def test2():
#     controller = Controller(commandfile = "command_small_contact.txt", dht = Chord(m = 30, is_cheating = False), 
#                             rep_filename = "chord_reply_small_contact.txt", is_cheating = False)
#     controller.execute()

# def test3():
#     dht = Chord(m = 5, is_cheating = False)
#     controller = Controller(commandfile = "command_5nodejoins.txt", dht = dht, 
#                             rep_filename = "chord_5nodejoins.txt", is_cheating = False)
#     controller.execute()
#     time.sleep(15)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print("==============================================================================")

# def test4():
#     dht = Chord(m = 30, is_cheating = False)
#     controller = Controller(commandfile = "command_20nodejoins.txt", dht = dht, 
#                             rep_filename = "chord_20nodejoins.txt", is_cheating = False)
#     controller.execute()
#     time.sleep(300)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print("==============================================================================")

# def test5():
#     dht = Chord(m = 6, is_cheating = False)
#     controller = Controller(commandfile = "command_keys_transfer_small.txt", dht = dht, 
#                             rep_filename = "keyval_keys_transfer_small.txt", is_cheating = False)
#     controller.execute()
#     time.sleep(15)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")

# def test6():
#     dht = Chord(m = 10, is_cheating = False)
#     controller = Controller(commandfile = "command_nodejoin_insert_keys_100.txt", dht = dht, 
#                             rep_filename = "keyval_keys_transfer_small.txt", is_cheating = False)
#     controller.execute()
#     time.sleep(30)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")

# def test7():
#     t = 4
#     dht = Chord3(m = 10, is_cheating = False)
#     controller = Controller(commandfile = "command_10nodejoins.txt", dht = dht, 
#                             rep_filename = "keyval_keys_transfer_small.txt", is_cheating = False, makenode_sleep = t)
#     controller.execute()
#     time.sleep(100)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")

# def test8():
#     t=20
#     dht = Chord2(m = 10, is_cheating = False)
#     controller = Controller(commandfile = "command_nodejoin_insert_keys_100.txt", dht = dht, 
#                             rep_filename = "keyval_keys_transfer_small.txt", is_cheating = False, makenode_sleep=t)
#     controller.execute()
#     time.sleep(300)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")


# def test9():
#     t=10
#     dht = Chord2(m = 10, is_cheating = False)
#     controller = Controller(commandfile = "command_keys_transfer_small.txt", dht = dht, 
#                             rep_filename = "keyval_keys_transfer_small.txt", is_cheating = False, makenode_sleep=t)
#     controller.execute()
#     time.sleep(30)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")

# def test10():
#     t=2
#     dht = Chord2(m = 10, is_cheating = False)
#     controller = Controller(commandfile = "command_keys_transfer_medium.txt", dht = dht, 
#                             rep_filename = "keyval_keys_transfer_small.txt", is_cheating = False, makenode_sleep=t)
#     controller.execute()
#     time.sleep(100)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")

# def test_c5h20():
#     t=2
#     cold_file = "cold5.txt"
#     hot_file = "hot20.txt"
#     filename = "empty.txt"
#     dht = Chord3(m = 10, is_cheating = False)
#     controller = ControllerColdHot(cold_file, hot_file, dht, rep_filename = filename, 
#                                    is_cheating = False, makenode_sleep=5)
#     controller.execute()
#     time.sleep(30)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")       

# def test_c20h500():
#     t=2
#     cold_file = "cold20.txt"
#     hot_file = "hot500.txt"
#     filename = "empty.txt"
#     dht = Chord3(m = 10, is_cheating = False)
#     controller = ControllerColdHot(cold_file, hot_file, dht, rep_filename = filename, 
#                                    is_cheating = False, makenode_sleep=t)
#     controller.execute()
#     time.sleep(180)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")       

# def test_coldhot(cold, hot, m):
#     t=2
#     cold_file = "cold{}.txt".format(cold)
#     hot_file = "hot{}.txt".format(hot)
#     rep_filename = "empty.txt"
#     dht = Chord4(m, is_cheating = False)
#     controller = ControllerColdHot(cold_file, hot_file, dht, rep_filename, 
#                                    is_cheating = False, makenode_sleep=t)
#     controller.execute()
#     time.sleep(120)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")      


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

