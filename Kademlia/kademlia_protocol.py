from contact import Contact
from env import *
from Kademlia.kademlia_node import *
import pickle as pkl


# TODO: fix request and reply class: node type -> contact type

class MessageType(Enum):
    # request message types
    PING = "ping"
    STORE = "store"
    FIND_NODE = "find_node"
    FIND_VALUE = "find_value"


class Message:
    
    def __init__(self, type: MessageType, info: dict):
        self.type = type
        # dictionary of key value pairs
        self.info = info
        return

def encode(msg: Message) -> str:
    return pkl.dump(msg).hex()

def decode(msg: str) -> Message:
    return pkl.load(bytes.fromhex(msg))


class KademliaProtocol:

    @staticmethod
    def ping_rpc(node, dest: Contact):
        """send a ping request to the destination node wait for response
        """
        request = Request(node.convert_to_contact(), dest, 
                          encode(Message(MessageType.PING, {})), proximity="p2p")
        node.send_p2p(request)
        # TODO: wait for response? asyn and find response in message queue?
        # return 1 if get a valid response, 0 if not
        return request.id
    
    @staticmethod
    def store_rpc(node, dest: Contact, key, value):
        """send a store request to the destination node
        """
        info = dict(key=key, value=value)
        request = Request(node.convert_to_contact(), dest,
                          encode(Message(MessageType.STORE, info)), proximity="p2p")
        node.send_p2p(request)
        # don't need to wait for response
        return request.id
    
    @staticmethod
    def find_node_rpc(node, dest: Contact, key):
        """send a find_node request to the destination node
        """
        info = dict(key=key)
        request = Request(node.convert_to_contact(), dest, 
                          encode(Message(MessageType.FIND_NODE, info)), proximity="p2p")
        node.send_p2p(request)
        return request.id
    
    @staticmethod
    def find_value_rpc(node, dest: Contact, key):
        """send a find_value request to the destination node
        """
        info = dict(key=key)
        request = Request(node.convert_to_contact(), dest, 
                          encode(Message(MessageType.FIND_VALUE, info)), proximity="p2p")
        node.send_p2p(request)
        return request.id



    @staticmethod
    def ping_reply(node, pkg: Package):
        """a node replies to a ping request
        """
        reply = Reply(pkg.sender, pkg.receiver, pkg.id, 
                      encode(Message(MessageType.PING, {})), proximity="p2p")

        node.send_p2p(reply)
        return
    
    # Store request does not need a reply
    
    @staticmethod
    def find_node_reply(node, pkg: Package):
        """a node replies to a find_node request
        """
        info = dict(result = node.find_node_handler(pkg.sender, pkg.content["key"]))
        reply = Reply(pkg.sender, pkg.receiver, pkg.id, 
                      encode(Message(MessageType.FIND_NODE, info)), proximity="p2p")
        node.send_p2p(reply)
        return
    
    @staticmethod
    def find_value_reply(node, pkg: Package):
        """a node replies to a find_value request
        """
        success, result = node.find_value_handler(pkg.sender, pkg.content["key"])
        info = dict(success = success, result = result)
        reply = Reply(pkg.sender, pkg.receiver, pkg.id, 
                      encode(Message(MessageType.FIND_VALUE, info)), proximity="p2p")
        node.send_p2p(reply)
        return