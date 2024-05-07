"""Shared Parameters"""
MEAN = 0.01 # mean of the gaussian distribution
SD = 0.0001 # standard deviation of the gaussian distribution


"""System Parameters for Kademalia Protocol
"""
<<<<<<< HEAD
K = 2 # Replication Parameter in case of failures need K>=2
P = 2 # Concurrency Parameter (alpha in the paper) need P>=2
# CUTOFF_P = (P+1)/2 # replies we need until we stop collecting replies
=======
K = 2 # Replication Parameter in case of failures
P = 2 # Concurrency Parameter (alpha in the paper)
CUTOFF_P = (P+1)/2 # replies we need until we stop collecting replies
>>>>>>> 09f4011d0bcfcf9cd85deb1e66bf254c74fc0bc0
KEY_RANGE = 8 # number of bits in the key space [0,2^160)
KEY_BASE = 2 # the base we use to represent keys in strings

K_COMMAND_FILE = "./test/k_commands.txt"
K_KEYVAL_FILE = "./test/k_keyval.txt"
DEBUG = False
K_DHT_STATE = "./test/k_dht_state.pkl"