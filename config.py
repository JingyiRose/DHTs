"""System Parameters for Kademalia Protocol
"""
K = 20 # Replication Parameter in case of failures
P = 3 # Concurrency Parameter (alpha in the paper)
CUTOFF_P = (P+1)/2 # replies we need until we stop collecting replies
KEY_RANGE = 8 # number of bits in the key space [0,2^160)
KEY_BASE = 2 # the base we use to represent keys in strings
TIMEOUT = 1 # timeout for RPC calls

K_COMMAND_FILE = "./test/k_commands.txt"
K_KEYVAL_FILE = "./test/k_keyval.txt"