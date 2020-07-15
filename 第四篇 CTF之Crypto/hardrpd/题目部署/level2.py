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
import os
os.chdir("/root/level2")

from random import *


while 1:
    a=raw_input("#")
    target=getrandbits(32)
    if a!=str(target):
        print target
    else:
        print open("flag","rb").read()