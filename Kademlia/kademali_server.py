

from Kademlia.kademlia_node import KademliaNode
from Kademlia.kademlia_protocol import KademliaProtocol


class KademliaServer:
    def __init__(self, node_id, ip_address, port, contact, dht):
        
        self.node = KademliaNode(node_id, ip_address, port, dht, contact)
        self.dht = dht,
        self.protocol = KademliaProtocol(self.node)
