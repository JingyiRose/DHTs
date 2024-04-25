from node import *
import math
class ChordNode(Node):
    def __init__(self, node_id, ip_address, port, dht, pos, finger = None):
        super().__init__(node_id, ip_address, port, dht)
        self.keyvals = {}
        # print("node made: {}".format(self.node_id))
        self.alive = True
        self.ongoing_requests = {}
        self.req_to_fulfill = {}
        # self.in_queue = []
        # self.is_done = False
        self.pkg_pointers = {}
        self.pos_on_ring = pos
        if finger == None:
            self.finger = {}
        else:
            self.finger = finger
        self.keyspace_size = self.dht.keyspace_size

    def store(self, key, val):
        self.keyvals[key] = val


    def find_next_node_id(self, x):
        # x could be anything in chord ring value (not even have to me mod 2^m)
        next_node_id = None
        smallest_dist = self.keyspace_size
        for y in self.finger:
            new_dist = (x-y) % self.keyspace_size
            if new_dist < smallest_dist:
                smallest_dist = new_dist
                next_node_id = self.finger[y]
        return next_node_id


    def process(self, pkg):
        # need to specify how each node handles various type of packages
        if pkg.type == "ClientRequest":
            query_key = pkg.content.split("=")[-1]
            if query_key in self.keyvals:
                rep = ClientReply(self, pkg.client, content = "Value is {}".format(self.keyvals[query_key]), 
                                  proximity="local",  id = None)
                rep.send()
                print("key found immediately")
                print("client request fulfilled")
            else:
                self.req_to_fulfill[pkg.id] = pkg
                next_node_id = self.find_next_node_id(int(query_key))
                req = Request(self.node_id, next_node_id , content = pkg.content, proximity = "local", id = None)
                self.pkg_pointers[req.id] = pkg.id
                self.ongoing_requests[req.id] = req
                self.send(req)
                print("client request made and sent to next node")


        if pkg.type == "REQ":
            query_key = pkg.content.split("=")[-1]
            if query_key in self.keyvals:
                rep = Reply(self.node_id, pkg.sender, pkg.id, content = "val={}".format(self.keyvals[query_key]), proximity="p2p")
                self.send(rep)
                print("key found and started sending back: {}, {}".format(query_key, self.keyvals[query_key]))
            else:
                self.req_to_fulfill[pkg.id] = pkg
                next_node_id = self.find_next_node_id(int(query_key))
                req = Request(self.node_id, next_node_id , content = pkg.content, proximity = "p2p", id = None)
                self.pkg_pointers[req.id] = pkg.id
                self.ongoing_requests[req.id] = req
                self.send(req)
                print("Node {}: peer request for {} forwarded to next node {}".format(self.node_id, query_key, next_node_id))
                print(self.keyvals)
                print("================================")
        if pkg.type == "REP":
            prev_id = self.pkg_pointers[pkg.req_id]
            prev_req = self.req_to_fulfill[prev_id]
            if prev_req.type == "REQ":
                rep = Reply(self.node_id, prev_req.sender, prev_req.id, content = pkg.content, proximity="p2p",  id = None)
                self.send(rep)
                print("relaying rep")
            if prev_req.type == "ClientRequest":
                val = pkg.content.split("=")[-1]
                rep = ClientReply(self, prev_req.client, content = "Value is {}".format(val),proximity="local",  id = None)
                rep.send()
                print("client request fulfilled")
                    # del self.req_to_fulfill[prev_id]
                    # del self.pkg_pointers[pkg.req_id]

        #     if prev_req.type == "REQ":
        #         pass

