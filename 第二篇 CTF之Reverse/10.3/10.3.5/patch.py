from zio import *

def ul(v):
  return v & 0xFFFFFFFF

def retea(ct, key):
    res=''
    v0 = l32(ct[0:4])
    v1 = l32(ct[4:8])
    sum = 0x1bbcdc80

    for i in range(128):
        v1 = ul(v1-((v0+sum)^(16*v0+key[2])^((v0>>5)+key[3])))
        v0 = ul(v0-((v1+sum)^(16*v1+key[0])^((v1>>5)+key[1])))
        sum = ul(sum - 0x9e3779b9)
        
    res = '%08x%08x' %(v0, v1)
    return res

with open('./debug', 'rb') as f:
    datas = f.read()[0x7030:0x7030+0x10]

d2 = ''.join(chr(ord(d)^0x31) for d in datas)

key = [0x112233,0x44556677,0x8899aabb,0xccddeeff]
flag = retea(d2[0:8], key)
flag += retea(d2[8:16], key)

print flag
