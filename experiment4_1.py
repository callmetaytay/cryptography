import gmpy2

def crackN(x):
    t = gmpy2.iroot(x, 2)[0]
    while True:
        t += 1
        diff = t*t - x
        if gmpy2.is_square(diff):
            dd = gmpy2.mpz(diff)
            r, ok = gmpy2.iroot(dd, 2)
            assert ok
            return (t - r, t + r)

def h2s(h):
    return bytes.fromhex(h).decode("utf-8")

with open("Frame10", "r") as f:
    data = f.read()

mod = int(data[:256], 16)
ee  = int(data[256:512], 16)
cc  = int(data[512:], 16)

pp, qq = crackN(mod)
print("pp =", hex(pp))
print("qq =", hex(qq))

phi = (pp - 1) * (qq - 1)
dd = gmpy2.invert(ee, phi)
print("dd =", hex(dd))

mm = gmpy2.powmod(cc, dd, mod)
print("mm =", hex(mm))

seg = hex(mm)[-16:]
print(h2s(seg))
