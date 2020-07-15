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
import os
os.chdir("/root/level1")

flag=open("flag","r").read()

import subprocess
o = subprocess.check_output(["java", "Main"])
tmp=[]
for i in o.split("\n")[0:3]:
    tmp.append(int(i.strip()))


v1=tmp[0] % 0xffffffff
v2=tmp[1] % 0xffffffff
v3=tmp[2] % 0xffffffff
print v1
print v2
v3_get=int(raw_input())
if v3_get==v3:
    print flag