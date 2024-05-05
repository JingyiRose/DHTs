from env import *


class LookUpRequest(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, initiator = None, client_id = None, num_hops = 0, proximity = "p2p", id = None):
        self.type = "LookUpRequest"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator
        self.client_id = client_id
        self.num_hops = num_hops


class LookUpReply(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, req_id, content, initiator = None, client_id = None, num_hops = 0, proximity = "p2p", id = None):
        self.type = "LookUpReply"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator
        self.req_id = req_id
        self.client_id = client_id
        self.num_hops = num_hops




class InitSuccessorRequest(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, initiator = None, proximity = "p2p", id = None):
        self.type = "InitSuccessorRequest"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator



class InitSuccessorReply(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, req_id, content, initiator = None, proximity = "p2p", id = None):
        self.type = "InitSuccessorReply"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator
        self.req_id = req_id

class InitFingerUpdate(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, initiator = None, proximity = "p2p", id = None):
        self.type = "InitFingerUpdate"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator

class InitPing(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, initiator = None, proximity = "p2p", id = None):
        self.type = "InitPing"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator

class KeysRequest(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, initiator = None, proximity = "p2p", id = None):
        self.type = "KeysRequest"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator


class KeysReply(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, initiator = None, proximity = "p2p", id = None):
        self.type = "KeysReply"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator

class PutByNode(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, initiator = None, proximity = "p2p", id = None):
        self.type = "PUTByNode"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator



class StabRequest(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, initiator = None, proximity = "p2p", id = None):
        self.type = "StabRequest"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator


class StabReply(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, req_id, content, initiator, proximity = "p2p", id = None):
        self.type = "StabReply"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator
        self.req_id = req_id


class FingerRequest(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, content, initiator = None, proximity = "p2p", id = None):
        self.type = "FingerRequest"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator


class FingerReply(Package):
    # p2p request
    # There could be other various types requests depending on the content
    
    def __init__(self, sender_node, receiver_node, req_id, content, initiator, proximity = "p2p", id = None):
        self.type = "FingerReply"
        if id == None:
            self.id = get_random_string(12)
        else:
            self.id = id
        self.sender = sender_node # id
        self.receiver = receiver_node # id
        self.proximity = "p2p"
        self.content = content
        self.clock_on = False
        self.fulfilled = False
        self.initiator = initiator
        self.req_id = req_id