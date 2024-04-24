
from enum import Enum


class EvictPolicy(Enum):
    """The policy to decide how long to keep a <key, value> pair in a node's
    cache, and when to evict it. It also specifies if we can only keep a bounded
    number of pairs in the cache, which pair we should evict.
    """


    # The eviction policy used in Kademlia paper:
    # The expiration time of a <key, value> pair in any node is exponentially inversely
    # proportional to the number of nodes between the node and the node whose ID is
    # closest to the key.
    EXP_EVICT_POLICY = "Exponential Decay Eviction Policy"

    # Least recently used eviction policy
    LRU_EVICT_POLICY = "LRU Eviction Policy"