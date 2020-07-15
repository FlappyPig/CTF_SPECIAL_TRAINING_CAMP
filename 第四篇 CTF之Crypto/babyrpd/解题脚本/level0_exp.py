from zio import *
import time
import random
target=("106.14.204.93",5000)

io=zio(target)


def getstream(times):
    for i in range(times-1):
        random.randint(0, 2 ** 64)
    return random.randint(0, 2 ** 64)

times=0
now=int(time.time())+10
while 1:
    now-=1
    times+=1
    seed=random.seed(now)
    print 1
    io.writeline(str(getstream(times)))
    if "atum" not in io.readline():
        break
