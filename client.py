from helper import *
from env import *
import os


class Client:

    def __init__(self, local_node, key, write_to = None):
        self.local_node = local_node
        self.query_key = key
        self.lookup_id = get_random_digits(8)
        self.req_complete = False
        self.in_queue = []
        self.client_id = get_random_string(8)
        # self.write_to = write_to[:-4] + str(self.client_id) + write_to[-4:]
        self.write_to = write_to

    
    def make_query(self):
        req = ClientRequest(self, self.local_node,
                            content = "Look-up key={}".format(self.query_key), id = self.lookup_id)
        req.send()
    
    def insert_data(self, key, value):
        req = PutRequest(self, self.local_node, content = "Insert key={} value={}".format(key, value), id = self.lookup_id)
        req.send()


    def wake(self):
        rep = self.in_queue.pop(0)
        self.req_complete = True
        # print("Query {} key = {} = value {}".format(self.lookup_id, self.query, rep.content[-10:]))
        val = rep.content.split(" ")[-1]
        if self.write_to:
            f = open(self.write_to, 'a')
            f.write("Query {} key = {} = value {}\n".format(self.lookup_id, self.query_key, val))
            f.close()


