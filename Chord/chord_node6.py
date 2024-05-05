from node import *
import math
import threading
import time
from Chord.chord_env import *
import random


def is_in_between(x,l,r,m):
    # is l < x <= r in mod m?
    return (x-l-1) % m + (r-x) % m == (r-l-1) % m


class ChordNode6(Node):
    def __init__(self, node_id, ip_address, port, contact_node, dht, pos, coldstart=False):
        super().__init__(node_id, ip_address, port, dht)
        self.keyvals = {}
        self.alive = True
        self.ongoing_requests = {}
        self.req_to_fulfill = {}
        self.contact_node = contact_node
        self.pkg_pointers = {}
        self.pos_on_ring = pos
        self.keyspace_size = self.dht.keyspace_size
        self.num_identifier_bits = dht.num_identifier_bits
        self.finger = {}
        self.successor = None
        self.successor_pos = None
        self.predecessor = None
        self.predecessor_pos = None
        self.stabilization_queue = []
        self.init_queue = []
        self.is_stabilizing = True
        self.normal_queue = []
        self.active = (contact_node == "None")
        self.waiting = False
        self.coldstart = (contact_node == "None")
        self.stabilizer = not (contact_node == "None")
        self.lock = threading.Lock()
        self.clients = {}
        self.lookup_queue = []
        self.put_queue = []
        self.release_lookups = True
        self.keys_queue = []
        for i in range(self.num_identifier_bits):
            if contact_node == "None":
                self.finger[(self.pos_on_ring + 2 ** i) % self.keyspace_size] = node_id
                self.successor = self.node_id
                self.successor_pos = self.pos_on_ring
                self.predecessor = self.node_id
                self.predecessor_pos = self.pos_on_ring
            else:    
                self.finger[(self.pos_on_ring + 2 ** i) % self.keyspace_size] = None 


        def thread_function(node):
            clock = time.time()
            while not node.is_done:
                if  self.stabilizer and time.time()-clock > 30:
                    node.stabilize()
                    # print("Node {} shortcut stabilize".format(self.node_id))
                    node.fix_finger()
                    # print("Node {} fixing finger".format(self.node_id))
                    node.keys_request()
                    clock = time.time()
                if len(node.in_queue) > 0:
                    pkg = node.in_queue.pop(0)
                    if pkg.type.startswith("Init") and pkg.initiator == node.node_id:
                        node.init_queue.append(pkg)
                    elif pkg.type.startswith("Stab") and pkg.initiator == node.node_id:
                        node.init_queue.append(pkg)
                    elif pkg.type.startswith("PUT"):
                        node.put_queue.append(pkg)
                    elif pkg.type.startswith("Keys"):
                        node.keys_queue.append(pkg)
                    else:
                        node.normal_queue.append(pkg)
                else:
                    if node.active == False:
                        if len(node.init_queue) > 0:
                            pkg = node.init_queue.pop(0)
                            node.process(pkg)
                    elif node.active == True:
                        if len(node.init_queue) > 0:
                            pkg = node.init_queue.pop(0)
                            self.process(pkg)
                        elif len(node.keys_queue) > 0:
                            pkg = node.keys_queue.pop(0)
                            node.process(pkg)
                        elif len(node.put_queue) > 0:
                            pkg = node.put_queue.pop(0)
                            node.process(pkg)
                        elif len(node.normal_queue) > 0:
                            pkg = node.normal_queue.pop(0)
                            node.process(pkg)
                        
            return

        # make each node its own thead (running forever, as long as packages (i.e. RPCs) remained, pop and process it)
        thr = threading.Thread(target=thread_function, args=(self,)) 
        thr.start()

    def notify_client(self, client, content):
        client.get(content)

    def process(self, pkg):
        if pkg.type.startswith("Init"):
            self.process_init(pkg)
        if pkg.type.startswith("Stab"):
            self.process_stab(pkg)
        if pkg.type.startswith("Finger"):
            self.process_finger(pkg)
        if pkg.type.startswith("Keys"):
            self.process_key(pkg)
        if pkg.type.startswith("GET"):
            self.process_client(pkg)
        if pkg.type.startswith("LookUp"):
            self.process_lookup(pkg)
        if pkg.type.startswith("PUT"):
            self.process_put(pkg)

    def update_successor(self, successor_id, successor_pos):
        self.successor = successor_id
        self.successor_pos = successor_pos

    def update_predecessor(self, predecessor_id, predecessor_pos):
        self.predecessor = predecessor_id
        self.predecessor_pos = predecessor_pos

    def find_next_node_id(self, x):
        # x could be anything in chord ring value (not even have to me mod 2^m)
        next_node_id = None
        smallest_dist = self.keyspace_size
        for y in self.finger:
            if self.finger[y]:
                new_dist = (x-y) % self.keyspace_size
                if new_dist < smallest_dist:
                    smallest_dist = new_dist
                    next_node_id = self.finger[y]
        if not next_node_id:
            # print("no good node found")
            # print(self.node_id)
            # print(self.finger)
            next_node_id = self.successor
        # else:
        #     print("good node found")
        return next_node_id
    
    def fix_finger(self):
        print("Node {} fixing finger".format(self.node_id))
        if self.is_finger_ready():
            for finger in self.finger:
                if random.random() < 1:
                    content = "find-successor pos={}".format(finger)
                    next_node = self.finger[random.choice(list(self.finger.keys()))]
                    req = FingerRequest(self.node_id, next_node, content, initiator = self.node_id)
                    self.send(req)


    def is_finger_ready(self):
        for pos in self.finger:
            if self.finger[pos] == None:
                return False
        return True
    
    def store(self, key, val):
        self.lock.acquire()
        self.keyvals[key] = val
        self.release_lookups = True
        self.lock.release()

    def initialize(self):
        # find successor node
        if not self.successor:
            print("Initializing Node {}".format(self.node_id))
            content = "find successor={}".format(self.pos_on_ring)
            req = InitSuccessorRequest(self.node_id, self.contact_node, content, initiator = self.node_id)
            self.send(req)
            # print("Node {} successor request sent to {}".format(self.node_id, self.contact_node))
        return
    
    def init_predecessor(self):
        # ask successor who is his current predecessor. successor upon receiving change his predecessor to self
        content = "who is your predecessor"
        req = InitSuccessorRequest(self.node_id, self.successor, content, initiator = self.node_id)
        self.send(req)
    def init_fingers(self):
        # print("Node {} request fingers from successor node {}".format(self.node_id, self.successor))
        for finger in self.finger:
            content = "find successor for finger={}".format(finger)
            req = InitSuccessorRequest(self.node_id, self.contact_node, content, initiator = self.node_id)
            self.send(req)

    def init_finger_update(self):
        print("Node {} initiating finger_update".format(self.node_id))
        for i in range(self.num_identifier_bits):
            maxpos = (self.pos_on_ring - 2**i) % self.keyspace_size
            next_node = self.predecessor # can be better
            content = "I might be your finger i={} node={} pos={} maxpos={}".format(i, self.node_id, self.pos_on_ring, maxpos)
            update = InitFingerUpdate(self.node_id, next_node, content, initiator = self.node_id) 
            # print("Node {} sent finger update for i={} to {}".format(self.node_id, i, self.predecessor))
            self.send(update)

    def keys_request(self):
        if self.successor:
            content = "send me your keys before pos={}".format(self.pos_on_ring)
            req = KeysRequest(self.node_id, self.successor, content, initiator=self.node_id)
            self.send(req)

    def stabilize(self):
        if self.successor:
            print("Stabilizing Node {}".format(self.node_id))
            content = "who is your predecessor node={} pos={}".format(self.node_id, self.pos_on_ring)
            req = StabRequest(self.node_id, self.successor, content, initiator = self.node_id)
            self.send(req)
    
    def process_client(self, pkg):
        if pkg.type == "GET":
            # print("Client request received at node {} id = {} content={}".format(self.node_id, pkg.id, pkg.content))
            print(pkg.content)
            query_key = pkg.content.split("=")[-1][:-1]
            if query_key in self.keyvals:
                content = "val={} hops={}".format(self.keyvals[query_key], 0)
                self.notify_client(pkg.client, content)

                print("Client reply sent!")
            else:
                if not self.active:
                    self.normal_queue.append(pkg)
                else:
                    self.req_to_fulfill[pkg.id] = pkg
                    lookup_pos = self.dht.hash_fn(int(query_key)) % self.keyspace_size
                    next_node_id = self.find_next_node_id(lookup_pos)
                    client = pkg.client
                    req = LookUpRequest(self.node_id, next_node_id , content = pkg.content[:-1], initiator=self.node_id, client_id = client.client_id, num_hops=0, proximity = "local", id = None)
                    self.pkg_pointers[req.id] = pkg.id
                    self.ongoing_requests[req.id] = req
                    self.send(req)
                    self.clients[client.client_id] = client
                    # print("client req {} for key={} pos={} relayed to node {}".format(req.content, query_key, lookup_pos, next_node_id))

    def process_put(self, pkg):
        # if pkg.type == "PUTByNode":
        #     print("Node {} processing PUTByNode content={}".format(self.node_id, pkg.content))
        val = pkg.content.split("=")[-1]
        key = pkg.content.split("=")[-2].split(" ")[0]
        if is_in_between(self.dht.hash_fn(key), self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
            self.store(key, val)
            print("Node {} stores ({},{})".format(self.node_id, key, val))
        
        else:
            next_node_id = self.successor
            put = PutByNode(self.node_id, next_node_id, pkg.content)
            self.send(put)
            # print("Node {} ships ({},{}) to {}".format(self.node_id, key, val, self.successor))


            

            # print("Node {} receives an InsertKey".format(self.node_id))
        #     print("Client request received at node {} id = {}".format(self.node_id, pkg.id))
        #     query_key = int(pkg.content.split("=")[-1])
        #     if query_key in self.keyvals:
        #         content = "val={}".format(self.keyvals[query_key])
        #         self.notify_client(pkg.client, content)

        #         print("Client reply sent!")
        #     else:
        #         if not self.active:
        #             self.normal_queue.append(pkg)
        #         else:
        #             self.req_to_fulfill[pkg.id] = pkg
        #             lookup_pos = self.dht.hash_fn(int(query_key)) % self.keyspace_size
        #             next_node_id = self.find_next_node_id(lookup_pos)
        #             req = LookUpRequest(self.node_id, next_node_id , content = pkg.content, initiator=self.node_id, client_req_id = pkg.id, proximity = "local", id = None)
        #             self.pkg_pointers[req.id] = pkg.id
        #             self.ongoing_requests[req.id] = req
        #             self.send(req)
        #             print("client req for key={} pos={} relayed to node {}".format(query_key, lookup_pos, next_node_id))

    def process_lookup(self, pkg):
        if pkg.type == "LookUpRequest":
            query_key = int(pkg.content.split("=")[-1])
            query_pos = self.dht.hash_fn(int(query_key)) % self.keyspace_size
            if is_in_between(query_pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
                # print("key={} pos={} should be at this node".format(query_key, query_pos))
                if str(query_key) in self.keyvals:
                    content = "val={}".format(self.keyvals[str(query_key)])
                    rep = LookUpReply(self.node_id, pkg.sender, pkg.id, content, pkg.initiator, client_id = pkg.client_id, num_hops = pkg.num_hops+1)
                    self.send(rep)
                    print("Client look-up request found!")
                else:
                    print("Node {} circulating request for query {} bc pos={} pred={} lookup={}".format(self.node_id, query_key, self.pos_on_ring, self.predecessor_pos, query_pos))
                    self.normal_queue.append(pkg)
                    time.sleep(5)
            else:
                next_node_id = self.find_next_node_id(query_pos)
                req = LookUpRequest(self.node_id, next_node_id, pkg.content, pkg.initiator, client_id = pkg.client_id, num_hops = pkg.num_hops+1)
                self.req_to_fulfill[pkg.id] = pkg
                self.pkg_pointers[req.id] = pkg.id
                self.send(req)
                # print("client req for key={} pos={} not found at\nnode={} pos={} keyvals={}\nrequest relayed to node={}".format(query_key, query_pos, self.node_id, self.pos_on_ring, self.keyvals, next_node_id))

        if pkg.type == "LookUpReply":
            prev_id = self.pkg_pointers[pkg.req_id]
            prev_req = self.req_to_fulfill[prev_id]
            if pkg.initiator == self.node_id:
                print("LookUpReply made it back to local node!")
                client = self.clients[pkg.client_id]
                new_content = pkg.content + " num_hops={}".format(pkg.num_hops)
                self.notify_client(client, new_content)
            else:
                rep = LookUpReply(self.node_id, prev_req.sender, prev_req.id, pkg.content, initiator=pkg.initiator, client_id = pkg.client_id, num_hops = pkg.num_hops)
                self.send(rep)



    def process_stab(self, pkg):
        if pkg.type == "StabRequest":
            if pkg.content.startswith("who is your predecessor"):
                content = "my predecessor={} pos={}".format(self.predecessor, self.predecessor_pos)
                rep = StabReply(self.node_id, pkg.sender, pkg.id, content, initiator=pkg.initiator)
                self.send(rep)

                tentative_predecessor_pos = int(pkg.content.split("=")[-1])
                tentative_predecessor = pkg.content.split("=")[-2].split(" ")[0]
                if (self.successor == self.node_id) and (self.predecessor == self.node_id):
                    self.update_predecessor(tentative_predecessor, tentative_predecessor_pos)
                    self.update_successor(tentative_predecessor, tentative_predecessor_pos)
                    # print("Node {} successor updated to {} pos={}".format(self.node_id, tentative_predecessor, tentative_predecessor_pos))
                    # print("Node {} predecessor updated to {} pos={}".format(self.node_id, tentative_predecessor, tentative_predecessor_pos))
                if is_in_between(tentative_predecessor_pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
                    print("Node {} predecessor updated to {} pos={}".format(self.node_id, tentative_predecessor, tentative_predecessor_pos))
                    self.update_predecessor(tentative_predecessor, tentative_predecessor_pos)
                
            
        if pkg.type == "StabReply":
            # print("StabReply Node {} from {} content={}".format(self.node_id, pkg.sender, pkg.content))
            reply_node_pos = int(pkg.content.split("=")[-1])
            reply_node = pkg.content.split("=")[-2].split(" ")[0]
            # print(pkg.content)
            if reply_node != self.node_id:
                if is_in_between(reply_node_pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
                    self.update_predecessor(reply_node, reply_node_pos)
                    print("Node {} pos={} predecessor updated to {} pos={}".format(self.node_id, self.pos_on_ring, reply_node, reply_node_pos))
                if is_in_between(reply_node_pos, self.pos_on_ring-1, self.successor_pos, self.keyspace_size):
                    self.update_successor(reply_node, reply_node_pos)
                    print("Node {} pos={} successor updated to {} pos={}".format(self.node_id, self.pos_on_ring, reply_node, reply_node_pos))


    def process_key(self, pkg):
        if pkg.type == "KeysRequest":
            requestor_pos = int(pkg.content.split("=")[-1])
            keys_to_send = []
            # keys = list(self.keyvals.keys())
            self.lock.acquire()
            for (key,val) in self.keyvals.items():
                if is_in_between(requestor_pos, self.dht.hash_fn(int(key))-1, self.pos_on_ring, self.keyspace_size):
                    keys_to_send.append(key)
                    val = self.keyvals[key]
                    content = "you should add key={} val={}".format(key, val)
                    rep = KeysReply(self.node_id, pkg.sender, content, initiator=pkg.initiator)
                    self.send(rep)
                    print("KEY SENT! ({},{}) sent from {} to {}".format(key, val, self.node_id, pkg.sender))

                
            for key in keys_to_send:
                del self.keyvals[key]
               
            self.lock.release()

        if pkg.type == "KeysReply":
            val = pkg.content.split("=")[-1]
            key = int(pkg.content.split("=")[-2].split(" ")[0])
            print("Node {} storing (key,val)=({},{})".format(self.node_id, key,val))
            self.store(key,val)
            
        
    
    def process_init(self, pkg):

        if pkg.type == "InitFingerUpdate":
            maxpos = int(pkg.content.split("=")[-1])
            node_pos = int(pkg.content.split("=")[-2].split(" ")[0])
            node_id = pkg.content.split("=")[-3].split(" ")[0]
            if node_id == self.node_id:
                print("Dead update: circulated to")
                pass
            elif is_in_between(self.pos_on_ring, maxpos, node_pos, self.keyspace_size):
                next_node = self.predecessor # can be better
                update = InitFingerUpdate(self.node_id, next_node, pkg.content, initiator = self.node_id) 
                self.send(update)
            else:
                i = int(pkg.content.split("=")[-4].split(" ")[0])
                node_id = pkg.content.split("=")[-3].split(" ")[0]
                if not self.finger[(self.pos_on_ring + 2**i) % self.keyspace_size]:
                    self.finger[(self.pos_on_ring + 2**i) % self.keyspace_size] = node_id
                    next_node = self.predecessor # can be better
                    update = InitFingerUpdate(self.node_id, next_node, pkg.content, initiator = self.node_id) 
                    self.send(update)
                else:
                    finger_pos = self.dht.hash_fn(self.finger[(self.pos_on_ring + 2**i) % self.keyspace_size]) % self.keyspace_size
                    if is_in_between(node_pos, self.pos_on_ring + 2**i-1, finger_pos, self.keyspace_size):
                        # print("Finger i={} of node={} pos={} originally is node={} pos={} updated node={} pos={} and forwarded to {} at pos={}".format(i, self.node_id, self.pos_on_ring, 
                        #                                                                                                  self.finger[(self.pos_on_ring + 2**i) % self.keyspace_size], finger_pos,
                        #                                                                                                  node_id, node_pos, self.predecessor, self.predecessor_pos))
                        self.finger[(self.pos_on_ring + 2**i) % self.keyspace_size] = node_id
                        next_node = self.predecessor # can be better
                        update = InitFingerUpdate(self.node_id, next_node, pkg.content, initiator = self.node_id) 
                        self.send(update)
                      


        if pkg.type == "InitSuccessorRequest":
            if pkg.content.startswith("find successor="):
                pos = int(pkg.content.split("=")[-1])
                # print("ABOUT TO BE ERROR: {} {} {} {} {} {}".format(pos, self.predecessor_pos, self.pos_on_ring, self.node_id, pkg.initiator, self.active))
                if not self.active:
                    print("CIRCULATING")
                    self.normal_queue.append(pkg)
                elif is_in_between(pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
                    # print("Successor for {} pos={} found at node={} pos={} with prec={} pos={}"
                    #       .format(pkg.initiator, pos, self.node_id, self.pos_on_ring, self.predecessor, self.predecessor_pos))
                    content = "successor={} pos={} predecessor={} pos={}".format(self.node_id, self.pos_on_ring, self.predecessor, self.predecessor_pos)
                    rep = InitSuccessorReply(self.node_id, pkg.sender, pkg.id, content, initiator=pkg.initiator)
                    self.send(rep)
                else:
                    next_node_id = self.find_next_node_id(pos)
                    req = InitSuccessorRequest(self.node_id, next_node_id, pkg.content, initiator=pkg.initiator)
                    self.req_to_fulfill[pkg.id] = pkg
                    self.pkg_pointers[req.id] = pkg.id
                    self.send(req)

            if pkg.content.startswith("find successor for finger="):
                pos = int(pkg.content.split("=")[-1])
                if is_in_between(pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
                    content = "successor for finger={} is node={} pos={}".format(pos, self.node_id, self.pos_on_ring)
                    rep = InitSuccessorReply(self.node_id, pkg.sender, pkg.id, content, initiator=pkg.initiator)
                    self.send(rep)
                else:
                    next_node_id = self.find_next_node_id(pos)
                    req = InitSuccessorRequest(self.node_id, next_node_id, pkg.content, initiator=pkg.initiator)
                    self.req_to_fulfill[pkg.id] = pkg
                    self.pkg_pointers[req.id] = pkg.id
                    self.send(req)


        if pkg.type == "InitSuccessorReply":
            if pkg.content.startswith("successor="):
                if pkg.initiator == self.node_id:
                    successor_pos = int(pkg.content.split("=")[-3].split(" ")[0])
                    successor_id = pkg.content.split("=")[-4].split(" ")[0]
                    predecessor_pos = int(pkg.content.split("=")[-1])
                    predecessor_id = pkg.content.split("=")[-2].split(" ")[0]
                    self.update_successor(successor_id, successor_pos)
                    self.update_predecessor(predecessor_id, predecessor_pos)
                    if self.predecessor and self.successor:
                        self.active = True
                    else:
                        self.initialize()
                    self.init_fingers()
                    self.keys_request()
                    self.init_finger_update()
                else:
                    prev_id = self.pkg_pointers[pkg.req_id]
                    prev_req = self.req_to_fulfill[prev_id]
                    rep = InitSuccessorReply(self.node_id, prev_req.sender, prev_req.id, pkg.content, initiator=pkg.initiator)
                    self.send(rep)
            
            if pkg.content.startswith("successor for finger="):
                if pkg.initiator == self.node_id:
                    finger_pos = int(pkg.content.split("=")[-1])
                    finger_id = pkg.content.split("=")[-2].split(" ")[0]
                    f = int(pkg.content.split("=")[-3].split(" ")[0])
                    self.finger[f] = finger_id
                    print("Node {} finger {} initialized to {}".format(self.node_id, f, finger_id))
                    if self.is_finger_ready():
                        self.init_predecessor()

                else:
                    prev_id = self.pkg_pointers[pkg.req_id]
                    prev_req = self.req_to_fulfill[prev_id]
                    rep = InitSuccessorReply(self.node_id, prev_req.sender, prev_req.id, pkg.content, initiator=pkg.initiator)
                    self.send(rep)

    def process_finger(self, pkg):
        if pkg.type == "FingerRequest":
            pos = int(pkg.content.split("=")[-1])
            if is_in_between(pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
                # print("Node {} fixing finger {} to {} with pos={} predpos={}".format(pkg.initiator, pos, self.pos_on_ring, self.predecessor_pos))
                content = "finger={} node={}".format(pos, self.node_id)
                rep = FingerReply(self.node_id, pkg.sender, pkg.id, content, pkg.initiator)
                self.send(rep)
            else:
                next_node_id = self.find_next_node_id(pos)
                req = FingerRequest(self.node_id, next_node_id, pkg.content, initiator=pkg.initiator)
                self.req_to_fulfill[pkg.id] = pkg
                self.pkg_pointers[req.id] = pkg.id
                self.send(req)
        
        if pkg.type == "FingerReply":
            if pkg.initiator == self.node_id:
                node = pkg.content.split("=")[-1]
                finger = int(pkg.content.split("=")[-2].split(" ")[0])
                if node != self.finger[finger]:
                    print("Node {} finger {} fixed to {}".format(self.node_id, finger, node))
                self.finger[finger] = node
            else:
                prev_id = self.pkg_pointers[pkg.req_id]
                prev_req = self.req_to_fulfill[prev_id]
                rep = FingerReply(self.node_id, prev_req.sender, prev_req.id, pkg.content, initiator=pkg.initiator)
                self.send(rep)




