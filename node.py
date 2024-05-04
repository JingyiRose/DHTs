import threading
from env import *
import math

class Node:

    def __init__(self, node_id, ip_address, port, dht):
        self.node_id = node_id 
        self.ip_address = ip_address
        self.port = port
        self.in_channels = {} # key = id of node that self has a channel with, val  = channel instance
        self.out_channels = {} # key = id of node that self has a channel with, val  = channel instance
        self.dht = dht
        self.in_queue = [] # FIFO queue of RPCs going into this node
        self.is_done = False

        # self.alive = True
        # self.ongoing_requests = {}
        # self.req_to_filfill = {}
        # self.pkg_pointers = {}


        def thread_function(node):
            while not node.is_done:
                if len(node.in_queue) > 0:
                    pkg = node.in_queue.pop(0)
                    node.process(pkg)
            return

        # make each node its own thead (running forever, as long as packages (i.e. RPCs) remained, pop and process it)
        thr = threading.Thread(target=thread_function, args=(self,)) 
        thr.start()


    def send(self, pkg):
        # RPCs from peer to peer by this node sending a package (request, reply, etc) into a channel
        receiver_id = pkg.receiver.node_id
        if receiver_id not in self.out_channels:
            self.open_channel(receiver_id)
        channel = self.out_channels[receiver_id]
        channel.process(pkg)
        return
    
    
    def shut_down(self):
        self.is_done = True


    def dies(self):
        self.alive = False
    
    def finish(self):
        self.is_done = True

    def open_channel(self, destination):
        # destionation is id
        self.dht.MakeChannel(self.node_id, destination)
