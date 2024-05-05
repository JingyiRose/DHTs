
from typing import List
from Kademlia.utils import *
import time
import random
from contact import Contact


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
        return f'{(int(self.node_id, KEY_BASE) + rand_dist) % (2**KEY_RANGE):b}'
    
    def get_prefix(self):
        """Get the prefix that all nodes in this k-bucket share. 
        This function is mostly for debugging purposes.
        """
        # padded with 0 to a total length KEY_RANGE
        bin_string = f'{int(self.node_id, KEY_BASE):0{KEY_RANGE}b}'
        part1 = bin_string[:-self.index-1]
        part2 = flip(bin_string[-self.index-1])
        return part1 + part2


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
    
    
if __name__ == "__main__":
    # test KBucket
    node_id = "1010101"
    index = 7
    bucket = KBucket(node_id, index)
    bucket.contacts = {"10011011": Contact("ip", "port", "10011011"), 
                       "10001011": Contact("ip", "port", "10001011"),
                       "10000000": Contact("ip", "port", "10000000")}
    print(f'Key has length {KEY_RANGE}')
    print(f'the node is {node_id}')
    print(f'index of the bucket is {index}')
    print(f'prefix of the bucket is {bucket.get_prefix()}')
    print(f'a random key in the range is {bucket.get_random_key_in_range()}')
    print(bucket.sort_by_proximity("10111011",10).keys())
    print(bucket.sort_by_proximity("10101011",10).keys())
    print(bucket.sort_by_proximity("00000000",10).keys())



