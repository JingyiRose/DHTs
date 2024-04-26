import random
from helper import *
import os

random.seed(43)


def maketest(num_nodes, num_keyvals, num_lookups, save_to, keyvalfile, 
             node_id_length = 8, node_ip_length = 12, node_port_length = 5, 
             key_length = 8, val_length = 16):
    # generate sequence of operations stored in txt file
    # need to specify number of keys, nodes, and (random) lookups
    if os.path.exists(save_to):
        os.remove(save_to)
    if os.path.exists(keyvalfile):
        os.remove(keyvalfile)
    node_ids = [get_random_string(node_id_length) for _ in range(num_nodes)]
    node_ips = [get_random_string(node_ip_length) for _ in range(num_nodes)]
    node_ports = [get_random_digits(node_port_length) for _ in range(num_nodes)]
    keys = [get_random_digits(key_length) for _ in range(num_keyvals)]
    vals = [get_random_digits(val_length) for _ in range(num_keyvals)]


    f1 = open(keyvalfile, 'w')
    for i in range(num_keyvals):
        f1.write('({},{})\n'.format(keys[i], vals[i]))
    f1.close()

    f2 = open(save_to, 'w')


    for i in range(num_nodes):
        f2.write('nodejoin id={}, ip={}, port={}\n'.format(node_ids[i], node_ips[i], node_ports[i]))

    for i in range(num_keyvals):
        f2.write('insert key={}, val={}\n'.format(keys[i], vals[i]))

    request_nodes = random.choices(node_ids, k = num_lookups)
    destination_keys = random.choices(keys, k = num_lookups)
    
    for i in range(num_lookups):
        f2.write('look-up localnode={}, key={}\n'.format(request_nodes[i], destination_keys[i]))
    f2.close()
    return

if __name__ == '__main__':
    num_nodes = 5
    num_keyvals = 10
    num_lookups = 15
    save_to = "command_small.txt"
    keyvalfile = "keyval_small.txt"
    maketest(num_nodes, num_keyvals, num_lookups, save_to, keyvalfile, 
             node_id_length = 8, node_ip_length = 12, node_port_length = 5, 
             key_length = 8, val_length = 16)

