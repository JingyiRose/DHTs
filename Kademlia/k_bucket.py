
from typing import List
from Kademlia.utils import *
import time
import random


class KBucket:
    """The bucket that stores k contacts in the subtree not containing the node ID.
    """

    def __init__(self, node_id: str, index: int):
        # more recently seen contacts are at the end of the list
        self.contacts = {} # map node_id -> Contact
        self.last_seen = {}
        self.node_id = node_id
        # index i represents nodes of distance [2^i, 2^{i-1}) from the current node
        self.index = index

    def get_random_key_in_range(self):
        """Get a random key whose distance with the current node is 
        in the range of distance that the k-bucket covers.
        """
        rand_dist = random.randint(2**(self.index), 2**(self.index+1)-1)
        return f'{int(self.node_id, KEY_BASE) + rand_dist:b}'
    
    def get_prefix(self):
        """Get the prefix that all nodes in this k-bucket share. 
        This function is mostly for debugging purposes.
        """
        # padded with 0 to a total length KEY_RANGE
        bin_string = f'{int(self.node_id, KEY_BASE):0{KEY_RANGE}b}'
        return bin_string[:-self.index-1] + flip(bin_string[-self.index-1])


    def sort_by_proximity(self, target_key: str, num: int) -> dict:
        """Sort the list of node_ids in the k-bucket by distance to target,
        from closest to farthest. Truncate the returned list at some number.
        

        Args:
            target (str): the key we are looking up
            num (int): how many node_ids to return

        Return: a sorted dict of length num
        """
        return dict(list(sort_contact_dict(self.contacts, target_key).items())[:num])

    
    def add(self, contact):
        """Add the contact to the tail of k-bucket and update last seen time.

        Args:
            contact (Contact): the contact to be added
        """
        self.contacts[contact.node_id] = contact
        self.last_seen[contact.node_id] = time.time()
        return

    def remove(self, node_id):
        """Remove the contact from the k-bucket if exists.

        Args:
            node_id (str): the node_id of the contact to be removed
        """
        if node_id in self.contacts:
            del self.contacts[node_id]
            del self.last_seen[node_id]


    def __contains__(self, node_id):
        return node_id in self.contacts

    def __len__(self):
        return len(self.contacts)
    
    




