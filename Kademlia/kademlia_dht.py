"""Implements the Kademlia Protocol RPCs
"""

from DHT import *
from Kademlia.kademlia_node import *
import pickle as pkl

class KademliaDHT(DHT):
    """Simulates a Kademlia DHT network."""

    def __init__(self, key_length=KEY_RANGE):
        self.nodes = {}
        self.channels = []
        self.key_length = key_length

        
    def MakeNode(self, node_id, ip_address, port):
        contact = None
        if len(list(self.nodes.items())) > 0:
            # assign an arbitrary node in the network as contact to the new node
            contact = self.nodes[random.choice(list(self.nodes.keys()))].convert_to_contact()
        
        node = KademliaNode(node_id, ip_address, port, self)
        node.start() # start processing packages
        self.nodes[node_id] = node
        node.join(contact)
        # print("node {} made".format(node_id))
        # print("===================================")
        return
    
    # --------------- Centralized Operations for QuickStart  ---------------
            
    def centralized_make_node(self, node_id, ip_address, port):
        """Centralized operation for a node to join the network.
        need to call construct_routing_tables() after all nodes are added."""
        
        node = KademliaNode(node_id, ip_address, port, self)
        self.nodes[node_id] = node

    
    def construct_routing_tables(self):
        # instead of calling node.join(contact), we will construct the routing
        # table for the new nodes with an omniscient view of the network
        
        # populate all the kbuckets by picking a random key in the range
        # of each bucket and the network will tell the node the k existing
        # nodes in that range that is closest to the key
        if DEBUG:
            print(self.nodes.keys())
        for _, node in self.nodes.items():
            for i in range(self.key_length):
                kbucket = node.k_buckets[i]
                rand_key = kbucket.get_random_key_in_range()
                prefix = kbucket.get_prefix()
                k_contacts = self.find_k_closest_w_prefix(prefix, rand_key)
                kbucket.update(k_contacts)
            node.start()
            # self.get_global_view()
        return
    
    
    def centralized_insert_key(self, key, val):
        """Centralized operation to insert a key-value pair in network."""
        closest_node_id = self.find_closest_node(key)
        self.nodes[closest_node_id].cache[key] = val
        return

    def find_closest_node(self, key):
        """Find the closest node to a key in the network."""
        # distances = list(map(lambda x: (x,xor_base10(x,key)), self.nodes.keys()))
        return min(self.nodes.keys(), key = lambda x: xor_base10(x,key))
    
    def find_k_closest_w_prefix(self, prefix, rand_key):
        """Find the k closest nodes to a key with a certain prefix.
        """
        sorted_node_ids = sorted(self.nodes.keys(), key = lambda x: xor_base10(x,rand_key))
        sorted_nodes_w_prefix = filter(lambda x: pad(x,self.key_length)[:len(prefix)] == prefix, sorted_node_ids)
        sorted_contacts_w_prefix = map(lambda x: self.nodes[x].convert_to_contact(), sorted_nodes_w_prefix)
        return list(sorted_contacts_w_prefix)[:K]

    # --------------- Global View of the Network for Monitoring  ---------------

    def get_global_view(self):
        """Get the global view of the network."""
        for node_id in self.nodes.keys():
            node = self.nodes[node_id]
            print(f'----------Node {node_id}----------')
            print(f'KBuckets:')
            for i in range(self.key_length):
                kbucket = node.k_buckets[i]
                if len(kbucket) != 0:
                    print(f'Bucket {i}:')
                    print(f'Contacts: {list(kbucket.contacts.keys())}')
            print(f'Cache:{node.cache}')
        return self.nodes
    
    def write_state_to_file(self, filename):
        """Write the state of the network to a file."""
        with open(filename,'wb+') as f:
            pkl.dump(self, f, protocol=pkl.HIGHEST_PROTOCOL)
    
    def all_nodes_finished(self):
        return all([self.nodes[node_id].has_finished for node_id in self.nodes.keys()])

    def clean_up(self):
        """Clean up the network. Stop all nodes."""
        for node_id in self.nodes.keys():
            self.nodes[node_id].stop()
        return


def read_state_from_file(filename, restart: bool) -> KademliaDHT:
    """Read the state of the network from a file."""
    with open(filename, 'rb') as f:
        k_dht = pkl.load(f)
        if restart:
            for node_id in k_dht.nodes.keys():
                k_dht.nodes[node_id].start()
        return k_dht
    

   

        



