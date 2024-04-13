import random
import time
import os

random.seed(43)


def maketest(num_keys, num_nodes, num_lookups, testfile, keyvalfile):
    # generate sequence of operations stored in txt file
    # need to specify number of keys, nodes, and (random) lookups
    if os.path.exists(testfile):
        os.remove(testfile)
    if os.path.exists(keyvalfile):
        os.remove(keyvalfile)
    keys_ids = random.sample(range(1000000000, 9999999999), num_keys)
    values = random.sample(range(1000000000, 9999999999), num_keys)
    nodes_ids = keys_ids[:num_nodes]

    f1 = open(keyvalfile, 'w')
    for i in range(num_keys):
        f1.write('{} {}\n'.format(keys_ids[i], values[i]))
    f1.close()

    f2 = open(testfile, 'w')


    for i in range(num_nodes):
        f2.write('{}: make node {} {}\n'.format(i, nodes_ids[i], values[i]))

    for i in range(num_nodes, num_keys):
        f2.write('{}: make key {} {}\n'.format(i, keys_ids[i], values[i]))

    request_nodes = random.choices(nodes_ids, k = num_lookups)
    destination_keys = random.choices(keys_ids, k = num_lookups)
    
    for i in range(num_lookups):
        f2.write('{}: look up {} {}\n'.format(i+num_keys, request_nodes[i], destination_keys[i]))
    f2.close()

if __name__ == "__main__":
    num_keys = 10
    num_nodes = 10
    num_lookups = 25
    testfile = 'log.txt'
    keyvalfile = 'keyval.txt'
    maketest(num_keys, num_nodes, num_lookups, testfile, keyvalfile)

