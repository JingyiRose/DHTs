import time

class Channel:
    # channel is a unidirectional communication medium between two nodes/threads. Things that could come into a channel include
    # - Heartbeat
    # - Ack
    # - Request
    #    - there could be various types of requests based on dht type (e.g. chord needs pointers redirection if node fails/joins) this could be specified by content
    # - Reply
    #    - reply to a request
    #    - for requests that dont require a reply, maybe send an ack?

    def __init__(self, sender, receiver, latency_dist):
        # sender and receiver is node object NOT ids
        self.sender = sender
        self.receiver = receiver
        self.latency_dist = latency_dist
    
    def process(self, request):
        lat = self.latency_dist.draw()
        time.sleep(lat/1000)
        self.receiver.in_queue.append(request)

    def activate(self):
        self.sender.out_channels[self.receiver.key] = self
        self.receiver.in_channels[self.sender.key] = self
