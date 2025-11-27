import gmpy2

def grab(NN):
    x = 3
    k = 2
    while True:
        x = gmpy2.powmod(x, k, NN)
        g = gmpy2.gcd(x - 1, NN)
        if g != 1 and g != NN:
            return g, NN // g
        k += 1

def h2t(s):
    return bytes.fromhex(s).decode("utf-8")

with open("Frame19") as f:
    buf = f.read()

modu = int(buf[:256], 16)
exp  = int(buf[256:512], 16)
enc  = int(buf[512:], 16)

pp, qq = grab(modu)
print("pp=", hex(pp))
print("qq=", hex(qq))

tot = (pp - 1) * (qq - 1)
dd = gmpy2.invert(exp, tot)
print("dd=", hex(dd))

msg = gmpy2.powmod(enc, dd, modu)
print("msg=", hex(msg))

seg = hex(msg)[-16:]
print(h2t(seg))
