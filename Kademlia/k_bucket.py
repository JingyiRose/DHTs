
from typing import List
from utils import *
import time
from Kademlia.kademlia_protocol import ping_request


class KBucket:
    """The bucket that stores k contacts in the subtree not containing the node ID.
    """

    def __init__(self, node_id):
        # self.node_id = node_id # the node it belongs to
        # maps node_ids to contact objects, sorted by time last seen
        # more recently seen contacts are at the end of the list
        self.contacts = {}
        self.last_seen = {}
        self.node_id = node_id

    
    def sort_by_proximity(self, target_key: str, num: int) -> dict:
        """Sort the list of node_ids in the k-bucket by distance to target,
        from closest to farthest. Truncate the returned list at some number.
        

        Args:
            target (str): the key we are looking up
            num (int): how many node_ids to return

        Return: a sorted dict of length num
        """
        return sorted(self.contacts, 
                      key=lambda x: xor_base10(x.node_id, target_key))[:num]

    
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
    
    




