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

#flag=open("/root/parity/flag","r").read()
flag="\x11\x11\x11\x11"
from Crypto.Util.number import getPrime,long_to_bytes,bytes_to_long
import primefac

p=getPrime(512)
q=getPrime(512)
n=p*q
e=65537
m=bytes_to_long(flag)
c=pow(m,e,n)

print n
print c

d=primefac.modinv(e,(p-1)*(q-1)) % ((p-1)*(q-1))

while 1:
    getc=raw_input("c:")
    getcc=int(getc)
    getm=pow(getcc,d,n)
    print getm%2