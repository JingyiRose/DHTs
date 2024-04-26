from node import *

class CliqueNode(Node):
    def __init__(self, node_id, ip_address, port, dht):
        super().__init__(node_id, ip_address, port, dht)
        self.keyvals = {}
        # print("node made: {}".format(self.node_id))
        self.alive = True
        self.ongoing_requests = {}
        self.req_to_fulfill = {}
        self.in_queue = []
        self.is_done = False
        self.pkg_pointers = {}

    def store(self, key, val):
        self.keyvals[key] = val



    def process(self, pkg):
        # need to specify how each node handles various type of packages
        
        if pkg.type == "ClientRequest":
            self.req_to_fulfill[pkg.id] = pkg
            for nbr_node_id in self.out_channels:
                req = Request(self.node_id, nbr_node_id, content = pkg.content, proximity = "local", id = None)
                self.pkg_pointers[req.id] = pkg.id
                self.ongoing_requests[req.id] = req
                self.send(req)
                


        if pkg.type == "REQ":
            query_key = pkg.content.split("=")[-1]
            if query_key in self.keyvals:
                rep = Reply(self.node_id, pkg.sender, pkg.id, content = "val={}".format(self.keyvals[query_key]), proximity="p2p")
            else:
                rep = Reply(self.node_id, pkg.sender, pkg.id, content = "", proximity="p2p")
            self.send(rep)

        if pkg.type == "REP":
            prev_id = self.pkg_pointers[pkg.req_id]
            prev_req = self.req_to_fulfill[prev_id]
            if prev_req.type == "ClientRequest":
                if len(pkg.content) > 0:
                    print("val found")
                    val = pkg.content.split("=")[-1]
                    rep = ClientReply(self, prev_req.client, content = "Value is {}".format(val),proximity="p2p",  id = None)
                    rep.send()
                    # del self.req_to_fulfill[prev_id]
                    # del self.pkg_pointers[pkg.req_id]

            if prev_req.type == "REQ":
                pass

