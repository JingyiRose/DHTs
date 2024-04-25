from DHT import *
from Clique.clique_node import *


class Clique(DHT):

    def __init__(self):
        super().__init__()

    def InsertKey(self, key, val):
        closest_node_id = None
        for node_id in self.nodes:
            if closest_node_id == None:
                closest_node_id = node_id
            elif abs(hash(node_id) - hash(key)) < abs(hash(closest_node_id) -hash(key)):
                closest_node_id = node_id
        self.nodes[closest_node_id].store(key,val)
        print("key {} inserted".format(key))
    
    def MakeNode(self, node_id, ip_address, port):
        node = CliqueNode(node_id, ip_address, port, dht = self)
        self.nodes[node_id] = node
        for other_node_id in self.nodes:
            self.MakeChannel(node_id, other_node_id)
    
    def cheat(self):
        return