def eg(a, b):
    if b == 0:
        return 1, 0, a
    u, v, g = eg(b, a % b)
    return v, u - (a // b) * v, g

def h2s(t):
    return bytes.fromhex(t).decode("utf-8")

with open("Frame0") as f:
    txt = f.read()
    nA = int(txt[:256], 16)
    eA = int(txt[256:512], 16)
    cA = int(txt[512:], 16)

with open("Frame4") as f:
    txt = f.read()
    nB = int(txt[:256], 16)
    eB = int(txt[256:512], 16)
    cB = int(txt[512:], 16)

u, v, g = eg(eA, eB)

res = (pow(cA, u, nA) * pow(cB, v, nB)) % nA
print(hex(res))
print(h2s(hex(res)[-16:]))
