from Framework.make_commands_v2 import *    
import random 
import os

random.seed(1003)


def gen_eval_lookups_only():
    # [20,50,100] starting nodes, 250 starting keys
    # evaluation on 500 look-ups

    L = 12
    num_start_nodes = None
    num_start_keys = 250
    num_ops = 500
    p_nodejoin = 0
    p_insertkey = 0
    p_lookups = 1
    stable_start = True
    for n in [20, 50, 100]:
        num_start_nodes = n
        start_filename = os.getcwd() + "/Evaluation1/init_n{}.txt".format(n)
        normal_ops_filename = os.getcwd() + "/Evaluation1/normal_ops_n{}.txt".format(n)
        stable_start = True
        maketest_v2(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                    start_filename, normal_ops_filename, node_id_length = L, node_ip_length = 12, 
                    node_port_length = 5, key_length = L, key_base= 2, val_length = 16, stable_start=stable_start)
        
def gen_eval_lookup_insert():
    # 50 starting nodes, 250 starting keys
    # evaluation on 500 normal ops with p_insertkey = {0.05, 0.1, 0.25, 0.5}

    L = 12
    num_start_nodes = 50
    num_start_keys = 250
    num_ops = 500
    p_nodejoin = 0
    p_insertkey = None
    p_lookups = 1
    stable_start = True
    for p_insert_str in ["005", "010", "025", "050"]:
        p_insertkey = float(int(p_insert_str)/100)
        start_filename = os.getcwd() + "/Evaluation2/init_p_insert_{}.txt".format(p_insert_str)
        normal_ops_filename = os.getcwd() + "/Evaluation2/normal_ops_p_insert_{}.txt".format(p_insert_str)
        stable_start = True
        maketest_v2(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                    start_filename, normal_ops_filename, node_id_length = L, node_ip_length = 12, 
                    node_port_length = 5, key_length = L, key_base= 2, val_length = 16, stable_start=stable_start)
        
def gen_eval_lookup_insert_nodejoin():
    # 50 starting nodes, 250 starting keys
    # evaluation on 500 normal ops with p_insertkey = 0.25, p_nodejoin = {0.002, 0.01, 0.02}

    L = 12
    num_start_nodes = 50
    num_start_keys = 250
    num_ops = 500
    p_nodejoin = 0
    p_insertkey = 0.25
    p_lookups = 1
    stable_start = True
    for p_nodejoin_str in ["002", "01", "02"]:
        p_nodejoin = float(int(p_nodejoin_str)/10**(len(p_nodejoin_str)))
        start_filename = os.getcwd() + "/Evaluation3/init_p_nodejoin_{}.txt".format(p_nodejoin_str)
        normal_ops_filename = os.getcwd() + "/Evaluation3/normal_ops_p_nodejoin_{}.txt".format(p_nodejoin_str)
        stable_start = True
        maketest_v2(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                    start_filename, normal_ops_filename, node_id_length = L, node_ip_length = 12, 
                    node_port_length = 5, key_length = L, key_base= 2, val_length = 16, stable_start=stable_start)
        

        

if __name__ == "__main__":
    gen_eval_lookups_only()
    gen_eval_lookup_insert()
    gen_eval_lookup_insert_nodejoin()