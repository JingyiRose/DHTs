from DHT import *
from Chord.chord_node import *
import math
from Chord.chord_node2 import *

class Chord2(DHT):

    def __init__(self, m, hash_fn = None, is_cheating = False):
        super().__init__()
        if hash_fn == None:
            self.hash_fn = hash
        else:
            self.hash_fn = hash_fn
        self.num_identifier_bits = m
        self.keyspace_size = 2 ** m
        self.node_ids = []
        
        # this is solely for the purpose of easing into imlementations where "cheating" is allowed
        self.is_cheating = is_cheating
        if self.is_cheating:
            self.keyvals = []


    def find_successor_node(self, x):
        # x could be anything in chord ring value (not even have to me mod 2^m)
        closest_node_id = None
        smallest_dist = self.keyspace_size
        for node_id in self.node_ids:
            new_dist = (self.hash_fn(node_id) - x) % self.keyspace_size
            if new_dist < smallest_dist:
                smallest_dist = new_dist
                closest_node_id = node_id
        return closest_node_id
            

    def InsertKey(self, key, val):
        successor_node_id = self.find_successor_node(self.hash_fn(int(key)))
        self.nodes[successor_node_id].store(int(key), val)
        # print(self.keyspace_size)
        print("({},{}) added pos={}".format(key,val, self.hash_fn(int(key)) % self.keyspace_size))
        # print("({},{}) inserted".format(key,val))
        # for cheating only 
        # if self.is_cheating:
        #     self.keyvals.append((key,val))
        # end cheating

    def make_finger(self, key):
        finger = {}
        for i in range(self.num_identifier_bits):
            finger[(int(key) + 2 ** i)%self.keyspace_size] = self.find_successor_node(int(key) + 2 ** i)
        return finger
    
    def MakeNode(self, node_id, ip_address, port, contact_node):
        self.node_ids.append(node_id)
        pos = self.hash_fn(node_id) % self.keyspace_size
        node = ChordNode2(node_id, ip_address, port, contact_node, dht = self, pos = pos)
        self.nodes[node_id] = node
        if not contact_node == "None":
            self.MakeChannel(node_id, contact_node)
        node.initialize()
        print("Node {} made & pos = {} & active = {}".format(node_id, pos, node.active))
        return

    def cheat(self):
        # after all node joins and keys added, we "cheat" once for reassigning fingers and each keyval pairs to an appropriate node
        for node_id in self.node_ids:
            new_finger = self.make_finger(self.hash_fn(node_id))
            self.nodes[node_id].finger = new_finger
            self.nodes[node_id].keyvals = {}
        for (key,val) in self.keyvals:
            successor_node_id = self.find_successor_node(int(key))
            self.nodes[successor_node_id].store(key, val)
        return
