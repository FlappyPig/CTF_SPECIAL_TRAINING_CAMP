from zio import *

def get_byte():
    global pc, mem
    ret = ord(mem[pc])
    pc += 1
    return ret

def get_dword():
    global pc, mem
    ret = l32(mem[pc:pc+4])
    pc += 4
    return ret

def disasm():
    global pc, mem
    while pc < len(mem):
        real_pc = pc
        opcode = get_byte()

        size = (opcode >> 6) & 3
        opcode = opcode & 0x3f

        if opcode == 0:
            print '%08x: initvm' %real_pc
            break
        elif opcode == 1:
            if size == 0:
                reg1_index = get_byte()
                reg2_index = get_byte()
                print '%08x: mov reg%d, reg%d' % (real_pc, reg1_index, reg2_index)
            else:
                reg1_index = get_byte()
                imm = get_dword()
                print '%08x: mov reg%d, %08x' % (real_pc, reg1_index, imm)
        elif opcode == 2:
            reg1_index = get_byte()
            reg2_index = get_byte()
            size_dict = {0: 'byte', 1: 'word', 2: 'dword'}
            print '%08x: mov reg%d, %s [reg%d]' % (real_pc, reg1_index, size_dict[size], reg2_index)
        elif opcode == 3:
            reg1_index = get_byte()
            reg2_index = get_byte()
            size_dict = {0: 'byte', 1: 'word', 2: 'dword'}
            print '%08x: mov %s [reg%d], reg%d' % (real_pc, size_dict[size], reg2_index, reg1_index)
        elif (opcode == 4) | (opcode == 5):
            reg1_index = get_byte()
            mnemonic_dict = {4: 'pop', 5: 'push'}
            print '%08x: %s reg%d' %(real_pc, mnemonic_dict[opcode], reg1_index)
        elif (opcode == 6) | (opcode == 7):
            mnemonic_dict = {6: 'printf', 7: 'scanf'}
            reg1_index = get_byte()
            if size == 0:
                print '%08x: %s reg%d #c' %(real_pc, mnemonic_dict[opcode], reg1_index)
            elif size == 1:
                print '%08x: %s reg%d #d' %(real_pc, mnemonic_dict[opcode], reg1_index)
            elif size == 2:
                print '%08x: %s reg%d #x' %(real_pc, mnemonic_dict[opcode], reg1_index)
            elif size == 3:
                print '%08x: %s byte [reg%d]' %(real_pc, mnemonic_dict[opcode], reg1_index)
        elif opcode == 8:
            print '%08x: ret' %real_pc
        elif opcode == 9:
            imm = get_dword()
            jcc_mnemonic_dict = {0: 'jmp', 1: 'jz', 2: 'jnz', 3: 'jl'}
            print '%08x: %s %08x' %(real_pc, jcc_mnemonic_dict[size], imm)
        elif opcode == 10:
            reg1_index = get_byte()
            jcc_mnemonic_dict = {0: 'jmp', 1: 'jz', 2: 'jnz', 3: 'jl'}
            print '%08x: %s reg%d' %(real_pc, jcc_mnemonic_dict[size], reg1_index)
        elif (opcode >= 11)&(opcode <=16):
            mnemonic_dict = {11: 'add', 12: 'sub', 13: 'and', 14: 'or', 15: 'xor', 16: 'cmp'}
            reg1_index = get_byte()
            if size == 0:
                reg2_index = get_byte()
                print '%08x: %s reg%d, reg%d' %(real_pc, mnemonic_dict[opcode], reg1_index, reg2_index)
            else:
                imm = get_dword()
                print '%08x: %s reg%d, %08x' %(real_pc, mnemonic_dict[opcode], reg1_index, imm)
        elif opcode == 17:
            print '%08x: ret' %real_pc
        elif opcode == 18:
            reg1_index = get_byte()
            reg2_index = get_byte()
            size_dict = {0: 'byte', 1: 'word', 2: 'dword'}
            print '%08x: mov reg%d, %s[reg%d]' %(real_pc, reg1_index, size_dict[size], reg2_index)
        elif opcode == 19:
            reg1_index = get_byte()
            reg2_index = get_byte()
            if size == 0:
                print '%08x: mov byte[reg%d], reg%d' %(real_pc, reg2_index, reg1_index)
            elif size == 1:
                print '%08x: mov word[reg%d], reg%d' %(real_pc, reg2_index, reg1_index)
            elif size == 2:
                print '%08x: mov dword[reg%d], reg%d' %(real_pc, reg2_index, reg1_index)
        elif opcode == 20:
            if size == 0:
                reg1_index = get_byte()
                print '%08x: call reg%d' %(real_pc, reg1_index)
            else:
                imm = get_dword()
                print '%08x: call %08x' %(real_pc, imm)
        elif opcode == 21:
            print '%08x: nop' %real_pc
        elif (opcode == 22) | (opcode == 23):
            mnemonic_dict = {22: 'inc', 23: 'dec'}
            reg1_index = get_byte()
            print '%08x: %s reg%d' %(real_pc, mnemonic_dict[opcode], reg1_index)
        elif opcode == 24:
            reg1_index = get_byte()
            reg2_index = get_byte()
            print '%08x: test reg%d, reg%d' %(real_pc, reg1_index, reg2_index)
        else:
            print 'invalid opcode:%x' %opcode
            raise Exception('error')

pc = 0
with open('input.bin', 'rb') as f:
    mem = f.read()
disasm()
