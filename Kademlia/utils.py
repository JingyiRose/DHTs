"""Helper functions that are reused by Kademlia Module
"""

from config import *
import re


def get_first(item_dict:dict, num: int) -> dict:
    """Get the first num elements in the dictionary
    """
    return dict(list(item_dict.items())[:num])

# Helper functions
def sort_contact_dict(contact_dict, key):
    """Sort the dictionary of contacts by proximity to the key
    """
    return dict(sorted(contact_dict.items(), key = lambda x: xor_base10(x[0], key)))


# Bit operations
def flip(bit: str):
    """Flip the bit in base 2
    """
    if bit == '0': return '1'
    if bit == '1': return '0'

def xor_base10(key1: str, key2: str, key_base = KEY_BASE):
    """find the XOR distance of two keys. Yield answer in base 10
    """
    return int(key1, key_base) ^ int(key2, key_base)

def xor_base2_str(key1: str, key2: str, key_base = KEY_BASE):
    """find the XOR distance of two keys. Yield answer in base 2 string
    """
    distance = int(key1, key_base) ^ int(key2, key_base)
    # e.g. f'{14:#b}', f'{14:b}' yields ('0b1110', '1110')
    # Note the string is empty if distance is 0 (we strip the leading 0s)
    return re.sub('^0', '', f'{distance:b}')

def pad(key: str, key_length: int, key_base = KEY_BASE):
    """Pad the key with 0s to make it of length key_length
    """
    return f'{int(key, key_base):0{key_length}b}'


    

if __name__ == '__main__':
    print(pad("1001", 8))
    
