class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
import sys
import hashlib
sys.stdout = Unbuffered(sys.stdout)

flag=open("/root/xhash/flag").read()

a=raw_input("filea:")
ma=a.decode("hex")

b=raw_input("fileb:")
mb=b.decode("hex")

if ma[0:3]=="xxx" and mb[0:3]=="xxx" and ma!=mb and hashlib.md5(ma).hexdigest()==hashlib.md5(ma).hexdigest():
    print flag
