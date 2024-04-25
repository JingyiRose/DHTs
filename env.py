import time
import random
import threading

class Package:
    # whatever is communicated between partites -- two types 1) local = client to local machine, 2) p2p = between nodes/threads
    def __init__(self, origin, destination, content, proximity = None, id = None):

        # if proximity is local, origin and destination are both objects
        # if proximity is p2p, origin and destination are nodes in dht; and is represented by identifiers
        self.type = None
        if id == None:
            self.id = random.randrange(100000000000, 999999999999)
        self.origin = origin
        self.destination = destination
        self.content = content
        self.proximity = proximity

    def send_local(self):
        # goes into queue of dest
        if self.proximity == "local":
            self.destination.in_queue.append(self)
        
    def send_p2p(self, channel):
        # origin posesses the package and will be shipped through a proper channel to destination
        if self.proximity == "p2p":
            channel.process(self)

class ClientRequest(Package):
    # client request
    # can only be lookup request

    def __init__(self, origin, local_node, query, content, proximity = "local", id = None):
        # origin is client, destination is node instance
        self.type = "ClientRequest"
        self.proximity = "local"
        self.destination = local_node
        self.query = query
        # print("destination {}".format(destination))
        self.origin = origin
        self.content = content

        if id == None:
            self.id = random.randrange(100000000000, 999999999999)
        else:
            self.id = id
    
    def send(self):
        self.send_local()

class ClientReply(Package):
    # client reply

    def __init__(self, origin, client, content, proximity = "local", id = None):
        # origin is client, destination is node instance
        self.type = "ClientReply"
        self.proximity = "local"
        self.destination = client
        self.origin = origin
        self.content = content

        if id == None:
            self.id = random.randrange(100000000000, 999999999999)
        else:
            self.id = id
    
    def send(self):
        self.send_local()
        self.destination.wake()



class Request(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, proximity, id = None):
        self.type = "REQ"
        if id == None:
            self.id = random.randrange(100000000000, 999999999999)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
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

    def __init__(self, sender_node, receiver_node, req_id, content, proximity, id = None):
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





