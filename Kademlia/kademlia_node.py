
from Kademlia.kademlia_protocol import *
from env import *
from node import *
from evict_policy import *
from utils import *
from config import *
from DHT import *
import random
from Kademlia.k_bucket import *
from contact import *
import threading
import pickle as pkl
import math



class KademliaNode(Node):
    """Implement Nodes in Kademlia Protocol
    """

    def __init__(self, node_id, ip_address, port, dht, contact,
                 evict_policy=EvictPolicy.EXP_EVICT_POLICY):

        # self.in_channels = {} # key = id of node that self has a channel with, val  = channel instance
        # self.out_channels = {} # key = id of node that self has a channel with, val  = channel instance
        # self.dht = dht
        # self.in_queue = [] # FIFO queue of RPCs going into this node
        # self.is_done = False
        super().__init__(node_id, ip_address, port, dht)
        self.cache = {} # Cache <key, value> pairs
        self.evict_policy = evict_policy
        self.k_buckets = {}
        for i in range(KEY_RANGE):
            self.k_buckets[i] = KBucket(node_id, i)
        self.join(dht, contact)
        self.protocol = KademliaProtocol()
        # keep record of the unused replies we got so far 
        self.replies = {}  # req.id to reply dict

    
    def process(self, pkg):
        """Process the incoming package. Send replies to requests, 
        store replies that it gets from other nodes.

        Args:
            pkg (Package): ClientRequest/Request/Reply
        """

        # Client Requests
        if pkg.type == "GET":
            if pkg.key in self.cache:
                rep = ClientReply(self, pkg.client, 
                            content = "Value is {}".format(self.cache[pkg.key]), 
                            proximity="local",  id = None)
                rep.send()
                print("key found immediately")
                print("client request fulfilled")
            else:
                self.lookup_keyval(pkg.key)
            return

        elif pkg.type == "PUT":
            self.store_pair_on_k_nodes(pkg.key, pkg.val)
            return
        
        message = pkl.load(bytes.fromhex(pkg.content))
        # Node Requests
        if pkg.type == "REQ":
            if message.type == MessageType.FIND_NODE:
                self.protocol.find_node_reply(self, pkg)
            
            elif message.type == MessageType.FIND_VALUE:
                self.protocol.find_value_reply(self, pkg)
            
            elif message.type == MessageType.PING:
                self.protocol.ping_reply(self, pkg)
        # Node Replies
        elif pkg.type == "REP":
            self. replies[pkg.id] = pkg
        return

        

    # ------------ Helper functions for handling Node Requests ------------
    def find_node_handler(self, sender: Contact, key: str)-> List[Contact]:
        """add the sender to kbuckets and returns the contact information of 
        k closest nodes in its routing table to the key

        Args:
            node_id
        
        Returns: a sorted dictionary of K contacts {node_id : contact} closest to the key that the current
        node has contact of. If the current node does not have contact of K nodes
        then return all nodes it knows of. 
        """
        self.add_contact(sender)
        return self.find_closed_contacts(key, K)


    def find_value_handler(self, sender: Contact, key: str):
        """Similar to find_node, except if the node has received a store RPC
        for the key, it just returns the stored value. Additionally, we return
        a success code to indicate whether the value is found or not.
        """
        
        self.add_contact(sender)
        if key in self.cache:
            # 1 is the success code for finding the value
            return (1,self.cache[key])
        return (0,self.find_node_handler(key))


    def store_handler(self, key, val):
        self.cache[key] = val
    

    # ------------ Helper functions for handling Client Requests ------------
    def store_pair_on_k_nodes(self, key, val):
        """locate the k closest nodes to the key and sends them a store RPC
        """
        k_nodes = self.lookup_k_nodes(key) # dict
        for _, contact in k_nodes.items():
            self.store_rpc(self.convert_node_to_contact(), contact, key, val)

    def lookup_keyval(self, key):
        """lookup the value of the key in the DHT
        """

        value = None
        # node_id = None
        value_found = False

        # similar to look-up k nodes, except that the recursive step 
        # uses find_value instead of find_node RPCs
        if key in self.cache:
            return self.cache[key]

        # use dictionary to avoid duplicated node_ids
        k_closest_contacts = {} # sorted by proximity to key
        queried_contacts = {} # node IDs that have already been queried
        # pick P nodes from its closest non-empty k-bucket and if that bucket
        # has fewer than P entries, take the P closest nodes it knows of
        p_contacts = self.find_closed_contacts(key, P)
        distance = xor_base10(self.node_id, key)

        while not value_found:
            # simulate the async calls
            req_ids = []
            for _, contact in p_contacts.items():
                req_id = self.protocol.find_value_rpc(self, contact, key)
                req_ids.append(req_id)
            # stop collecting replies when timeout is reached
            time.sleep(TIMEOUT)
            for req_id in req_ids:
                if req_id in self.replies:
                    reply_info = decode(self.replies[req_id].content).info
                    success, result = reply_info['success'], reply_info['result']
                    # halts immediately when any node returns the value
                    if success == 1:
                        print("value found from find_value_rpc")
                        value = result
                        value_found = True
                        node_id = self.replies[req_id].sender.node_id
                        break
                    else:
                        k_contacts = result
                        k_closest_contacts.update(k_contacts)
                        queried_contacts.update(contact)
                        req_ids.remove(req_id)
                        del self.replies[req_id]
            # of the k nodes the initiator has heard of closest to the target, it picks
            # P that it has not yet queried and resends find_node RPC to them. 
            # note that the initiator can ignore nodes that don't respond quick enough.
            assert len(k_closest_contacts) != 0
            k_closest_contacts = sort_contact_dict(k_closest_contacts, key)
            p_contacts = dict(filter(lambda x: x[0] not in queried_contacts, k_closest_contacts.items())[:P])
                

        # store the <key, value> pair at the closest node it observed to the key
        # that did not return the value

        # For a fair comparison with Chord, we might not want to do this optimization
        # k_closest_contacts = sort_contact_dict(k_closest_contacts, key)[:K]
        # for id, contact in k_closest_contacts.items():
        #     if id != node_id:
        #         self.store_rpc(self.convert_to_contact(), contact, key, value)
        #         break

        # store the <key, value> pair if the node is closer than any other node
        if xor_base10(self.node_id, key) < xor_base10(k_closest_contacts.items()[0][0], key):
            self.cache[key] = value
        
        return value


    # --------------- Core Node Functionalities ---------------
    def join(self, dht:DHT, contact):
        # add node to dht
        dht.nodes[self.node_id] = self

        # insert contact to appropriate k-bucket
        self.add_contact(contact)
        # perform node lookup for its own node id
        k_nodes = self.lookup_k_nodes(self.node_id)
        # add nodes to appropriate k-bucket
        for _, contact in k_nodes.items():
            self.add_contact(contact)
        # refreshes all k-buckets further away than its closest neighbor
        for index in range(1, KEY_RANGE):
            # this populates its k-buckets and inserts itself into other nodes' k-buckets
            self.refresh_bucket(index)

        # need to store any key-value pairs to which it is one of the k-closest
        # we do this when the node is finding a key value pair for the first time
        # if it is closer than the node that returned the value, then it stores the value
        return
    

    def lookup_k_nodes(self, key):
        """locate the k closest nodes to some given key in the DHT
        """
        # use dictionary to avoid duplicated node_ids
        k_closest_contacts = {} # sorted by proximity to key
        queried_contacts = {} # node IDs that have already been queried
        # pick P nodes from its closest non-empty k-bucket and if that bucket
        # has fewer than P entries, take the P closest nodes it knows of
        p_contacts = self.find_closed_contacts(key, P)
        distance = xor_base10(self.node_id, key)

        while True:
            # simulate the async calls
            req_ids = []
            for _, contact in p_contacts.items():
                req_id = self.protocol.find_node_rpc(self, contact, key)
                req_ids.append(req_id)
            # wait to hear replies
            time.sleep(TIMEOUT)
            for req_id in req_ids:
                if req_id in self.replies:
                    k_contacts = decode(self.replies[req_id].content).info['result']
                    k_closest_contacts.update(k_contacts)
                    queried_contacts.update(contact)
                    req_ids.remove(req_id)
                    del self.replies[req_id]
            # of the k nodes the initiator has heard of closest to the target, it picks
            # P that it has not yet queried and resends find_node RPC to them. 
            # note that the initiator can ignore nodes that don't respond quick enough.
            assert len(k_closest_contacts) != 0
            k_closest_contacts = sort_contact_dict(k_closest_contacts, key)
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

        req_ids = []
        for _, contact in k_contacts.items():
            req_id = self.protocol.find_node_rpc(self, contact, key)
            req_ids.append(req_id)

        time.sleep(TIMEOUT)
        counter = 0
        # need to collect all replies
        while counter < len(k_contacts):
            for req_id in req_ids:
                if req_id in self.replies:
                    counter += 1
                    k_contacts = decode(self.replies[req_id].content).info['result']
                    k_closest_contacts.update(k_contacts)
                    queried_contacts.update(contact)
                    req_ids.remove(req_id)
                    del self.replies[req_id]
        

        k_closest_contacts = sort_contact_dict(k_closest_contacts, key)[:K]
        
        return k_closest_contacts
    

    def refresh_bucket(self, index):
        """pick a random ID in the bucket's range and perform a
        node search for that ID. Add the nodes returned to the appropriate k-bucket.
        """
        k_bucket = self.k_buckets[index]
        k_nodes = self.lookup_k_nodes(random.choice(k_bucket).node_id)
        for _, contact in k_nodes:
            self.add_contact(contact)

    

        
    
    # --------------- Other Helper functions  ---------------
    def convert_to_contact(self):
        """Get contact information of a node i.e.
        (IP address, UDP port, Node ID) and store it as a contact object
        """
        return Contact(self.ip_address, self.port, self.key)
    
    def add_contact(self, contact: Contact):
        # Note: this is implementing the static routing table.
        """Add a contact to the appropriate k-bucket.
        If the contact already exists, move the contact to the end of the list.
        Otherwise, if the k-bucket is not full, add the contact to tail.
        If the k-bucket is full, ping the contact at the head (least recently seen)
        and if fails, insert new node to tail; if succeeds, move pinged contact to tail.
        Update last_seen time.
        """
        index = self.find_k_bucket_index(contact.node_id)
        kbucket = self.k_buckets[index]

        if contact in kbucket.contacts:
            kbucket.remove(contact.node_id)
            kbucket.add(contact)
            return
        if len(kbucket) < K:
            kbucket.add(contact)
            return
        # ping the contact at the head
        lrs_node_id, lrs_contact = self.contact.items()[0]
        kbucket.remove(lrs_node_id)
        req_id = self.protocol.ping_rpc(self, self.node_id, lrs_contact)
        time.sleep(TIMEOUT)
        if req_id in self.replies:
            kbucket.add(lrs_contact)
            del self.replies[req_id]
        else:
            kbucket.add(contact)
    
    def find_k_bucket_index(self, key:str) -> int:
        """each k-bucket corresponds to the nodes with xor distance [2^i, 2^{i-1})
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
        
        Returns: a sorted dictionary of num contacts {node_id : contact} closest to the key that the current
        node has contact of. If the current node does not have contact of num nodes
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
    