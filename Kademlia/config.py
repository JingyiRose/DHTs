"""System Parameters for Kademalia Protocol
"""

K = 20 # Replication Parameter in case of failures
P = 3 # Concurrency Parameter (alpha in the paper)
CUTOFF_P = (P+1)/2 # replies we need until we stop collecting replies
KEY_RANGE = 160 # number of bits in the key space [0,2^160)
KEY_BASE = 10 # the base we use to represent keys in strings
TIMEOUT = 1 # timeout for RPC calls
