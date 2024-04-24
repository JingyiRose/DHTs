from node import *

class KademliaNode(Node):
    """Implement Nodes in Kademlia Protocol
    """

    def __init__(self, node_id, ip_address, port, dht, contact,
                 evict_policy=EvictPolicy.EXP_EVICT_POLICY):

        super().__init__(node_id, ip_address, port, dht)
        # Cache <key, value} pairs
        self.evict_policy = evict_policy
        self.join(dht, contact)
