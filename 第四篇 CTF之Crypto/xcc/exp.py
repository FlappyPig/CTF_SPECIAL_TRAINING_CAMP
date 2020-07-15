from zio import *

def cbc_chosen_cipher_recover_iv(cc,mm):
    assert cc[0:16]==cc[16:32]
    def _xorstr(a, b):
        s = ""
        for i in range(16):
            s += chr(ord(a[i]) ^ ord(b[i]))
        return s
    p0=mm[0:16]
    p1=mm[16:32]
    return _xorstr(_xorstr(p0, p1), cc[0:16])



target=("106.14.204.93",5005)
io=zio(target)
io.read_until("c:")
io.writeline(("1"*32).encode("hex"))
mm=io.readline().strip().decode("hex")
iv=cbc_chosen_cipher_recover_iv("1"*32,mm)
print iv
io.interact()