__author__ = 'ling'

import struct
import os
try:
    import gdb
except ImportError:
    print("Not running inside of GDB, exiting...")
    exit()


class OnBreakpoint(gdb.Breakpoint):
    def __init__(self, loc, callback):
        if isinstance(loc, int):
            loc = '*'+hex(loc)
        super(OnBreakpoint, self).__init__(loc, gdb.BP_BREAKPOINT, internal=False)
        self.callback = callback

    def stop(self):
        self.callback()
        return False

WP_ACCESS = 2
WP_READ = 1
WP_WRITE = 0

class OnHardBreakpoint(gdb.Breakpoint):
    def __init__(self, loc, callback, wp_class=WP_ACCESS):
        if isinstance(loc, int):
            loc = '*'+hex(loc)
        super(OnHardBreakpoint, self).__init__(loc, type=gdb.BP_WATCHPOINT, wp_class=wp_class, internal=False)
        self.callback = callback

    def stop(self):
        self.callback()
        return False


def get_reg(reg):
    #return execute_output('info registers '+reg)
    return int(gdb.parse_and_eval("$"+reg))

def set_reg(reg, value):
    return gdb.execute("set $"+reg+" "+str(value))

def read_mem(address, length):
    inferior = gdb.selected_inferior()
    return inferior.read_memory(address, length)

def write_mem(address, value):
    inferior = gdb.selected_inferior()
    return inferior.write_memory(address, value)

