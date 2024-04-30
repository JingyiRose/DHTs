import time
import random
import threading
from helper import *
from contact import *
from node import *

class Package:
    """Communication between parties.
    """
    def __init__(self, content, proximity = None, id = None):
        """
        Args:
            content (str): content of the package
            proximity (str): 1) local = client to local machine, 
                            2) p2p = between nodes/threads
            id (str): package id. If not specified, it will be randomly generated
        """

        self.type = None
        if id == None:
            self.id = random.randrange(100000000000, 999999999999)
        self.content = content
        self.proximity = proximity

    def send_local(self, local_node: Node):
        # goes into queue of dest
        if self.proximity == "local":
            local_node.in_queue.append(self)
        
    def send_p2p(self, channel):
        # origin posesses the package and will be shipped through a proper channel to destination
        if self.proximity == "p2p":
            channel.process(self)

class ClientRequest(Package):
    # client request
    # can only be lookup request

    def __init__(self, client, local_node: Node, content, proximity = "local", id = None):
        # origin is client, destination is node instance
        self.type = "ClientRequest"
        self.proximity = "local"
        self.client = client
        self.local_node = local_node
        self.content = content

        if id == None:
            self.id = random.randrange(100000000000, 999999999999)
        else:
            self.id = id
    
    def send(self):
        self.send_local(self.local_node)

class GetRequest(ClientRequest):
    def __init__(self, client, local_node, content, proximity = "local", id = None):
        super.__init__(client, local_node, content, proximity, id)
        self.type = "GET"
        # content is "Look-up key=1234567890" see Client class
        self.key = self.content.split("=")[-1]

class PutRequest(ClientRequest):
    def __init__(self, client, local_node, content, proximity = "local", id = None):
        super.__init__(client, local_node, content, proximity, id)
        self.type = "PUT"
        # content is "Insert key=123456 value=1234567890" see Client class
        content_split = content.split(" ")
        self.key = content_split[1].split("=")[-1][:-1]
        self.val = content_split[2].split("=")[-1][:-1]
        

class ClientReply(Package):
    # client reply

    def __init__(self, local_node: Node, client, content, proximity = "local", id = None):
        # origin is node instance, destination is client
        self.type = "ClientReply"
        self.proximity = "local"
        self.client = client
        self.local_node = local_node
        self.content = content

        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
    
    def send(self):
        self.send_local(self.local_node)
        self.destination.wake()



class Request(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node: Contact, receiver_node: Contact, content, 
                 proximity = "p2p", id = None):
        self.type = "REQ"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node
        self.receiver = receiver_node
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
    
    def start_clock(self, period):
        self.clock_on = True
        while self.clock_on:
            time.sleep(period)
            if self.clock:
                self.sender.revisit(self)

    
    def stop_clock(self):
        self.clock_on = False

    def fulfill(self):
        self.fulfilled = True

    def __str__(self) -> str:
        return "REQ {} {} {} {}".format(self.id, self.sender, self.receiver, self.content)

class Reply(Package):
    # reply from a peer

    def __init__(self, sender_node: Contact, receiver_node: Contact , req_id, 
                 content, proximity = "p2p", id = None):
        self.type = "REP"
        if id == None:
            self.id = random.randrange(100000000000, 999999999999)
        else:
            self.id = id
        self.sender = sender_node
        self.receiver = receiver_node
        self.req_id = req_id
        self.content = content
        self.proximity = "p2p"

    def __str__(self) -> str:
        return "REP {} {} {} {} {}".format(self.id, self.sender, self.receiver, self.req_id, self.content)
    
# class Heartbeat(Package):
#     def __init__(self, id):
#         self.type = "HB"
#         self.id = id

# class Ack(Package):
#     def __init__(self, id, ack_id):
#         self.type = "ACK"
#         self.id = id
#         self.ack_id = ack_id





