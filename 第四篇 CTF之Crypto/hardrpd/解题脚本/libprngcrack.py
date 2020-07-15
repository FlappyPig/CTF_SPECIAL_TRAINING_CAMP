import subprocess
import random

def sign(iv):
    # converts a 32 bit uint to a 32 bit signed int
    if(iv&0x80000000):
        iv = -0x100000000 + iv
    return iv
def crack_prng(outputs_624_list):
    get_in=[]
    for i in outputs_624_list:
        get_in.append(sign(i))

    o = subprocess.check_output(["java", "Main"] + map(str, get_in))
    stateList = [int(s) % (2 ** 32) for s in o.split()]
    r = random.Random()
    state = (3, tuple(stateList + [624]), None)
    r.setstate(state)
    return r

'''
r=crack_prng([...])
#r.getrandbits(32)
'''
