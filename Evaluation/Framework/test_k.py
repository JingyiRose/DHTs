import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from Evaluation.Framework.k_controller import *
from Evaluation.Framework.make_commands_v2 import *
from Kademlia.kademlia_dht import *



def save_init_state(start_filename, key_length, save_init_filename):
    dht = KademliaDHT(key_length)
    try:
        controller = KController(start_filename, None, dht, rep_filename)
        controller.execute_init()
        print(f'----------Init finished. Saving to file {save_init_filename}----------')
        dht.write_state_to_file(save_init_filename)
        dht.clean_up() # stop all threads
        print("----------Finish Clean Up and Save State ---------------")
        
    except Exception as e:
        print("----------Exception Occured ---------------")
        print(e.args)
        dht.clean_up()

def continue_ops_from_state(save_init_filename, normal_ops_filename, rep_filename, save_final_filename):
    try:
        dht = read_state_from_file(save_init_filename, True) # restart = True
        controller = KController(None, normal_ops_filename, dht, rep_filename)
        start_time = time.time()
        controller.execute_eval()
        while not dht.all_nodes_finished():
            time.sleep(3)
        end_time = time.time()
        time.sleep(10)
        print(f'----------All nodes finished in {end_time-start_time} seconds.----------')
        dht.write_state_to_file(save_final_filename)
        # dht.clean_up() # stop all threads
        print("----------Finish Clean Up ---------------")
    except Exception as e:
        print("----------Exception Occured ---------------")
        print(e.args)
        dht.clean_up()

def inspect_init_state(save_init_filename):
    dht = read_state_from_file(save_init_filename, False) # restart = False
    print("----------The saved DHT init state is ---------------")
    dht.get_global_view()
    print("----------Finish locading DHT init state ---------------")

def inspect_final_state(save_final_filename):
    dht = read_state_from_file(save_final_filename, False) # restart = False
    print("----------The saved DHT final state is ---------------")
    dht.get_global_view()
    print("----------Finish locading DHT final state ---------------")


"""Final Test File for Kademlia
"""

def test_two_phase(start_filename, normal_ops_filename, rep_filename, key_length, save_init_filename, save_final_filename):
    save_init_state(start_filename, key_length, save_init_filename)
    continue_ops_from_state(save_init_filename, normal_ops_filename, rep_filename, save_final_filename)

def test(start_filename, normal_ops_filename, rep_filename, key_length, save_final_filename):
    try:
        # node that key_lnegth is the number of bits in node_id and key
        dht = KademliaDHT(key_length)
        controller = KController(start_filename, normal_ops_filename, dht, rep_filename)
        controller.execute_all()
        while not dht.all_nodes_finished():
            time.sleep(3)
        print(f'----------All nodes finished for {normal_ops_filename} ops.----------')
        dht.write_state_to_file(save_final_filename)
        # dht.clean_up() # stop all threads
        print("----------Finish Clean Up ---------------")
    except Exception as e:
        print("----------Exception Occured ---------------")
        print(e.args)
        dht.clean_up()

def eval_1():
    return

def eval_2():
    return

def eval_3():
    return


if __name__ == "__main__":

    num_start_nodes = 50
    num_start_keys = 50
    num_ops = 50
    p_nodejoin = 0
    p_insertkey = 0
    p_lookups = 0.5
    start_filename = "k_small_init.txt"
    normal_ops_filename = "k_small_normal_ops.txt"
    rep_filename = "k_small_reply.txt"
    save_init_filename = "k_small_init_state.pkl"
    save_final_filename = "k_small_final_state.pkl"
    stable_start = True
    key_length = 10

    make_commands = False
    run_test = True
    continue_from_init = False

    if make_commands:
        maketest_v2(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                start_filename, normal_ops_filename, node_id_length = key_length, node_ip_length = 12, 
                node_port_length = 5, key_length = key_length, key_base= 2, val_length = 16, stable_start=stable_start)
    if run_test:
        if continue_from_init:
            continue_ops_from_state(save_init_filename, normal_ops_filename, rep_filename, save_final_filename)
        else:
            # test(start_filename, normal_ops_filename, rep_filename, key_length, save_final_filename)
            test_two_phase(start_filename, normal_ops_filename, rep_filename, key_length, save_init_filename, save_final_filename)

    # inspect_init_state(save_init_filename)
    # inspect_final_state(save_final_filename)