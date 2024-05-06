from Framework.make_commands_v2 import *    
import random 
import os

random.seed(1005)


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
    # 50 starting nodes, 250g starting keys
    # evaluation on 500 normal ops with p_insertkey = 0.25, p_nodejoin = {0.002, 0.01, 0.02}

    L = 12
    num_start_nodes = 50
    num_start_keys = 250
    num_ops = 500
    p_nodejoin = 0
    p_insertkey = 0.25
    p_lookups = 0.75
    stable_start = True
    for p_nodejoin_str in ["002", "01", "02"]:
        p_nodejoin = float(int(p_nodejoin_str)/10**(len(p_nodejoin_str)))
        start_filename = os.getcwd() + "/Evaluation3/init_p_nodejoin_{}.txt".format(p_nodejoin_str)
        normal_ops_filename = os.getcwd() + "/Evaluation3/normal_ops_p_nodejoin_{}.txt".format(p_nodejoin_str)
        stable_start = True
        maketest_v2(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                    start_filename, normal_ops_filename, node_id_length = L, node_ip_length = 12, 
                    node_port_length = 5, key_length = L, key_base= 2, val_length = 16, stable_start=stable_start)
        
def gen_eval_lookups_only_left_bias():
    # 50 starting nodes, 250 starting keys
    # evaluation on 500 look-ups & left biases = {0.99, 0.95, 0.90, 0.80}

    L = 12
    num_start_nodes = 50
    num_start_keys = 250
    num_ops = 500
    p_nodejoin = 0
    p_insertkey = 0
    p_lookups = 1
    stable_start = True
    for b in ["99", "95", "90", "80"]:
        left_bias = float(int(b)/(10**len(b)))
        start_filename = os.getcwd() + "/Evaluation4/init_b{}.txt".format(b)
        normal_ops_filename = os.getcwd() + "/Evaluation4/normal_ops_b{}.txt".format(b)
        stable_start = True
        maketest_v2_biased(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                    start_filename, normal_ops_filename, node_id_length = L, node_ip_length = 12, 
                    node_port_length = 5, key_length = L, key_base= 2, val_length = 16, stable_start=stable_start, left_bias = left_bias)


def gen_eval_lookups_insert_left_bias():
    # 50 starting nodes, 250 starting keys
    # evaluation on 500 look-ups & p_insertkey = 0.5, p_lookup = 0.5, left biases = {0.99, 0.95, 0.90, 0.80}

    L = 12
    num_start_nodes = 50
    num_start_keys = 250
    num_ops = 500
    p_nodejoin = 0
    p_insertkey = 0.5
    p_lookups = 0.5
    stable_start = True
    for b in ["99", "95", "90", "80"]:
        left_bias = float(int(b)/(10**len(b)))
        start_filename = os.getcwd() + "/Evaluation5/init_lookup_insert_b{}.txt".format(b)
        normal_ops_filename = os.getcwd() + "/Evaluation5/normal_ops_lookup_insert_b{}.txt".format(b)
        stable_start = True
        maketest_v2_biased(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                    start_filename, normal_ops_filename, node_id_length = L, node_ip_length = 12, 
                    node_port_length = 5, key_length = L, key_base= 2, val_length = 16, stable_start=stable_start, left_bias = left_bias)
        

def gen_eval_lookups_insert_nodejoin_left_bias():
    # 50 starting nodes, 250 starting keys
    # evaluation on 500 look-ups & p_nodejoin = 0.01, p_insertkey = 0.25, p_lookup = 0.74, left biases = {0.99, 0.95, 0.90, 0.80}

    L = 12
    num_start_nodes = 50
    num_start_keys = 250
    num_ops = 500
    p_nodejoin = 0.01
    p_insertkey = 0.25
    p_lookups = 0.74
    stable_start = True
    for b in ["99", "95", "90", "80"]:
        left_bias = float(int(b)/(10**len(b)))
        start_filename = os.getcwd() + "/Evaluation6/init_lookup_insert_nodejoin_b{}.txt".format(b)
        normal_ops_filename = os.getcwd() + "/Evaluation6/normal_ops_lookup_insert_nodejoin_b{}.txt".format(b)
        stable_start = True
        maketest_v2_biased(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                    start_filename, normal_ops_filename, node_id_length = L, node_ip_length = 12, 
                    node_port_length = 5, key_length = L, key_base= 2, val_length = 16, stable_start=stable_start, left_bias = left_bias)

        

if __name__ == "__main__":
    pass
    # gen_eval_lookups_only()
    # gen_eval_lookup_insert()
    # gen_eval_lookup_insert_nodejoin()
    # gen_eval_lookups_only_left_bias()
    # gen_eval_lookups_insert_left_bias()
    # gen_eval_lookups_insert_nodejoin_left_bias()