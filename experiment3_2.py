import random
from math import gcd
from sympy import mod_inverse

def is_p(x):
    if x <= 1:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    for i in range(3, int(x ** 0.5) + 1, 2):
        if x % i == 0:
            return False
    return True

def gen_p(bits=16):
    while True:
        v = random.getrandbits(bits)
        if is_p(v):
            return v

def gen_keys(bits=16):
    while True:
        a = gen_p(bits)
        b = gen_p(bits)
        while a == b:
            b = gen_p(bits)
        n = a * b
        t = (a - 1) * (b - 1)
        k = 3
        if gcd(k, t) == 1:
            break
    r = mod_inverse(k, t)
    return (k, n), (r, n)

def enc(msg, pub):
    k, n = pub
    return [pow(ord(ch), k, n) for ch in msg]

def dec(cip, priv):
    r, n = priv
    return ''.join(chr(pow(x, r, n)) for x in cip)

def run():
    pub, priv = gen_keys(bits=16)
    print("public ", pub)
    print("private ", priv)
    s = "cryptography"
    c = enc(s, pub)
    print("encrypto ", c)
    p = dec(c, priv)
    print("decrypto ", p)

run()
