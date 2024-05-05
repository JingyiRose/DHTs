from enum import Enum
from contact import Contact
from env import *
from Kademlia.kademlia_node import *
import pickle as pkl
from config import DEBUG


""" Handling Kademlia protocol messages """

class MessageType(Enum):
    # request message types
    PING = "PING"
    STORE = "STORE"
    FIND_NODE = "FIND_NODE"
    FIND_VALUE = "FIND_VALUE"


class Message:
    
    def __init__(self, type: MessageType, info: dict):
        self.type = type
        # dictionary of key value pairs
        self.info = info
        return
    
    def __str__(self) -> str:
        content = ""
        if "result" in self.info and type(self.info["result"]) == dict:
            content = "Contacts = {"
            for key, value in self.info["result"].items():
                # just print the node_ids of the contacts
                content += "{}, ".format(key)
            content += "}"
        else:
            content = self.info
        return "Message: {}, {}".format(self.type.value, content)

def encode(msg: Message) -> str:
    return pkl.dumps(msg).hex()

def decode(msg: str) -> Message:
    return pkl.loads(bytes.fromhex(msg))


def debug_print(debug, is_request, msg, pkg):
    if debug and is_request:
        print("REQ   {} S:{} R:{} {}".format(pkg.id, pkg.sender.node_id, 
                    pkg.receiver.node_id, msg))
    if debug and not is_request:
        print("REPLY {} S:{} R:{} {}".format(pkg.req_id, pkg.sender.node_id, 
                    pkg.receiver.node_id, msg))

def ping_rpc(node, dest: Contact, debug = DEBUG):
    """send a ping request to the destination node wait for response
    """
    msg = Message(MessageType.PING, {})
    request = Request(node.convert_to_contact(), dest, 
                        encode(msg), proximity="p2p")
    node.send(request) #p2p request
    debug_print(debug, True, msg, request)
    return request.id


def store_rpc(node, dest: Contact, key, value, debug = DEBUG):
    """send a store request to the destination node
    """
    info = dict(key=key, value=value)
    msg = Message(MessageType.STORE, info)
    request = Request(node.convert_to_contact(), dest,
                        encode(msg), proximity="p2p")
    node.send(request)
    debug_print(debug, True, msg, request)
    return request.id


def find_node_rpc(node, dest: Contact, key, debug = DEBUG):
    """send a find_node request to the destination node
    """
    info = dict(key=key)
    msg = Message(MessageType.FIND_NODE, info)
    request = Request(node.convert_to_contact(), dest, 
                        encode(msg), proximity="p2p")
    node.send(request)
    debug_print(debug, True, msg, request)
    return request.id


def find_value_rpc(node, dest: Contact, key, debug = DEBUG):
    """send a find_value request to the destination node
    """
    info = dict(key=key)
    msg = Message(MessageType.FIND_VALUE, info)
    request = Request(node.convert_to_contact(), dest, 
                        encode(msg), proximity="p2p")
    node.send(request)
    debug_print(debug, True, msg, request)
    return request.id



def ping_reply(node, pkg: Package, debug = DEBUG):
    """a node replies to a ping request
    """
    msg = Message(MessageType.PING, {})
    reply = Reply(pkg.receiver, pkg.sender, pkg.id, 
                    encode(msg), proximity="p2p")

    node.send(reply)
    debug_print(debug, False, msg, reply)
    return

# Store request does not need a reply
def store_reply(node, pkg: Package):
    data = decode(pkg.content).info
    key, val = data["key"], data["value"]
    node.cache[key]= val
    if DEBUG:
        print(f"Stored <{key}, {val}> in node {node.node_id}")
    return


def find_node_reply(node, pkg: Package, debug = DEBUG):
    """a node replies to a find_node request
    """
    info = dict(result = node.find_node_handler(pkg.sender, decode(pkg.content).info["key"]))
    msg = Message(MessageType.FIND_NODE, info)
    reply = Reply(pkg.receiver, pkg.sender, pkg.id, 
                    encode(msg), proximity="p2p")
    node.send(reply)
    debug_print(debug, False, msg, reply)
    return

def find_value_reply(node, pkg: Package, debug = DEBUG):
    """a node replies to a find_value request
    """
    success, result = node.find_value_handler(pkg.sender, decode(pkg.content).info["key"])
    info = dict(success = success, result = result)
    msg = Message(MessageType.FIND_VALUE, info)
    reply = Reply(pkg.receiver, pkg.sender, pkg.id, 
                    encode(msg), proximity="p2p")
    node.send(reply)
    debug_print(debug, False, msg, reply)
    return