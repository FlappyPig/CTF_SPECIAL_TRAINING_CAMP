from zio import *
with open('./ciphertext') as f:
d = f.read()

flag = ''
for i in range(len(d)):
    for c in range(0x21, 0x80):
        try_input = flag + chr(c)
        io = zio('./cipher')
        io.writeline(try_input)
        io.close()
        f = open('./out', 'rb')
        d2 = f.read()
        if d2[i] == d[i]:
            flag += chr(c)
            break
print flag
