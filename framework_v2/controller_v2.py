
from client import *
from command_v2 import *
import time

class ControllerColdHot:
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

    def __init__(self, cold_file, hot_file, dht, rep_filename = None, is_cheating = False, makenode_sleep=0):
        # turning on "cheat" (by setting it to true) lets dht calls self.cheat() after all keys/nodes are inserted 

        self.cold_cmds = parse_commands(cold_file)
        self.hot_cmds = parse_commands(hot_file)
        self.clients = []
        self.dht = dht
        # self.length_log = len(self.cmds)
        if rep_filename and os.path.exists(rep_filename):
            os.remove(rep_filename)
        self.rep_filename = rep_filename

        self.is_cheating = is_cheating
        self.lookup_started = False
        self.makenode_sleep = makenode_sleep
        
    
    def execute(self):
        for cmd in self.cold_cmds:
            if cmd.type == "MakeNode":
                id, ip, port, contact_node = cmd.id, cmd.ip, cmd.port, cmd.contact_node
                self.dht.MakeNode(id, ip, port, contact_node)

            if cmd.type == "InsertKey":
                key, val = cmd.key, cmd.val
                self.dht.InsertKey(key, val)

        # this function stabliizes cold nodes and keys
        self.dht.stabilize_cold_files()

        time.sleep(10)
        

        # this is where the actual simulation/evaluation begins
        for cmd in self.hot_cmds:
            if cmd.type == "InsertKey":
                key, val = cmd.key, cmd.val
                self.dht.InsertKey(key, val)
                time.sleep(0.5)

            if cmd.type == "MakeNode":
                id, ip, port, contact_node = cmd.id, cmd.ip, cmd.port, cmd.contact_node
                self.dht.MakeNode(id, ip, port, contact_node)
                time.sleep(self.makenode_sleep)

            if cmd.type == "ClientLookUp":
                local_node = self.dht.nodes[cmd.local_node_id]
                query_key = cmd.destination_key
                client = Client(local_node, query_key, write_to = self.rep_filename)
                client.make_query()
                print("Client of node {} made a query".format(cmd.local_node_id))
                self.clients.append(client)