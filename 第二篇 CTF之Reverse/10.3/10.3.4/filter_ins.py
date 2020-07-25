from idc import *

ips = []
with open('itrace.out', 'rb') as f:
    for line in f:
        ips.append(int(line.strip(), 16))

with open('itrace_asm.out', 'wb') as f:
    for ip in ips:
        if (ip >= 0xDEAD0ED) & (ip < 0xDEAD3AF):
            mnemonic = GetMnem(ip)
            if (mnemonic == 'jmp') | (mnemonic == 'retn'):
                continue
            
            asm = GetDisasm(ip)
            if asm == 'add     rsi, 8':
                continue
            if asm == 'sub     rsi, 8':
                continue
            f.write('%08x %s\n' %(ip, asm)) 
