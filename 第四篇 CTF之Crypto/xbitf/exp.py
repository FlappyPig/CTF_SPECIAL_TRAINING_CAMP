from zio import *

def cbc_bit_attack_mul(c,m,position,target):
    l = len(position)
    r=c
    for i in range(l):
        change=position[i]-16
        tmp=chr(ord(m[position[i]])^ord(target[i])^ord(c[change]))
        r=r[0:change]+tmp+r[change+1:]
    return r


target=("106.14.204.93",5009)
io=zio(target)
io.read_until("session=")
session=io.read(16)
io.read_until("checksum=")
c=io.readline().strip()

t1="session="+session+";admin=0"

newchecksum=cbc_bit_attack_mul(c.decode("hex"),t1,[16+16-1],['1'])
io.writeline("session="+session+";admin=1;checksum="+newchecksum.encode("hex"))

io.interact()