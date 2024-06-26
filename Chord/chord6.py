from DHT import *
import math
from Chord.chord_node6 import *

class Chord6(DHT):

    def __init__(self, m, hash_fn = None):
        super().__init__()
        if hash_fn == None:
            self.hash_fn = lambda x: int(str(x),2)
        else:
            self.hash_fn = hash_fn
        self.num_identifier_bits = m
        self.keyspace_size = 2 ** m
        self.node_ids = []
        self.cold_keyvals = []
        
        
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
        self.cold_keyvals.append((key, val))
         



    def make_finger(self, pos):
        finger = {}
        for i in range(self.num_identifier_bits):
            finger[(pos + 2 ** i)%self.keyspace_size] = self.find_successor_node(pos + 2 ** i, node_id = None)
        return finger
    
    def MakeNode(self, node_id, ip_address, port, make_contact = True):
        pos = self.hash_fn(node_id) % self.keyspace_size
        if make_contact:
            contact_node = random.choice(self.node_ids)
        else:
            contact_node = "None"

        node = ChordNode6(node_id, ip_address, port, contact_node, dht = self, pos = pos)
        if not make_contact:
            self.cold_nodes.append(node)

        self.nodes[node_id] = node
        self.node_ids.append(node_id)

        if not contact_node == "None":
            self.MakeChannel(node_id, contact_node)
            node.initialize() 
        return
    
    def arrange_keys(self):
        for (key,val) in self.cold_keyvals:
            successor_node_id = self.find_successor_node(self.hash_fn(int(key)), None)
            self.nodes[successor_node_id].store(key, val)

    
    def stabilize_cold_files(self):
        print("Stabilizing cold nodes")
        self.make_finger_cold_nodes()
        self.make_pointers_cold_nodes()
        self.arrange_keys()
        for node in self.cold_nodes:
            node.stabilizer = True
        print("Cold nodes stabilized")


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

