from Kademlia.contact import Contact
from env import *
from Kademlia.kademlia_node import *


class RequestType(Enum):
    PING = "ping"
    STORE = "store"
    FIND_NODE = "find_node"
    FIND_VALUE = "find_value"


class Message:
    
    def __init__(self, request_type: RequestType, info: str):
        self.request_type = request_type
        # dictionary of key value pairs
        self.info = info
        return
    



class KademliaProtocol:

    def __init__(self, node):
        # node instance running this protocol
        self.node = node
        

    def ping_rpc(self, source_id, contact: Contact):
        """send a ping request to the destination node wait for response
        """
        request = Request(source_id, contact.ip_address, 
                          Message(RequestType.PING, {}), proximity="p2p")
        self.node.send_p2p(request)
        return 
    
    def store_rpc(self, source_id, contact: Contact, key, value):
        """send a store request to the destination node
        """
        info = dict(key=key, value=value)
        request = Request(source_id, contact.ip_address, 
                          Message(RequestType.STORE, info), proximity="p2p")
        self.node.send_p2p(request)
        return
    
    def find_node_rpc(self, source_id, contact: Contact, key):
        """send a find_node request to the destination node
        """
        info = dict(key=key)
        request = Request(source_id, contact.ip_address, 
                          Message(RequestType.FIND_NODE, info), proximity="p2p")
        self.node.send_p2p(request)
        return
    
    def find_value_rpc(self, source_id, contact: Contact, key):
        """send a find_value request to the destination node
        """
        info = dict(key=key)
        request = Request(source_id, contact.ip_address, 
                          Message(RequestType.FIND_VALUE, info), proximity="p2p")
        self.node.send_p2p(request)
        return