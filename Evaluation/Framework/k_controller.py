import sys, os
sys.path.insert(1, os.path.abspath(''))
# print(sys.path)
from client import *
from Kademlia.kademlia_dht import KademliaDHT
from Evaluation.Framework.command_v2 import *
import time

class KController:
    # controller = evaluation framework. It feeds a sequence of commands into DHTs. In ControllerColdHot, there are two phases
    # Phase 1:
    #   - initializing "cold" nodes and keys (i.e. hard-wiring them to dht) and "stabilize" the dht. After this phase, dht should be in stable states
    # Phase 2:
    #   - assuming the dht is in stable states, this is where the evaluation actually happens
    #   - commands in this phase include 
    #       1) node joins
    #           -> dht should handle node joins gracefully (i.e. in the case of chord, it needs to complete successor, predecessor, 
    #               initialize finger table, and correct other nodes' pointers, etc.)
    #       2) insert keys
    #           -> keys should be stored at a correct node             
    #       3) client look-ups
    #           -> client initiates a look-up request to its local node; then local node should fetch (key,value) and send them back to the client

    def __init__(self, start_file, normal_ops_file, dht: KademliaDHT, rep_filename = None):
        if start_file:
            self.start_cmds = parse_commands(start_file)
        if normal_ops_file:
            self.normal_ops_cmds = parse_commands(normal_ops_file)
        self.clients = []
        self.dht = dht
        if rep_filename and os.path.exists(rep_filename):
            os.remove(rep_filename)
        self.rep_filename = rep_filename

    def execute_init(self):
        # the first phase is to initialize dht and stabilize it
        for cmd in self.start_cmds:
            if cmd.type == "MakeNode":
                id, ip, port = cmd.id, cmd.ip, cmd.port
                self.dht.centralized_make_node(id, ip, port)

            if cmd.type == "ClientInsertKey":
                _, key, val = cmd.local_node_id, cmd.key, cmd.val
                self.dht.centralized_insert_key(key, val)
        self.dht.construct_routing_tables()
    
    def execute_eval(self):
        # this is where the actual simulation/evaluation begins
        for cmd in self.normal_ops_cmds:
            if cmd.type == "ClientInsertKey":
                local_node_id, key, val = cmd.local_node_id, cmd.key, cmd.val
                local_node = self.dht.nodes[local_node_id]
                client = Client(local_node, keyval=(key,val))
                client.insert_data()

            if cmd.type == "MakeNode":
                id, ip, port = cmd.id, cmd.ip, cmd.port
                self.dht.MakeNode(id, ip, port)
                time.sleep(self.makenode_sleep)

            if cmd.type == "ClientLookUp":
                local_node = self.dht.nodes[cmd.local_node_id]
                query_key = cmd.destination_key
                client = Client(local_node, query_key, write_to = self.rep_filename)
                client.make_query()
                if DEBUG:
                    print("Client of node {} made a query key={}".format(cmd.local_node_id, query_key))
                self.clients.append(client)


    def execute_all(self):
        self.execute_init()
        self.execute_eval()
        
