a=open("pre_msg1.txt","rb").read()
b=open("pre_msg2.txt","rb").read()

from zio import *
import base64
import time
import random
target=("106.14.204.93",5004)

io=zio(target)
io.read_until("filea:")
io.writeline(a.encode("hex"))
io.read_until("fileb:")
io.writeline(b.encode("hex"))
io.interact()