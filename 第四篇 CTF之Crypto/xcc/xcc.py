class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
import sys
sys.stdout = Unbuffered(sys.stdout)
#import signal
#signal.alarm(600)

import random
import time
flag=open("/root/xcc/flag","r").read()

from Crypto.Cipher import AES
import os

def aes_cbc(key,iv,m):
    handler=AES.new(key,AES.MODE_CBC,iv)
    return handler.encrypt(m).encode("hex")
def aes_cbc_dec(key,iv,c):
    handler=AES.new(key,AES.MODE_CBC,iv)
    return handler.decrypt(c.decode("hex"))

key=os.urandom(16)
iv=flag

for i in range(10):
    c=raw_input("c:")
    print aes_cbc_dec(key,iv,c).encode("hex")