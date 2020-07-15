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
flag=open("/root/xbitf/flag","r").read()

from Crypto.Cipher import AES
import os

def aes_cbc(key,iv,m):
    handler=AES.new(key,AES.MODE_CBC,iv)
    return handler.encrypt(m).encode("hex")
def aes_cbc_dec(key,iv,c):
    handler=AES.new(key,AES.MODE_CBC,iv)
    return handler.decrypt(c.decode("hex"))

key=os.urandom(16)
iv=os.urandom(16)
session=os.urandom(8)
token="session="+session.encode("hex")+";admin=0"
checksum=aes_cbc(key,iv,token)
print token+";checksum="+checksum
for i in range(10):
    token_rcv=raw_input("token:")
    if token_rcv.split("admin=")[1][0]=='1' and token_rcv.split("session=")[1][0:16].decode("hex")==session:
        c_rcv=token_rcv.split("checksum=")[1].strip()
        m_rcv=aes_cbc_dec(key,iv,c_rcv)
        print m_rcv
        if m_rcv.split("admin=")[1][0]=='1':
            print flag
