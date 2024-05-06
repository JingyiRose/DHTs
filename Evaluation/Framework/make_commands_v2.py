import random
from Framework.helper import *
import os
# from config import *

# random.seed(43)


# def maketest(num_nodes, num_keyvals, num_lookups, save_to, keyvalfile, 
#              node_id_length = KEY_RANGE, node_ip_length = 12, node_port_length = 5, 
#              key_length = KEY_RANGE, val_length = 16):
#     # generate sequence of operations stored in txt file
#     # need to specify number of keys, nodes, and (random) lookups
#     if os.path.exists(save_to):
#         os.remove(save_to)
#     if os.path.exists(keyvalfile):
#         os.remove(keyvalfile)
#     node_ids = [get_random_digits(node_id_length, KEY_BASE) for _ in range(num_nodes)]
#     node_ips = [get_random_string(node_ip_length) for _ in range(num_nodes)]
#     node_ports = [get_random_digits(node_port_length, KEY_BASE) for _ in range(num_nodes)]

#     keys = [get_random_digits(key_length, KEY_BASE) for _ in range(num_keyvals)]
#     vals = [get_random_digits(val_length, KEY_BASE) for _ in range(num_keyvals)]

#     f1 = open(keyvalfile, 'w')
#     for i in range(num_keyvals):
#         f1.write('({},{})\n'.format(keys[i], vals[i]))
#     f1.close()

#     f2 = open(save_to, 'w')


#     for i in range(num_nodes):
#         f2.write('nodejoin id={}, ip={}, port={}\n'.format(node_ids[i], node_ips[i], node_ports[i]))

#     insert_at_nodes = random.choices(node_ids, k = num_keyvals)
#     for i in range(num_keyvals):
#         # f2.write('insert key={}, val={}\n'.format(keys[i], vals[i]))
#         f2.write('insert localnode={}, key={}, val={}\n'.format(insert_at_nodes[i], keys[i], vals[i]))

#     request_nodes = random.choices(node_ids, k = num_lookups)
#     destination_keys = random.choices(keys, k = num_lookups)
    
#     for i in range(num_lookups):
#         f2.write('look-up localnode={}, key={}\n'.format(request_nodes[i], destination_keys[i]))
#     f2.close()
#     return


def maketest_v2(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                start_filename, normal_ops_filename, node_id_length = 8, node_ip_length = 12, 
                node_port_length = 5, key_length = 8, key_base = 2, val_length = 16, stable_start = True):
    # generate sequence of operations stored in txt file
    # need to specify number of keys, nodes, and (random) lookups
    if os.path.exists(start_filename):
        os.remove(start_filename)
    if os.path.exists(normal_ops_filename):
        os.remove(normal_ops_filename)



    node_ids = []
    keys = []

    if stable_start:
        f = open(start_filename, 'w')
        for _ in range(num_start_nodes):
            id = get_random_digits(node_id_length, key_base)
            ip = get_random_string(node_ip_length)
            port = get_random_digits(node_port_length, key_base)
            f.write('nodejoin id={}, ip={}, port={}\n'.format(id, ip, port))
            node_ids.append(id)
        for _ in range(num_start_keys):
            local_node = None
            key = get_random_digits(key_length, key_base)
            val = get_random_digits(val_length, key_base)
            f.write('insert localnode={}, key={}, val={}\n'.format(local_node, key, val))
            keys.append(key) 
        f.close()

    f = open(normal_ops_filename, 'w')

    for _ in range(num_ops):
        p = random.random()
        if p < p_nodejoin:
            id = get_random_digits(node_id_length, key_base)
            ip = get_random_string(node_ip_length)
            port = get_random_digits(node_port_length, key_base)
            f.write('nodejoin id={}, ip={}, port={}\n'.format(id, ip, port))
            node_ids.append(id)

        if p_nodejoin < p and p < p_nodejoin+p_insertkey:
            local_node = random.choice(node_ids)
            key = get_random_digits(key_length, key_base)
            val = get_random_digits(val_length, key_base)
            f.write('insert localnode={}, key={}, val={}\n'.format(local_node, key, val))
            keys.append(key)


        if p_nodejoin+p_insertkey < p:
            request_node = random.choice(node_ids)
            destination_key = random.choice(keys)
            f.write('look-up localnode={}, key={}\n'.format(request_node, destination_key))

    f.close()

    # for i in range(num_nodes):
    #     f2.write('nodejoin id={}, ip={}, port={}\n'.format(node_ids[i], node_ips[i], node_ports[i]))

    # insert_at_nodes = random.choices(node_ids, k = num_keyvals)
    # for i in range(num_keyvals):
    #     # f2.write('insert key={}, val={}\n'.format(keys[i], vals[i]))
    #     f2.write('insert localnode={}, key={}, val={}\n'.format(insert_at_nodes[i], keys[i], vals[i]))

    # request_nodes = random.choices(node_ids, k = num_lookups)
    # destination_keys = random.choices(keys, k = num_lookups)
    
    # for i in range(num_lookups):
    #     f2.write('look-up localnode={}, key={}\n'.format(request_nodes[i], destination_keys[i]))
    # f2.close()
    return

def hsh(x):
    return int(str(x),2)


def maketest_v2_biased(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                start_filename, normal_ops_filename, node_id_length = 8, node_ip_length = 12, 
                node_port_length = 5, key_length = 8, key_base = 2, val_length = 16, stable_start = True,
                left_bias = None):
    # generate sequence of operations stored in txt file
    # need to specify number of keys, nodes, and (random) lookups
    if os.path.exists(start_filename):
        os.remove(start_filename)
    if os.path.exists(normal_ops_filename):
        os.remove(normal_ops_filename)



    node_ids = []
    keys = []

    if stable_start:
        f = open(start_filename, 'w')
        for _ in range(num_start_nodes):
            id = get_random_digits(node_id_length, key_base)
            ip = get_random_string(node_ip_length)
            port = get_random_digits(node_port_length, key_base)
            f.write('nodejoin id={}, ip={}, port={}\n'.format(id, ip, port))
            node_ids.append(id)
        for _ in range(num_start_keys):
            local_node = None
            key = get_random_digits(key_length, key_base)
            val = get_random_digits(val_length, key_base)
            f.write('insert localnode={}, key={}, val={}\n'.format(local_node, key, val))
            keys.append(key) 
        f.close()

    f = open(normal_ops_filename, 'w')

    for _ in range(num_ops):
        p = random.random()
        if p < p_nodejoin:
            id = get_random_digits(node_id_length, key_base)
            ip = get_random_string(node_ip_length)
            port = get_random_digits(node_port_length, key_base)
            f.write('nodejoin id={}, ip={}, port={}\n'.format(id, ip, port))
            node_ids.append(id)

        if p_nodejoin < p and p < p_nodejoin+p_insertkey:
            local_node = random.choice(node_ids)
            key = get_random_digits(key_length, key_base)
            val = get_random_digits(val_length, key_base)
            f.write('insert localnode={}, key={}, val={}\n'.format(local_node, key, val))
            keys.append(key)


        if p_nodejoin+p_insertkey < p:
            request_node = random.choice(node_ids)
            # print([hsh(x) for x in keys])
            # print(hsh(request_node))
            keys.sort(key = lambda x: ((hsh(request_node) -hsh(x)-1) % (2**key_length)))
            # print(keys)
            # print([hsh(x) for x in keys])
            if left_bias:
                if random.random() < left_bias:
                    destination_key = random.choice(keys[:len(keys)//2])
                else:
                    destination_key = random.choice(keys)
            else:
                destination_key = random.choice(keys)


            f.write('look-up localnode={}, key={}\n'.format(request_node, destination_key))

    f.close()

if __name__ == '__main__':
    num_start_nodes = 5
    num_start_keys = 10
    num_ops = 5
    p_nodejoin = 0.1
    p_insertkey = 0.4
    p_lookups = 0.5
    left_bias = 0.99
    start_filename = "init_bias.txt"
    normal_ops_filename = "normal_ops_bias.txt"
    


    num_nodes = 5
    num_keyvals = 10
    num_lookups = 15
    stable_start = True

    maketest_v2_biased(num_start_nodes, num_start_keys, num_ops,  p_nodejoin, p_insertkey, p_lookups, 
                start_filename, normal_ops_filename, node_id_length = 8, node_ip_length = 12, 
                node_port_length = 5, key_length = 8, key_base= 2, val_length = 16, stable_start=stable_start, left_bias = left_bias)
