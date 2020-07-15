from zio import *
target=("106.14.204.93",5002)

io=zio(target)

getlist=[]
for i in range(624):
    print i
    io.read_until("#")
    io.writeline("1")
    getlist.append(int(io.readline().strip()))

import libprngcrack
r=libprngcrack.crack_prng(getlist)
io.read_until("#")
io.writeline(str(r.getrandbits(32)))
io.interact()