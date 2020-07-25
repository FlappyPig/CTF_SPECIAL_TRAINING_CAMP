from idaapi import *
from idc import *
from idautils import *
start_ea = 0x401000

patterns = [('73 02', 2), ('EB 03', 1), ('72 03 73 01', 1),  ('74 03 75 01', 1), ('7E 03 7F 01', 1), ('74 04 75 02', 2)]

for pattern in patterns:
    ea = start_ea
    while True:
        ea = FindBinary(ea, SEARCH_DOWN, pattern[0])
        if ea == idaapi.BADADDR:
            break
        ea += len(pattern[0].replace(' ', ''))/2

        for i in range(pattern[1]):
            PatchByte(ea+i, 0x90)
            MakeCode(ea+i)
