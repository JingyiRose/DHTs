
from make_commands import *
from controller import *
from Kademlia.kademlia_dht import *

start_new = True
execute_commands = True

def handle_termination(dht):
    dht.write_state_to_file(K_DHT_STATE)
    dht.clean_up() # stop all threads
    dht = read_state_from_file(K_DHT_STATE, False) # restart = False
    dht.get_global_view()

# simulate a Kademlia DHT that processes the commands
try:
    dht = None
    if start_new:
        # make the commands and write to file
        num_nodes = 20
        num_keyvals = 20
        num_lookups = 20
        command_file = K_COMMAND_FILE
        keyval_file = K_KEYVAL_FILE
        maketest(num_keyvals, num_nodes, num_lookups, command_file, keyval_file)
        dht = KademliaDHT()
    else:
        dht = read_state_from_file(K_DHT_STATE, execute_commands) # restart = True
        print("----------The saved DHT state is ---------------")
        dht.get_global_view()
        print("----------Finish locading DHT state ---------------")
    if execute_commands:
        start_time = time.time()
        controller = Controller(commandfile = command_file, dht = dht, 
                        rep_filename = "./kademlia_reply_small.txt")
        controller.execute()
        while not dht.all_nodes_finished():
            pass
        end_time = time.time()
        time.sleep(1)
        print(f'----------All nodes finished in {end_time-start_time} seconds. Saving to file----------')
        handle_termination(dht)
        print("----------Finish Clean Up and Save State ---------------")
except Exception as e:
    print(e.args)
    print("----------Exception Occured, Saving to File ---------------")
    handle_termination(dht)
    print("----------Finish Clean Up and Save State ---------------")

