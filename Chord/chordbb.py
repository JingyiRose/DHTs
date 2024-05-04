from DHT import *
from Chord.chord_node import *
import math
from Chord.chord_node_bb import *

class ChordBB(DHT):

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
        
        self.cold_nodes = []


    def find_successor_node(self, x, node_id):
        # x could be anything in chord ring value (not even have to me mod 2^m)
        closest_node_id = None
        smallest_dist = self.keyspace_size
        for other_id in self.node_ids:
            if other_id != node_id:
                new_dist = (self.hash_fn(other_id) - x) % self.keyspace_size
                if new_dist < smallest_dist:
                    smallest_dist = new_dist
                    closest_node_id = other_id
        return closest_node_id
    
    def find_predecessor_node(self, x, node_id):
        # x could be anything in chord ring value (not even have to me mod 2^m)
        closest_node_id = None
        smallest_dist = self.keyspace_size
        for other_id in self.node_ids:
            if other_id != node_id:
                new_dist = (x-self.hash_fn(other_id)) % self.keyspace_size
                if new_dist < smallest_dist:
                    smallest_dist = new_dist
                    closest_node_id = other_id
        return closest_node_id
            

    def InsertKey(self, key, val):
        successor_node_id = self.find_successor_node(self.hash_fn(int(key)), None)
        self.nodes[successor_node_id].store(int(key), val)
        print("Key ({},{}) added pos={} at node={}".format(key,val, self.hash_fn(int(key)) % self.keyspace_size, successor_node_id))

    def make_finger(self, key):
        finger = {}
        for i in range(self.num_identifier_bits):
            finger[(int(key) + 2 ** i)%self.keyspace_size] = self.find_successor_node(int(key) + 2 ** i, node_id = None)
        return finger
    
    def MakeNode(self, node_id, ip_address, port, contact_node):
        pos = self.hash_fn(node_id) % self.keyspace_size
        node = ChordNodeBB(node_id, ip_address, port, contact_node, dht = self, pos = pos)
        self.nodes[node_id] = node
        self.node_ids.append(node_id)
        if contact_node == "None":
            self.cold_nodes.append(node)
            print("Cold Node {} made & pos = {} & active = {}".format(node_id, pos, node.active))
        if not contact_node == "None":
            self.MakeChannel(node_id, contact_node)
            node.initialize() 
        return
    
    def stabilize_cold_nodes(self):
        print("Stabilizing cold nodes")
        self.make_finger_cold_nodes()
        self.make_pointers_cold_nodes()
        print("Cold nodes stabilized")
        for node in self.cold_nodes:
            node.stabilizer = True


    def make_finger_cold_nodes(self):
        for node in self.cold_nodes:
            node.finger = self.make_finger(node.pos_on_ring)
            for k in node.finger:
                other_id = node.finger[k]
                if other_id != node.node_id:
                    self.MakeChannel(node.node_id, other_id)

    
    def make_pointers_cold_nodes(self):
        self.cold_nodes.sort(key=lambda n: n.pos_on_ring)
        for i in range(len(self.cold_nodes)):
            node = self.cold_nodes[i]
            successor = self.cold_nodes[(i+1) % len(self.cold_nodes)] 
            predecessor = self.cold_nodes[(i-1) % len(self.cold_nodes)]
            node.successor = successor.node_id
            node.successor_pos = successor.pos_on_ring
            node.predecessor = predecessor.node_id
            node.predecessor_pos = predecessor.pos_on_ring

