from Kademlia.contact import Contact
from env import *


def PingRequest(self, source_id, contact: Contact):
    """send a ping request to the destination node want wait for response
    """
    Request(source_id, contact.ip_address, "ping", proximity="p2p")
    return 