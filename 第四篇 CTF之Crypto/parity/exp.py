from zio import *
target=("106.14.204.93",5003)

io=zio(target,timeout=10000,print_read=COLORED(NONE,'red'),print_write=COLORED(NONE,'green'))

n=int(io.readline().strip())
c=int(io.readline().strip())

def getjo(num):
    io.read_until("c:")
    io.writeline(str(num))
    return int(io.readline().strip())

e=65537
lb = 0
ub = n
k = n.bit_length()
for i in range(k):
    c = (c * pow(2, e, n)) % n
    if getjo(c)==1:
        lb = (lb+ub)/2
    else:
        ub = (lb+ub)/2
    print hex(lb),hex(ub)

io.interact()