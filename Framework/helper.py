import random
import string



def get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def get_random_digits(length, key_base):
    """generate a binary number of certain length and convert it to a string in certain base
    only supports base 2/8/10/16

    Args:
        length (int): length of the integer in binary
        key_base (int): base used to represent the integer in a string
    """ 
    bin_str = ''.join(random.choice(['0','1']) for _ in range(length))
    
    if key_base == 2:
        base = "b"
    elif key_base == 8:
        base = "o"
    elif key_base == 10:
        base = "d"
    elif key_base == 16:
        base = "x"
    return format(int(bin_str, 2), base)

