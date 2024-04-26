from env import *
from command import *
from distributions import *
from node import *
from channel import *

class DHT:

    def __init__(self):
        self.nodes = {}
        self.channels = []
    
    def process(self, command):
        # process command from controller

        if command.type == "DHTInsertKey":
            key, val = command.key, command.val
            self.InsertKey(key, val)
            print("key made: {}, {}".format(key,val))
        
        if command.type == "DHTMakeNode":
            id, ip, port = command.id, command.ip, command.port
            self.MakeNode(id, ip, port)
    
        if command.type == "Finish":
            return
        

    # def DHTMakeKey(self, key, val):
    #     # create a key and its val (not necessary a node)
    #     return
    
    # def DHTMakeNode(self, key, val):
    #     node = Node(key, val, self)
    #     self.nodes[key] = node


    def MakeChannel(self, from_node_id, to_node_id, latency_dist = Gaussian(250, 10)):
        from_node = self.nodes[from_node_id]
        to_node = self.nodes[to_node_id]
        c1 = Channel(from_node, to_node, latency_dist)
        c2 = Channel(to_node, from_node, latency_dist)
        self.channels.append(c1)
        self.channels.append(c2)
        c1.activate()
        c2.activate()

    # def clean_up(self):
    #     for node in self.nodes.values():
    #         node.shut_down()
    

    # def NodeLookUp(self, lookup_id, req_node_id, dest_key):
    #     start_node = self.nodes[req_node_id]
    #     start_node.LookUp(lookup_id, dest_key)
    #     return
    
    # def kill_node(self, node):
    #     node.dies()
    #     return


# class Chord(DHT):
#     # fill out codes for MakeKey, Makenode, LookUp
#     def __init__(self):
#         super().__init__()

#     def LookUp(self, lookup_id, dest_key):
#         # generate a package and send through proper channel
#         # add package to self.ongoing_requests
#         return

# class DANode(Node):
#         node = Node(key, val)
#         for (node1_id, node1) in self.nodes.items():
#             c_out = Channel(node, node1, Gaussian(35, 5))
#             c_in = Channel(node1, node, Gaussian(37, 5))
#             node.out_channels[node1.id] = c_out
#             node.in_channels[node1.id] = c_in
#             node1.in_channels[node.id] = c_out
#             node1.out_channels[node.id] = c_in
#         self.nodes[key] = node


#         def thread_function(node):
#             while not node.is_done:
#                 if len(node.in_q) > 0:
#                     # x is either 1) client-requested LookUp for other nodes, or 2) peer-requested lookup
#                     x = node.in_q.pop(0)
#                     node.process(x)
#             return

#         thr = threading.Thread(target=thread_function, args=(node,))
#         thr.start()

# class Kademlia(DHT):
#     # fill out codes for MakeKey, Makenode, LookUp
#     def __init__(self):
#         super().__init__()
    
