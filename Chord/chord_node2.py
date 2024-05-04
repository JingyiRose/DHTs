from node import *
import math
import threading
import time
from Chord.chord_env import *


def is_in_between(x,l,r,m):
    # is l < x <= r in mod m?
    return (x-l-1) % m + (r-x) % m == (r-l-1) % m


class ChordNode2(Node):
    def __init__(self, node_id, ip_address, port, contact_node, dht, pos, finger = None):
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
        self.tentative_successor = None
        self.tentative_successor_pos = None

        self.predecessor = None
        self.predecessor_pos = None
        self.tentative_predecessor = None
        self.tentative_predecessor_pos = None
        self.stabilization_queue = []
        self.init_queue = []
        self.is_stabilizing = True
        self.normal_queue = []
        self.active = (contact_node == "None")
        self.waiting = False

        for i in range(self.num_identifier_bits):
            if contact_node == "None":
                self.finger[(self.pos_on_ring + 2 ** i) % self.keyspace_size] = node_id
                self.successor = self.node_id
                self.successor_pos = self.pos_on_ring
                self.predecessor = self.node_id
                self.predecessor_pos = self.pos_on_ring
            else:    
                self.finger[(self.pos_on_ring + 2 ** i) % self.keyspace_size] = None 

        # def get_pos(x):
        #     return self.dht.hash_fn(int(x)) % self.keyspace_size
    

        def thread_function(node):
            while not node.is_done:
                i = 0
                if i % 50 == 49 and node.active:
                    node.stabilize()
                    print("Node {} shortcut stabilize".format(self.node_id))
                    i += 1
                if len(node.in_queue) > 0:
                    pkg = node.in_queue.pop(0)
                    if pkg.type.startswith("Init") and pkg.initiator == node.node_id:
                        node.init_queue.append(pkg)
                    else:
                        node.normal_queue.append(pkg)
                else:
                    if node.active == False:
                        if len(node.init_queue) > 0:
                            i += 1
                            pkg = node.init_queue.pop(0)
                            node.process_init(pkg)
                    elif node.active == True:
                        if len(node.normal_queue) > 0:
                            pkg = node.normal_queue.pop(0)
                            i += 1
                            # print("this line should print")
                            # print(pkg)
                            if pkg.type.startswith("Init"):
                                node.process_init(pkg)
                            if pkg.type.startswith("Keys"):
                                # print("this line should print: {}".format(pkg.content))
                                node.process_key(pkg)
                            if pkg.type.startswith("Stab"):
                                node.process_stab(pkg)

            return

        # make each node its own thead (running forever, as long as packages (i.e. RPCs) remained, pop and process it)
        thr = threading.Thread(target=thread_function, args=(self,)) 
        thr.start()

    
    
    def is_finger_ready(self):
        for pos in self.finger:
            if self.finger[pos] == None:
                return False
        return True
    
    def store(self, key, val):
        self.keyvals[key] = val

    def initialize(self):
        # find successor node
        if not self.successor:
            content = "find successor={}".format(self.pos_on_ring)
            req = InitSuccessorRequest(self.node_id, self.contact_node, content, initiator = self.node_id)
            self.send(req)
            print("Node {} successor request sent to {}".format(self.node_id, self.contact_node))



        # ask successor to fill up fingers


        # activate

        return
    
    def init_predecessor(self):
        # ask successor who is his current predecessor. successor upon receiving change his predecessor to self
        content = "who is your predecessor"
        req = InitSuccessorRequest(self.node_id, self.successor, content, initiator = self.node_id)
        self.send(req)

    def init_notify_successor(self):
        content = "I am your predecessor now id={} pos={}".format(self.node_id, self.pos_on_ring)
        ping = InitPing(self.node_id, self.successor, content, initiator = self.node_id)
        self.send(ping)
                    #         predecessor_id = pkg.sender
                    # predecessor_pos = pos
                    # self.update_predecessor(predecessor_id, predecessor_pos)

    def init_notify_pred(self):
        content = "I am your successor now id={} pos={}".format(self.node_id, self.pos_on_ring)
        ping = InitPing(self.node_id, self.predecessor, content, initiator = self.node_id)
        self.send(ping)



    def init_fingers(self):
        for query in self.finger:
            content = "find successor for finger={}".format(query)
            req = InitSuccessorRequest(self.node_id, self.contact_node, content, initiator = self.node_id)
            self.send(req)

    def init_finger_update(self):
        for i in range(self.num_identifier_bits):
            maxpos = (self.pos_on_ring - 2**i) % self.keyspace_size
            next_node = self.predecessor # can be better
            content = "I might be your finger i={} node={} pos={} maxpos={}".format(i, self.node_id, self.pos_on_ring, maxpos)
            update = InitFingerUpdate(self.node_id, next_node, content, initiator = self.node_id) 
            # print("Node {} sent finger update for i={}".format(self.node_id, i))
            self.send(update)

    def keys_request(self):
        content = "send me your keys before pos={}".format(self.pos_on_ring)
        req = KeysRequest(self.node_id, self.successor, content, initiator=self.node_id)
        self.send(req)

    def stabilize(self):
        print("Node {} starts stabilizing".format(self.node_id))
        content = "who is your predecessor node={} pos={}".format(self.node_id, self.pos_on_ring)
        req = StabRequest(self.node_id, self.successor, content, initiator = self.node_id)
        self.send(req)


    def process_stab(self, pkg):
        if pkg.type == "StabRequest":
            if pkg.content.startswith("who is your predecessor"):
                content = "my predecessor={} pos={}".format(self.predecessor, self.predecessor_pos)
                rep = StabReply(self.node_id, pkg.sender, pkg.id, content, initiator=pkg.initiator)
                self.send(rep)

                tentative_predecessor_pos = int(pkg.content.split("=")[-1])
                tentative_predecessor = pkg.content.split("=")[-2].split(" ")[0]
                if is_in_between(tentative_predecessor_pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
                    self.update_predecessor(tentative_predecessor, tentative_predecessor_pos)
            
        if pkg.type == "StabReply":
            reply_node_pos = int(pkg.content.split("=")[-1])
            reply_node = pkg.content.split("=")[-2].split(" ")[0]
            if reply_node != self.node_id:
                if is_in_between(reply_node_pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
                    self.update_predecessor(reply_node, reply_node_pos)
                if is_in_between(reply_node_pos, self.pos_on_ring, self.successor_pos, self.keyspace_size):
                    self.update_successor(reply_node, reply_node_pos)

        


    def process_key(self, pkg):
        if pkg.type == "KeysRequest":
            requestor_pos = int(pkg.content.split("=")[-1])
            keys_to_send = []
            for key in self.keyvals:
                if is_in_between(requestor_pos, self.dht.hash_fn(int(key))-1, self.pos_on_ring, self.keyspace_size):
                    keys_to_send.append(key)
            
            for key in keys_to_send:
                val = self.keyvals[key]
                content = "you should add key={} val={}".format(key, val)
                rep = KeysReply(self.node_id, pkg.sender, content, initiator=pkg.initiator)
                self.send(rep)
                del self.keyvals[key]
                print("({},{}) sent from {} to {}".format(key, val, self.node_id, pkg.sender))

        if pkg.type == "KeysReply":
            val = pkg.content.split("=")[-1]
            key = int(pkg.content.split("=")[-2].split(" ")[0])
            self.keyvals[key] = val
        
    
    def process_init(self, pkg):
        # print("Node {} processing package".format(self.node_id))

        if pkg.type == "InitPing":
            if pkg.content.startswith("I am your successor now id="):
                successor_pos = int(pkg.content.split("=")[-1])
                successor_id = pkg.content.split("=")[-2].split(" ")[0]
                self.update_successor(successor_id, successor_pos)
                # print("Node {} with pos={} successor update to id={} pos={}".format(self.node_id, self.pos_on_ring, self.successor, self.successor_pos))

            if pkg.content.startswith("I am your predecessor now id="):
                predecessor_pos = int(pkg.content.split("=")[-1])
                predecessor_id = pkg.content.split("=")[-2].split(" ")[0]
                self.update_predecessor(predecessor_id, predecessor_pos)
                # print("Node {} with pos={} predecessor update to id={} pos={}".format(self.node_id, self.pos_on_ring, self.predecessor, self.predecessor_pos))

        if pkg.type == "InitFingerUpdate":
            maxpos = int(pkg.content.split("=")[-1])
            node_pos = int(pkg.content.split("=")[-2].split(" ")[0])
            if is_in_between(self.pos_on_ring, maxpos, node_pos, self.keyspace_size):
                next_node = self.predecessor # can be better
                update = InitFingerUpdate(self.node_id, next_node, pkg.content, initiator = self.node_id) 
                self.send(update)
            else:
                i = int(pkg.content.split("=")[-4].split(" ")[0])
                node_id = pkg.content.split("=")[-3].split(" ")[0]
                finger_pos = self.dht.hash_fn(self.finger[(self.pos_on_ring + 2**i) % self.keyspace_size]) % self.keyspace_size
                if is_in_between(node_pos, self.pos_on_ring, finger_pos, self.keyspace_size):
                    self.finger[(self.pos_on_ring + 2**i) % self.keyspace_size] = node_id
                    next_node = self.predecessor # can be better
                    update = InitFingerUpdate(self.node_id, next_node, pkg.content, initiator = self.node_id) 
                    self.send(update)
        


        if pkg.type == "InitSuccessorRequest":
            if pkg.content.startswith("find successor="):
                pos = int(pkg.content.split("=")[-1])
                if is_in_between(pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
                    # print("Successor for {} pos={} found at node={} pos={} with prec={} pos={}"
                    #       .format(pkg.initiator, pos, self.node_id, self.pos_on_ring, self.predecessor, self.predecessor_pos))
                    content = "successor={} pos={}".format(self.node_id, self.pos_on_ring)
                    rep = InitSuccessorReply(self.node_id, pkg.sender, pkg.id, content, initiator=pkg.initiator)
                    self.send(rep)
                else:
                    next_node_id = self.successor
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
                    next_node_id = self.successor
                    req = InitSuccessorRequest(self.node_id, next_node_id, pkg.content, initiator=pkg.initiator)
                    self.req_to_fulfill[pkg.id] = pkg
                    self.pkg_pointers[req.id] = pkg.id
                    self.send(req)
            
            if pkg.content == "who is your predecessor":
                content = "my predecessor is node={} pos={}".format(self.predecessor, self.predecessor_pos)
                rep = InitSuccessorReply(self.node_id, pkg.sender, pkg.id, content, initiator=pkg.initiator)
                self.send(rep)


        if pkg.type == "InitSuccessorReply":
            if pkg.content.startswith("successor="):
                if pkg.initiator == self.node_id:
                    successor_pos = int(pkg.content.split("=")[-1])
                    successor_id = pkg.content.split("=")[-2].split(" ")[0]
                    self.update_successor(successor_id, successor_pos)
                    print("Node {} successor found={} pos={}".format(self.node_id, self.successor, self.successor_pos))
                    # at this point successor is found. triggered asking successor for fingers
                    self.init_fingers()
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
                    if self.is_finger_ready():
                        self.init_predecessor()

                else:
                    prev_id = self.pkg_pointers[pkg.req_id]
                    prev_req = self.req_to_fulfill[prev_id]
                    rep = InitSuccessorReply(self.node_id, prev_req.sender, prev_req.id, pkg.content, initiator=pkg.initiator)
                    self.send(rep)

            if pkg.content.startswith("my predecessor is node="):
                predecessor_pos = int(pkg.content.split("=")[-1])
                predecessor_id = pkg.content.split("=")[-2].split(" ")[0]
                self.update_predecessor(predecessor_id, predecessor_pos)
                self.active = True
                print("Node {} predecessor updated to {} pos={}".format(self.node_id, self.predecessor, self.predecessor_pos))
                print("Node {} activated".format(self.node_id))
                self.init_notify_pred()
                self.init_notify_successor()
                self.init_finger_update()
                self.keys_request()
                self.stabilize()
                print("keys_request() initiated for Node {}".format(self.node_id))
                # print("Node {} predecessor found={} pos={}".format(self.node_id, self.successor, self.successor_pos))
                # at this point successor is found. triggered asking successor for fingers




    def update_successor(self, successor_id, successor_pos):
        self.successor = successor_id
        self.successor_pos = successor_pos

    def update_predecessor(self, predecessor_id, predecessor_pos):
        self.predecessor = predecessor_id
        self.predecessor_pos = predecessor_pos

    def update_tentative_successor(self, tentative_successor_id, tentative_successor_pos):
        self.tentative_successor = tentative_successor_id
        self.tentative_successor_pos = tentative_successor_pos

    def update_tentative_predecessor(self, tentative_predecessor_id, tentative_predecessor_pos):
        self.tentative_predecessor = tentative_predecessor_id
        self.tentative_predecessor_pos = tentative_predecessor_pos
        
    def commit_successor(self):
        self.successor = self.tentative_successor
        self.successor_pos = self.tentative_successor_pos
        self.tentative_successor = None
        self.tentative_successor_pos = None

    def commit_predecessor(self):
        self.predecessor = self.tentative_predecessor
        self.predecessor_pos = self.tentative_predecessor_pos
        self.tentative_predecessor = None
        self.tentative_predecessor_pos = None



    # def request_keys(self):
    #     # ask successor to transfer keys
    #     if self.successor:
    #         content = "request keys pos={}".format(self.pos_on_ring)
    #         req = KeysRequest(self.node_id, self.successor, content, initiator = self.node_id)
    #         self.send(req)

    # def update_others(self):
    #     print("Node {} calling update_others".format(self.node_id))
    #     for i in range(self.num_identifier_bits):
    #         pos = (self.pos_on_ring - 2**i) % self.keyspace_size
    #         next_node = self.contact_node # can be better
    #         content = "I might be your finger i={} node={} pos={} maxpos={}".format(i, self.node_id, self.pos_on_ring, pos)
    #         update = FingerUpdate(self.node_id, next_node, content, initiator = self.node_id) 
    #         print("Node {} sent finger update for i={}".format(self.node_id, i))
    #         self.send(update)

    # def store(self, key, val):
    #     self.keyvals[key] = val

    # def stabilize(self):
    #     self.stabilize1()

    # def stabilize1(self):
    #     # ask contact node to get me my successor (in his view.) Once so, move to stabilize2
    #     pos = self.pos_on_ring
    #     dest = self.contact_node
    #     content = "find-successor pos={}".format(pos)
    #     stab_pkg = StabRequest(self.node_id, dest, content, initiator = self.node_id, proximity="p2p", id=None)
    #     print("Node {} succcessor request sent to {}".format(self.node_id, dest))
    #     self.send(stab_pkg)

    # def add_finger(self, id, pos):
    #     self.finger[pos] = id

    # def stabilize2(self):
    #     content = "i think you're my successor"
    #     req = StabRequest(self.node_id, self.tentative_successor, content, initiator=self.node_id)
    #     self.send(req)

    #     # if self.tentative_successor:
    #     #     content = "i think you're my successor"
    #     #     req = StabRequest(self.node_id, self.tentative_successor, content, initiator=self.node_id)
    #     #     self.send(req)
    #     # else:
    #     #     self.update_others()
    #     #     self.make_fingers()
    
    # def stabilize3(self):
    #     # tentative_successor_pos = self.dht.hash_fn(self.tentative_successor) % self.keyspace_size
    #     # successors_old_predecessor_pos = self.dht.hash_fn(self.successors_old_predecessor) % self.keyspace_size
    #     print("Node {} entered stabilize3 with tent_succ = {} and old_pred_pos = {}".format(self.node_id, self.tentative_predecessor_pos, self.tentative_predecessor_pos))
    #     # if is_in_between(self.pos_on_ring, successors_old_predecessor_pos, tentative_successor_pos, self.keyspace_size):
    #     if is_in_between(self.pos_on_ring, self.tentative_predecessor_pos, self.tentative_successor_pos, self.keyspace_size):
    #         print("Node {} entered in_between with tent_succ = {} and old_pred_pos = {}".format(self.node_id, self.tentative_predecessor_pos, self.tentative_predecessor_pos))
    #         self.commit_successor()
    #         self.commit_predecessor()
    #         print("Node {} 's successor updated to {}".format(self.node_id, self.successor))
    #         content1 = "you're definitely my successor"
    #         ping1 = StabPing(self.node_id, self.successor, content1)
    #         self.send(ping1)
    #         print("Node {} 's predecessor updated to {}".format(self.node_id, self.predecessor))
    #         content2 = "i'll be your successor"
    #         ping2 = StabPing(self.node_id, self.predecessor, content2)
    #         self.send(ping2)
    #         self.update_others()
    #         self.make_fingers()
    #     # self.active = True
    #     print("Node {} finished stabilize3".format(self.node_id))
    #     return

    # def make_fingers(self):
    #     if self.successor:
    #         for pos in self.finger:
    #             # print(self.contact_node.active)
    #             content = "find-successor pos={}".format(pos)
    #             req = FingerRequest(self.node_id, self.contact_node, content, initiator = self.node_id, proximity="p2p", id=None)
    #             print("Node {} sent a request for finger {} to node {}".format(self.node_id, pos, self.contact_node))
    #             self.send(req)
    #     return
    
    # def is_finger_ready(self):
    #     for pos in self.finger:
    #         if self.finger[pos] == None:
    #             return False
    #     return True





    # def process_stab(self, pkg):

    #     if pkg.type == "FingerUpdate":
    #         maxpos = int(pkg.content.split("=")[-1].split(" ")[0])
    #         pos = int(pkg.content.split("=")[-2].split(" ")[0])
    #         node = pkg.content.split("=")[-3].split(" ")[0]
    #         i = int(pkg.content.split("=")[-4].split(" ")[0])
    #         # print("processing finger update maxpos={} pos={} node={} i={}".format(int(maxpos), int(pos), node, int(i)))
    #         successor_pos = self.dht.hash_fn(self.successor) % self.keyspace_size
    #         if is_in_between(maxpos, self.pos_on_ring-1, successor_pos-1, self.keyspace_size):
    #             # then I might need to change fiinger i
    #             print("Finger update arrived")
    #             current_finger_pos = self.dht.hash_fn(self.finger[(self.pos_on_ring + 2**i) % self.keyspace_size]) % self.keyspace_size
    #             if is_in_between(pos, self.pos_on_ring + 2**i-1, current_finger_pos-1, self.keyspace_size):
    #                 self.finger[(self.pos_on_ring + 2**i) % self.keyspace_size] = node
    #         else:
    #             next_node = self.successor # can be better
    #             update = FingerUpdate(self.node_id, next_node, pkg.content, initiator = pkg.initiator) 
    #             self.send(update)

    #     if pkg.type == "FingerRequest":
    #         if pkg.content.startswith("find-successor pos="):
    #             pos = int(pkg.content.split("=")[-1])
    #             selfpos = self.pos_on_ring
    #             predpos = self.dht.hash_fn(self.predecessor) % self.keyspace_size
    #             if  is_in_between(pos, predpos, selfpos, self.keyspace_size):
    #                 print("Finger {} for Node {} found at node {}".format(pos, pkg.initiator, self.node_id))
    #                 rep = FingerReply(self.node_id, pkg.sender, pkg.id, content = "successor={}".format(self.node_id), 
    #                                   initiator = pkg.initiator, query = pos, proximity="p2p")
    #                 self.send(rep)
    #             else:
    #                 self.req_to_fulfill[pkg.id] = pkg
    #                 next_node_id = self.successor # can do a lot better with find_next_node which needs fixing
    #                 print("Finger {} for Node {} NOT found at node {}, forwarding to node {}".format(pos, pkg.initiator, self.node_id, next_node_id))
    #                 req = FingerRequest(self.node_id, next_node_id , content = pkg.content, initiator = pkg.initiator, 
    #                                      proximity = "p2p", id = None)
    #                 self.pkg_pointers[req.id] = pkg.id
    #                 self.ongoing_requests[req.id] = req
    #                 self.send(req)
             

    #     if pkg.type == "FingerReply":           
    #         if pkg.content.startswith("successor="):
    #             if pkg.initiator == self.node_id:
    #                 finger_id = pkg.content.split("=")[-1]
    #                 self.dht.MakeChannel(self.node_id, finger_id)
    #                 self.add_finger(finger_id, pkg.query)
    #                 if self.is_finger_ready():
    #                     print("Node {} activated".format(self.node_id))
    #                     self.active = True
    #                     print("Node {} initiating request_keys()".format(self.node_id))
    #                     self.request_keys()
    #             else:
    #                 prev_id = self.pkg_pointers[pkg.req_id]
    #                 prev_req = self.req_to_fulfill[prev_id]
    #                 if prev_req.type == "FingerRequest":
    #                     rep = FingerReply(self.node_id, prev_req.sender, prev_req.id, content = pkg.content, 
    #                                     initiator = pkg.initiator, query=pkg.query, proximity="p2p",  id = None)
    #                     self.send(rep)

    #     if pkg.type == "StabPing":
    #         if pkg.content == "you're definitely my successor":
    #             sender_pos = self.dht.hash_fn(pkg.sender) % self.keyspace_size
    #             predeccessor_pos = self.dht.hash_fn(self.predecessor) % self.keyspace_size
    #             if is_in_between(sender_pos, predeccessor_pos, self.pos_on_ring, self.keyspace_size):
    #                 self.predecessor = pkg.sender
    #                 print("Node {} 's predecessor updated to {}".format(self.node_id, self.predecessor))
    #                 # self.lock.release()
                
    #         if pkg.content == "i'll be your successor":
    #             sender_pos = self.dht.hash_fn(pkg.sender) % self.keyspace_size
    #             successor_pos = self.dht.hash_fn(self.successor) % self.keyspace_size
    #             if is_in_between(sender_pos, self.pos_on_ring, successor_pos, self.keyspace_size):
    #                 self.successor = pkg.sender
    #                 print("Node {} 's successor updated to {}".format(self.node_id, self.successor))

    #     if pkg.type == "StabRequest":
    #         if pkg.content == "i think you're my successor":
    #             new_content = "my current predecessor={} predpos={}".format(self.predecessor, self.predecessor_pos)
    #             rep = StabReply(self.node_id, pkg.sender, pkg.id, new_content, initiator=pkg.initiator, proximity="p2p")
    #             self.send(rep)
            
    #         if pkg.content.startswith("find-successor pos="):
    #             pos = int(pkg.content.split("=")[-1])
    #             # selfpos = self.pos_on_ring
    #             # predpos = self.dht.hash_fn(self.predecessor) % self.keyspace_size
    #             if  is_in_between(pos, self.predecessor_pos, self.pos_on_ring, self.keyspace_size):
    #                 # print("Successor of {} found at {}".format(pkg.initiator, self.node_id))
    #                 rep = StabReply(self.node_id, pkg.sender, pkg.id, content = "successor={} pos={}".format(self.node_id, self.pos_on_ring), initiator = pkg.initiator, proximity="p2p")
    #                 self.send(rep)
    #             else:
    #                 print("Successor of {} not found at {}-- relaying to next node {}".format(pkg.initiator, self.node_id, self.successor))
    #                 self.req_to_fulfill[pkg.id] = pkg
    #                 next_node_id = self.successor # can do a lot better with find_next_node which needs fixing
    #                 req = StabRequest(self.node_id, next_node_id , content = pkg.content, initiator = pkg.initiator, proximity = "p2p", id = None)
    #                 self.pkg_pointers[req.id] = pkg.id
    #                 self.ongoing_requests[req.id] = req
    #                 self.send(req)

    #     if pkg.type == "StabReply":
    #         if pkg.content.startswith("successor="):
    #             if pkg.initiator == self.node_id:
    #                 tentative_successor_pos = int(pkg.content.split("=")[-1])
    #                 tentative_successor_id = pkg.content.split("=")[-2].split(" ")[0]
    #                 self.update_tentative_successor(tentative_successor_id, tentative_successor_pos)
    #                 print("Node {} receives tentative successor={}".format(self.node_id, tentative_successor_id))
    #                 # print("tentative successir id = {}".format(successor_id))
    #                 # self.tentative_successor = tentative_successor_id
    #                 self.dht.MakeChannel(self.node_id, self.tentative_successor)
    #                 self.add_finger(self.tentative_successor, self.pos_on_ring+1)
    #                 self.stabilize2()
    #             else:
    #                 prev_id = self.pkg_pointers[pkg.req_id]
    #                 prev_req = self.req_to_fulfill[prev_id]
    #                 if prev_req.type == "StabRequest":
    #                     rep = StabReply(self.node_id, prev_req.sender, prev_req.id, content = pkg.content, initiator = pkg.initiator, proximity="p2p",  id = None)
    #                     self.send(rep)

    #         if pkg.content.startswith("my current predecessor="):
    #             self.tentative_predecessor_pos = int(pkg.content.split("=")[-1])
    #             self.tentative_predecessor = pkg.content.split("=")[-2].split(" ")[0]
    #             self.stabilize3()

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
        # print(pkg.type)
        if pkg.type == "KeysRequest":
            keys_to_delete = []
            for key in self.keyvals:
                # print(self.node_id, pkg.content)
                requester_pos = int(pkg.content.split("=")[-1])
                if not is_in_between(self.dht.hash_fn(int(key)), requester_pos, self.pos_on_ring, self.keyspace_size):
                    content = "key={} val={}".format(key, self.keyvals[key])
                    rep = KeysReply(self.node_id, pkg.sender, content, initiator = pkg.initiator)
                    self.send(rep)
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                del self.keyvals[key]
            print("All keys from {} sent to {}".format(self.node_id, pkg.sender))

        
        if pkg.type == "KeysReply":
            # print("this line should print")
            val = pkg.content.split("=")[-1]
            key = int(pkg.content.split("=")[-2].split(" ")[0])
            self.store(key,val)

        if pkg.type == "ClientRequest":
            query_key = pkg.content.split("=")[-1]
            if query_key in self.keyvals:
                rep = ClientReply(self, pkg.client, content = "Value is {}".format(self.keyvals[query_key]), 
                                  proximity="local",  id = None)
                rep.send()
            else:
                self.req_to_fulfill[pkg.id] = pkg
                next_node_id = self.find_next_node_id(int(query_key))
                req = Request(self.node_id, next_node_id , content = pkg.content, proximity = "local", id = None)
                self.pkg_pointers[req.id] = pkg.id
                self.ongoing_requests[req.id] = req
                self.send(req)



        if pkg.type == "REQ":
            if pkg.content.startswith("Look-up key="):
                query_key = pkg.content.split("=")[-1]
                if query_key in self.keyvals:
                    rep = Reply(self.node_id, pkg.sender, pkg.id, content = "val={}".format(self.keyvals[query_key]), proximity="p2p")
                    self.send(rep)
                else:
                    self.req_to_fulfill[pkg.id] = pkg
                    next_node_id = self.find_next_node_id(int(query_key))
                    req = Request(self.node_id, next_node_id , content = pkg.content, proximity = "p2p", id = None)
                    self.pkg_pointers[req.id] = pkg.id
                    self.ongoing_requests[req.id] = req
                    self.send(req)
            

        if pkg.type == "REP":
            prev_id = self.pkg_pointers[pkg.req_id]
            prev_req = self.req_to_fulfill[prev_id]
            if prev_req.type == "REQ":
                rep = Reply(self.node_id, prev_req.sender, prev_req.id, content = pkg.content, proximity="p2p",  id = None)
                self.send(rep)
                # print("relaying rep")
            if prev_req.type == "ClientRequest":
                val = pkg.content.split("=")[-1]
                rep = ClientReply(self, prev_req.client, content = "Value is {}".format(val),proximity="local",  id = None)
                rep.send()
                # print("client request fulfilled")
                del self.req_to_fulfill[prev_id]
                del self.pkg_pointers[pkg.req_id]

        #     if prev_req.type == "REQ":
        #         pass

