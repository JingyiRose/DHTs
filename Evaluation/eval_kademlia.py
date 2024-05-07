import sys
import os
from Framework.k_controller import *
from Framework.test_k import *



def eval_kademlia(folder_name, label, continue_from_init = False):
    dir = os.getcwd() + "/Evaluation"
    start_filename =  dir + "/{}/init_{}.txt".format(folder_name, label)
    normal_ops_filename =  dir + "/{}/normal_ops_{}.txt".format(folder_name, label)
    rep_filename = dir + "/output_kademlia/{}/reply_{}.txt".format(folder_name, label)
    save_init_filename = dir + "/output_kademlia/{}/save_init_state_{}.pkl".format(folder_name, label)
    save_final_filename = dir + "/output_kademlia/{}/save_final_state_{}.pkl".format(folder_name,label)
    key_length = 12 #key_length


    if continue_from_init:
        continue_ops_from_state(save_init_filename, normal_ops_filename, rep_filename, save_final_filename)
    else:
        test_two_phase(start_filename, normal_ops_filename, rep_filename, key_length, save_init_filename, save_final_filename)



if __name__ == "__main__":
    # folder_name = "Evaluation1"
    # label = "n20"
    # eval_kademlia(folder_name, label, continue_from_init=True)

    # folder_name = "Evaluation2"
    # label = "p_insert_050"
    # eval_kademlia(folder_name, label)

    # folder_name = "Evaluation3"
    # label = "p_nodejoin_02"
    # eval_kademlia(folder_name, label, continue_from_init=True)

    # folder_name = "Evaluation4"
    # label = "b_80"
    # eval_kademlia(folder_name, label)

    # folder_name = "Evaluation5"
    # label = "lookup_insert_b80"
    # eval_kademlia(folder_name, label)

    folder_name = "Evaluation6"
    label = "lookup_insert_nodejoin_b80"
    eval_kademlia(folder_name, label, True)

    

    

# def test_hard(start_filename, normal_ops_filename, rep_filename, L):
#     # t = time sleep after new nodes are made -- this is for debugging purpose. set t=0 to turns it off.
#     t=5
#     dht = kademlia6(L, is_cheating = False)
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