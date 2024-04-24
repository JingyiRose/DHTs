
from node import *
from evict_policy import *



class KademliaNode(Node):
    """Implement Nodes in Kademlia Protocol
    """

    def __init__(self, node_id, ip_address, port, dht, contact,
                 evict_policy=EvictPolicy.EXP_EVICT_POLICY):

        super().__init__(node_id, ip_address, port, dht)
        # Cache <key, value} pairs
        self.evict_policy = evict_policy
        self.join(dht, contact)


    #TODO Implement the eviction logic
    
    def join(self, dht, contact):
        # TODO
    
    @staticmethod
    def get_contact_info(node):
        """Get contact information of a node as a tuple 
        (IP address, UDP port, Node ID)
        """
        return (node.ip_address, node.port, node.key)



    def find_node(self, node_ID: str):
        """returns the contact information of k closest nodes to the node
        with the specified node_ID

        Args:
            160-bit node_ID
        
        Returns: a list of k tuples <IP address, UDP port, Node ID>
                It can return < k items if it has fewer than k nodes in all of its
                K-buckets combined.
        """

        k_nodes = self.lookup_k_nodes(node_ID)
        k_nodes_info = list(map(Node.get_contact_info, k_nodes))
        return k_nodes_info


    def find_value(self, key: str) -> str:
        """Similar to find_node, except if the node has received a store RPC
        for the key, it just returns the stored value.
        """
        
        if key in self.cache:
            return self.cache[key]
        return self.find_node(key)


    def find_pair(self, key):
        k_nodes = self.lookup_k_nodes(key)

        # recursive step uses find_value instead of find_node RPCs??

        # halts immediately when any node returns the value

        # store the <key, value> pair at the closest node it observed to the key
        # that did not return the value
        # closest_node.store(key, val)

        return



    def ping():
        """PINGs can be piggy-backed on RPC replies to provide
        assurance of the sender's network address.
        """
        return

    def store(self, key, val):
        self.cache[key] = val
        return

    def store_pair_on_k_nodes(self, key, val):
        """locate the k closest nodes to the key and sends them a store RPC
        """
        return

    def republish(key, val):
        """re-publish to key (key, value) alive every 24 hours, Otherwise the pair
        expire 24 hours after publication, to limit stale information."""
        return

    def lookup_k_nodes(key):
        # locate the k closest nodes to some given key.

        # pick a (some concurrency parameter e.g.3) nodes from its closest non-empty
        # k-bucket and if that bucket has fewer than a entries, take the a closes 
        # nodes it knows of.

        # sends parallel, asynchronous find_node RPCs to the a ndoes it has chosen.
        # For the returned RPCs, the initiator resends the 
        # find_node RPC to nodes it has learned about from that RPC:
        # of the k nodes the initiator has heard of closest tot eh target, it picks
        # a that it has not yet queried and resends find_node RPC to them. 
        # note that the initiator can ignore nodes that don't respond quick enough.
        # if a round of find_node fails to return a node closer to the target,
        # the initiator resends the find_node to all of the k closest nodes it has
        # not queried. lookup terminates when initiator has queried and gotten 
        # responses from the k closest nodes it has seen.
        return


    def refresh_bucket(self, k_bucket):
        """pick a random ID in the bucket's range and perform a
        node search for that ID
        """
        return
