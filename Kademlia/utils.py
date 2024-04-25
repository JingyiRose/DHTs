"""Helper functions that are reused by Kademlia Module
"""

from config import *
import re



def xor_base10(key1: str, key2: str):
    """find the XOR distance of two keys. Yield answer in base 10
    """
    return int(key1, KEY_BASE) ^ int(key2, KEY_BASE)



def xor_base2_str(key1: str, key2: str):
    """find the XOR distance of two keys. Yield answer in base 2 string
    """
    distance = int(key1, KEY_BASE) ^ int(key2, KEY_BASE)
    # e.g. f'{14:#b}', f'{14:b}' yields ('0b1110', '1110')
    # Note the string is empty if distance is 0 (we strip the leading 0s)
    return re.sub('^0', '', f'{distance:b}')







def test_XOR():
    key1, key2 = str(int("1001", 2)), str(int("1011", 2))
    assert xor_base10(key1, key2) == int("0010", 2)
    key1, key2 = "0", "300"
    assert xor_base10(key1, key2) == 300
    key1, key2 = "123", "123"
    assert xor_base10(key1, key2) == 0


    key1, key2 = str(int("011", 2)), str(int("01", 2))
    assert xor_base2_str(key1, key2) == "10"
    key1, key2 = "0", "3"
    assert xor_base2_str(key1, key2) == "11"
    key1, key2 = "123", "123"
    assert xor_base2_str(key1, key2) == ""
    print("test_XOR finished")

if __name__ == '__main__':
    test_XOR()
    
