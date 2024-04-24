import threading
from env import *

class Node:

    def __init__(self, node_id, ip_address, port, dht):
        self.node_id = node_id
        self.ip_address = ip_address
        self.port = port
        self.in_channels = {}
        self.out_channels = {}
        self.alive = True
        self.ongoing_requests = {}
        self.req_to_filfill = {}
        self.in_queue = []
        self.is_done = False
        self.dht = dht
        self.pkg_pointers = {}
        # cached key value pairs
        self.cache = {}

        def thread_function(node):
            while not node.is_done:
                if len(node.in_queue) > 0:
                    pkg = node.in_queue.pop(0)
                    node.process(pkg)
            return

        thr = threading.Thread(target=thread_function, args=(self,))
        thr.start()

        self.thread = thr

    def send(self, request):
        # each request is sent into a channel, and triggers a clock start of such request.  
        if request.receiver not in self.out_channels:
            self.open_channel(request.receiver)
        channel = self.out_channels[request.receiver]
        channel.process(request)
        self.ongoing_requests[request.id] = request
        return

    def process(self, pkg):
        # need to specify how each node handles various type of packages
        
        if pkg.type == "ClientRequest":
            destination_key = pkg.query # pkg.query is a placeholder in chord this is finger table
            req = Request(self.node_id, destination_key, content = pkg.content, proximity = "p2p", id = None)
            self.pkg_pointers[req.id] = pkg.id
            self.ongoing_requests[pkg.id] = req
            self.send(req)
            self.req_to_filfill[pkg.id] = pkg

        if pkg.type == "REQ":
            rep = Reply(self.node_id, pkg.sender, pkg.id, content = "value {}".format(self.val), proximity = "p2p")
            self.send(rep)

        if pkg.type == "REP":
            val = pkg.content[-10:]
            prev_id = self.pkg_pointers[pkg.req_id]
            prev_req = self.req_to_filfill[prev_id]
            if prev_req.type == "ClientRequest":
                rep = ClientReply(self, prev_req.origin, content = "Value is {}".format(val), proximity = "local", id = None)
                rep.send()
            if prev_req.type == "REQ":
                # relay the value
                pass
    
    def shut_down(self):
        self.is_done = True


    def dies(self):
        self.alive = False
    
    def finish(self):
        self.is_done = True

    def open_channel(self, destination):
        # destionation is id
        self.dht.MakeChannel(self.node_id, destination)
