from helper import *
from env import *
import os


class Client:

    def __init__(self, local_node, query_key = None, keyval = None, write_to = None):
        self.local_node = local_node
        self.query_key = query_key # key that the client wants to look up in dht
        self.keyval = keyval # tuple (key, value) that the client wants to insert to dht
        self.req_complete = False
        self.in_queue = []
        self.client_id = get_random_string(8)
        # self.write_to = write_to[:-4] + str(self.client_id) + write_to[-4:]
        self.write_to = write_to

    
    def make_query(self):
        req = GetRequest(self, self.local_node,
                            content = "Look-up key={}\n".format(self.query_key))
        # print("Client of node {} sent a GetRequest {}".format(self.local_node.node_id, 
                # "Look-up key={}".format(self.query_key)))
        req.send()
    
    def insert_data(self):
        req = PutRequest(self, self.local_node, 
                         content = "Insert key={}, value={}\n".format(*self.keyval))
        print("Client of node {} sent a PutRequest {}".format(self.local_node.node_id, 
                "Insert key={}, value={}\n".format(*self.keyval)))
        req.send()


    def wake(self):
        rep = self.in_queue.pop(0)
        self.req_complete = True
        # print("Query {} key = {} = value {}".format(self.lookup_id, self.query, rep.content[-10:]))
        val = rep.content.split(" ")[-1]
        if self.write_to:
            f = open(self.write_to, 'a')
            f.write("Query {} key = {} = value {}\n".format(self.client_id, self.query_key, val))
            f.close()


