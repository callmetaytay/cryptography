import gmpy2

def gg(a, b):
    if b == 0:
        return a
    return gg(b, a % b)

def splitM(ms, tot):
    r = []
    for v in ms:
        r.append(tot // v)
    return r

def exg(a, b):
    if b == 0:
        return 1, 0, a
    x1, y1, q = exg(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return x, y, q

def invList(bigM, mods):
    arr = []
    for i in range(len(bigM)):
        t = exg(bigM[i], mods[i])[0]
        arr.append((t + mods[i]) % mods[i])
    return arr

def solveCRT(vals, mods):
    for i in range(len(mods)):
        for j in range(i+1, len(mods)):
            if gg(mods[i], mods[j]) != 1:
                return None
    tot = 1
    for m in mods:
        tot *= m
    sub = splitM(mods, tot)
    invs = invList(sub, mods)
    s = 0
    for i in range(len(vals)):
        s += vals[i] * sub[i] * invs[i]
        s %= tot
    rt, ok = gmpy2.iroot(s, 5)
    if ok:
        return rt
    return s

def h2s(h):
    return bytes.fromhex(h).decode("utf-8")

xs = []
mods = []

def readF(fn):
    with open(fn, "r") as f:
        t = f.read()
    nn = int(t[:256], 16)
    ee = int(t[256:512], 16)
    cc = int(t[512:], 16)
    xs.append(cc)
    mods.append(nn)

readF("frame3")
readF("frame8")
readF("frame12")
readF("frame16")
readF("frame20")

out = hex(solveCRT(xs, mods))
print(h2s(out[-16:]))
