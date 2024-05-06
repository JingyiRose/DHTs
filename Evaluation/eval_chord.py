import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from Framework.controller_v2 import *

from Chord.chord6 import *




def eval_chord(folder_name, label):
    start_filename =  os.getcwd() + "/{}/init_{}.txt".format(folder_name, label)
    normal_ops_filename =  os.getcwd() + "/{}/normal_ops_{}.txt".format(folder_name, label)
    rep_filename = os.getcwd() + "/output_chord/reply_{}.txt".format(label)
    L = 12
    dht = Chord6(L, is_cheating = False)
    controller = ControllerV2(start_filename, normal_ops_filename, dht, rep_filename, makenode_sleep=0)
    controller.execute()
    # test_hard(start_filename, normal_ops_filename, rep_filename, m = L)


if __name__ == "__main__":
    # folder_name = "Evaluation1"
    # label = "n100"
    # eval_chord(folder_name, label)

    # folder_name = "Evaluation2"
    # label = "p_insert_050"
    # eval_chord(folder_name, label)

    # folder_name = "Evaluation3"
    # label = "p_nodejoin_01"
    # eval_chord(folder_name, label)

    folder_name = "Evaluation6"
    label = "lookup_insert_nodejoin_b80"
    eval_chord(folder_name, label)

    

    

# def test_hard(start_filename, normal_ops_filename, rep_filename, L):
#     # t = time sleep after new nodes are made -- this is for debugging purpose. set t=0 to turns it off.
#     t=5
#     dht = Chord6(L, is_cheating = False)
#     controller = ControllerV2(start_filename, normal_ops_filename, dht, rep_filename, makenode_sleep=t)
#     controller.execute()
#     time.sleep(60)
#     for id in dht.nodes:
#         node = dht.nodes[id]
#         print("Node={}\npos={}\nsuccessor={}\npredecessor={}\nstatus={}".format(node.node_id, node.pos_on_ring, node.successor, node.predecessor, node.active))
#         print(node.finger)
#         print(node.keyvals)
#         print("==============================================================================")      


# if __name__ == "__main__":

#     num_start_nodes = 9
#     num_start_keys = 10
#     num_ops = 112
#     p_nodejoin = 0
#     p_insertkey = 0
#     p_lookups = 1
#     start_filename = "init.txt"
#     normal_ops_filename = "normal_ops.txt"
#     rep_filename = "reply.txt"
#     stable_start = True
#     l = 12

#     maketest_v2(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
#                 start_filename, normal_ops_filename, node_id_length = l, node_ip_length = 12, 
#                 node_port_length = 5, key_length = l, key_base= 2, val_length = 16, stable_start=stable_start)

#     test_hard(start_filename, normal_ops_filename, rep_filename, m = l)