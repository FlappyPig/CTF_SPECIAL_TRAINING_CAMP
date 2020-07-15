from Crypto.Util.number import getPrime,bytes_to_long
import primefac

p=getPrime(512)
q=getPrime(512)

n=p*q

d=getPrime(10)

e=primefac.modinv(d,(p-1)*(q-1)) % ((p-1)*(q-1))

flag="flag{wnwnwnwnweifnjiowenfoiwenf}"
m=bytes_to_long(flag)

print "c=",pow(m,e,n)
print "e=",e
print "n=",n