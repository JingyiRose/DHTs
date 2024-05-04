import random
from helper import *
import os




def maketest_hotcold(num_cold_nodes, num_cold_keys, cmd_length,  p_nodejoin, p_insertkey, p_lookups, 
                     cold_fname, hot_fname, keyvalfile, node_id_length = 8, node_ip_length = 12, 
                     node_port_length = 5, key_length = 8, val_length = 16, contact = False):
    # generate sequence of operations stored in txt file
    # need to specify number of keys, nodes, and (random) lookups
    if os.path.exists(cold_fname):
        os.remove(cold_fname)
    if os.path.exists(hot_fname):
        os.remove(hot_fname)
    # if os.path.exists(keyvalfile):
    #     os.remove(keyvalfile)

    fcold = open(cold_fname, 'w')

    node_ids = []
    keys = []

    for _ in range(num_cold_nodes):
        id = get_random_string(node_id_length)
        ip = get_random_string(node_ip_length)
        port = get_random_digits(node_port_length)
        contact_node = None
        fcold.write('nodejoin id={}, ip={}, port={}, contact_node={}\n'.format(id, ip, port, contact_node))
        node_ids.append(id)
    
    for _ in range(num_cold_keys):
        key = get_random_digits(key_length)
        val = get_random_digits(val_length)
        fcold.write('insert key={}, val={}\n'.format(key, val))
        keys.append(key)

    fcold.close() 

    fhot = open(hot_fname, 'w') 

    for _ in range(cmd_length):
        p = random.random()
        if p < p_nodejoin:
            id = get_random_string(node_id_length)
            ip = get_random_string(node_ip_length)
            port = get_random_digits(node_port_length)
            contact_node = random.choice(node_ids)
            node_ids.append(id)
            fhot.write('nodejoin id={}, ip={}, port={}, contact_node={}\n'.format(id, ip, port, contact_node))

        if p_nodejoin < p and p < p_nodejoin+p_insertkey:
            key = get_random_digits(key_length)
            val = get_random_digits(val_length)
            fhot.write('insert key={}, val={}\n'.format(key, val))
            keys.append(key)


        if p_nodejoin+p_insertkey < p:
            request_node = random.choice(node_ids)
            destination_key = random.choice(keys)
            fhot.write('look-up localnode={}, key={}\n'.format(request_node, destination_key))
                     
    fhot.close()
    return



if __name__ == '__main__':
    num_cold_nodes = 10
    num_cold_keys = 0
    cmd_length = 5
    p_nodejoin = 1
    p_insertkey = 0
    p_lookups = 0
    cold_fname = "cold_n{}_k{}.txt".format(num_cold_nodes, num_cold_keys)
    hot_fname =  "hot{}.txt".format(cmd_length)
    keyvalfile = "empty.txt"
    maketest_hotcold(num_cold_nodes, num_cold_keys, cmd_length,  p_nodejoin, p_insertkey, p_lookups, 
                     cold_fname, hot_fname, keyvalfile, node_id_length = 8, node_ip_length = 12, 
                     node_port_length = 5, key_length = 8, val_length = 16, contact = False)


