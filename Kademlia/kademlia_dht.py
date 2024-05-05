"""Implements the Kademlia Protocol RPCs
"""

from DHT import *
from Kademlia.kademlia_node import *

class KademliaDHT(DHT):
    """Simulates a Kademlia DHT network."""

    def __init__(self):
        super().__init__()
        # self.nodes = {} inherited from DHT

        
    def MakeNode(self, node_id, ip_address, port):
        contact = None
        if len(self.nodes) > 0:
            # assign an arbitrary node in the network as contact to the new node
            contact = self.nodes[random.choice(list(self.nodes.keys()))].convert_to_contact()
        
        node = KademliaNode(node_id, ip_address, port, self)
        self.nodes[node_id] = node
        node.join(contact)
        # print("node {} made".format(node_id))
        # print("===================================")
        return
    
    # --------------- Centralized Operations for QuickStart  ---------------
            
    def centralized_node_join(self, node):
        """Centralized operation for a node to join the network."""
        # print("node {} joining".format(node.node_id))
        self.nodes[node.node_id] = node
        



