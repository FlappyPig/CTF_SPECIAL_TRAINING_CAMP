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
import signal
signal.alarm(600)

import random
import time
flag=open("/root/level0/flag","r").read()

random.seed(int(time.time()))
def check():
    recv=int(raw_input())
    if recv==random.randint(0,2**64):
        print flag
        return True
    else:
        print "atum tql"
        return False

while 1:
    if check():
        break