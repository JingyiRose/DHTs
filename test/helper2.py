import random
import string



def get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def get_random_digits(length):
    return ''.join(random.choice(string.digits) for _ in range(length))


# def get_random_ip(lenght):
#     ip = ""
#     for i in range(lenght):
#         ip += str(random.randrange(1,10))
#     return ip 


# def get_random_port(lenght):
#     port = ""
#     for i in range(lenght):
#         port += str(random.randrange(1,10))
#     return port 

# def get_random_key(lenght):
#     key = ""
#     for i in range(lenght):
#         port += str(random.randrange(1,10))
#     return key 

# def get_random_val(lenght):
#     val = ""
#     for i in range(lenght):
#         port += str(random.randrange(1,10))
#     return val 

