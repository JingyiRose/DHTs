
from client import *
from Framework.command_v2 import *
import time

class ControllerV2:
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

    def __init__(self, start_file, normal_ops_file, dht, rep_filename = None, makenode_sleep=0):
        # turning on "cheat" (by setting it to true) lets dht calls self.cheat() after all keys/nodes are inserted 

        self.start_cmds = parse_commands(start_file)
        self.normal_ops_cmds = parse_commands(normal_ops_file)
        self.clients = []
        self.dht = dht
        if rep_filename and os.path.exists(rep_filename):
            os.remove(rep_filename)
        self.rep_filename = rep_filename

        self.lookup_started = False
        self.makenode_sleep = makenode_sleep
        
    
    def execute(self):

        # the first phase is to initialize dht and stabilize it
        for cmd in self.start_cmds:
            if cmd.type == "MakeNode":
                id, ip, port = cmd.id, cmd.ip, cmd.port
                self.dht.MakeNode(id, ip, port, make_contact = False)

            if cmd.type == "ClientInsertKey":
                local_node_id, key, val = cmd.local_node_id, cmd.key, cmd.val
                if local_node_id == "None":
                    self.dht.InsertKey(key, val)

        # this function stabliizes cold nodes and keys
        self.dht.stabilize_cold_files()

        # time.sleep(2)
        

        # this is where the actual simulation/evaluation begins
        for cmd in self.normal_ops_cmds:
            if cmd.type == "ClientInsertKey":
                local_node_id, key, val = cmd.local_node_id, cmd.key, cmd.val

                if local_node_id == "None":
                    self.dht.InsertKey(key, val)
                else:
                    local_node = self.dht.nodes[cmd.local_node_id]
                    client = Client(local_node, keyval=(key,val))
                    client.insert_data()


            if cmd.type == "MakeNode":
                id, ip, port = cmd.id, cmd.ip, cmd.port
                self.dht.MakeNode(id, ip, port, make_contact = True)
                time.sleep(self.makenode_sleep)

            if cmd.type == "ClientLookUp":
                local_node = self.dht.nodes[cmd.local_node_id]
                query_key = cmd.destination_key
                client = Client(local_node, query_key, write_to = self.rep_filename)
                client.make_query()
                print("Client of node {} made a query".format(cmd.local_node_id))
                self.clients.append(client)