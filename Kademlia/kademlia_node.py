
from node import *
from evict_policy import *
from utils import *
from config import *
import random
from k_bucket import *
from contact import *
import threading


class KademliaNode(Node):
    """Implement Nodes in Kademlia Protocol
    """

    def __init__(self, node_id, ip_address, port, dht, contact,
                 evict_policy=EvictPolicy.EXP_EVICT_POLICY):

        super().__init__(node_id, ip_address, port, dht)
        # Cache <key, value> pairs
        self.evict_policy = evict_policy
        self.k_buckets = {}
        self.join(dht, contact)


    #TODO Implement the eviction logic
    
    def join(self, dht, contact):
        # TODO
        # fill k-buckets, and insert itself into other nodes' k-buckets
        # insert contact to appropriate k-bucket
        # perform node lookup for its own node id
        # refreshes all k-buckets further away than its closest neighbor
        # which populates its own k-buckets and inserts itself into other nodes' k-buckets
        return
    
    @staticmethod
    def convert_node_to_contact(node):
        """Get contact information of a node i.e.
        (IP address, UDP port, Node ID) and store it as a contact object
        """
        return Contact(node.ip_address, node.port, node.key)
    

    def find_k_bucket_index(self, key:str) -> int:
        """each k-bucket corresponds to they keys with xor distance [2^i, 2^{i-1})
        from the current node where the index i ranges from [0,KEY_RANGE-1].
        We find the range represented by the index i that they key should fall into
        
        Args:
            key (str): the key to find the appropriate k-bucket
        
        Returns: None if key is the same as the current node ID. Otherwise
        return the index of the k-bucket.
        """
        if int(self.node_id) == int(key):
            return None
        # e.g. when distance 1, it's in the range 2^0 to 2^1, so index is 0
        return len(xor_base2_str(self.node_id, key))-1
    

    def find_closed_contacts(self, target_key, num):
        """find the closest nodes (sorted, up to num) that the current node has contacts of, i.e.
        stored in some k-bucket of the current node.

        Args:
            key (str)
        
        Returns: a sorted list of k nodes closest to the key that the current
        node has contact of. If the current node does not have contact of k nodes
        then return all nodes it knows of. 
        """
        # a sorted dictionary (order is preserved after appending data in python 3.7)
        closest_contact = {}
        # search the buckets from closest to the key to farthest until we have num nodes

        # Let bucket_string = int(self.node_id) ^ 2^i
        # This is the string by flipping 1 bit of node_id at the specified index 
        # corresponding to the bucket.
        # We can use this string to measure the distance of key from the bucket
        sorted_bucket_indices = sorted(list(range(KEY_RANGE)), 
                                key=lambda i: int(target_key, 2) ^int(self.node_id) ^ 2^i)

        num_node_needed = num
        while num_node_needed > 0 and len(sorted_bucket_indices) > 0:
            # get the closest remaining k-bucket
            index = sorted_bucket_indices.pop(0)
            sorted_dict = self.k_buckets[index].sort_by_proximity(target_key, num_node_needed)
            closest_contact.update(sorted_dict)
            num_node_needed -= len(sorted_dict)

        return closest_contact

        
        
    

    def find_node_handler(self, node_id: str):
        """returns the contact information of k closest nodes to the node
        with the specified node_id

        Args:
            node_id
        
        Returns: a list of k tuples <IP address, UDP port, Node ID>
                It can return < k items if it has fewer than k nodes in all of its
                K-buckets combined.
        """

        k_nodes = self.lookup_k_nodes(node_id)
        k_nodes_info = list(map(Node.get_contact_info, k_nodes))
        return k_nodes_info


    def find_value_handler(self, key: str) -> str:
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



    def ping_handler():
        """PINGs can be piggy-backed on RPC replies to provide
        assurance of the sender's network address.
        """
        return

    def store_handler(self, key, val):
        self.cache[key] = val
        return

    def store_pair_on_k_nodes(self, key, val):
        """locate the k closest nodes to the key and sends them a store RPC
        """
        k_nodes = self.lookup_k_nodes(key)
        for node in k_nodes:
            self.store_request(self.convert_node_to_contact(node),key, val)
        return

    def republish(key, val):
        """re-publish to key (key, value) alive every 24 hours, Otherwise the pair
        expire 24 hours after publication, to limit stale information."""
        return


    def find_node_request(self, contact, key):
        """send a find_node RPC to a contact
        """

        return

    def lookup_k_nodes(self, key):
        """locate the k closest nodes to some given key.
        """
        # use dictionary to avoid duplicated node_ids
        k_closest_contacts = {} # sorted by proximity to key
        queried_contacts = {} # node IDs that have already been queried
        # pick P nodes from its closest non-empty k-bucket and if that bucket
        # has fewer than P entries, take the P closest nodes it knows of
        p_contacts = self.find_closed_contacts(key, P)
        distance = xor_base10(self.node_id, key)

        while True:
            for _, contact in p_contacts.items():
                # TODO: async calls
                # sends parallel, asynchronous find_node RPCs to the P ndoes it has chosen.
                threading.Thread(target=self.find_node_request, args=(contact, key)).start()
                k_contacts = self.find_node_request(contact, key)
                k_closest_contacts.update(k_contacts)
                queried_contacts.update(contact)
            # of the k nodes the initiator has heard of closest to the target, it picks
            # P that it has not yet queried and resends find_node RPC to them. 
            # note that the initiator can ignore nodes that don't respond quick enough.
            k_closest_contacts = dict(sorted(k_closest_contacts.items(), lambda x: xor_base10(x[0], key)))
            p_contacts = dict(filter(lambda x: x[0] not in queried_contacts, k_closest_contacts.items())[:P])
            new_distance = xor_base10(k_closest_contacts.items()[0][0], key)
            if new_distance == distance:
                break
            distance = new_distance
            
            
        # if a round of find_node fails to return a node closer to the target,
        # the initiator resends the find_node to all of the k closest nodes it has
        # not queried. lookup terminates when initiator has queried and gotten 
        # responses from the k closest nodes it has seen.
        k_contacts = filter(lambda x: x[0] not in queried_contacts, k_closest_contacts)[:K]
        for _, contact in k_contacts.items():
            # TODO: async calls
            threading.Thread(target=self.find_node_request, args=(contact, key)).start()
            k_closest_contacts.update(self.find_node_request(contact, key))
            # TODO: do something to wait for all threads to join
        k_closest_contacts = dict(sorted(k_closest_contacts.items(), lambda x: xor_base10(x[0], key)))
        
        return k_closest_contacts[:K]


    def refresh_buckets(self):
        """pick a random ID in the bucket's range and perform a
        node search for that ID
        """
        for i in range(KEY_RANGE):
            k_bucket = self.k_buckets[i]
            self.lookup_k_nodes(random.choice(k_bucket).node_id)



        
        