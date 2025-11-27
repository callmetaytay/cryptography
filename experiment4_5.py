import gmpy2

def gg(a, b):
    if b == 0:
        return a
    return gg(b, a % b)

def h2s(x):
    return bytes.fromhex(x).decode("utf-8")

with open("Frame1") as f:
    t = f.read()
    nA = int(t[:256], 16)
    eA = int(t[256:512], 16)
    cA = int(t[512:], 16)

with open("Frame18") as f:
    t = f.read()
    nB = int(t[:256], 16)
    eB = int(t[256:512], 16)
    cB = int(t[512:], 16)

p = gg(nA, nB)

qA = nA // p
phiA = (p - 1) * (qA - 1)
dA = gmpy2.invert(eA, phiA)
mA = pow(cA, dA, nA)
hxA = hex(mA)
print(hxA)
print(h2s(hxA[-16:]))

qB = nB // p
phiB = (p - 1) * (qB - 1)
dB = gmpy2.invert(eB, phiB)
mB = pow(cB, dB, nB)
hxB = hex(mB)
print(hxB)
print(h2s(hxB[-16:]))
