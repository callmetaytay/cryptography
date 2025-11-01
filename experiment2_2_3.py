import os
import random
import Crypto.Cipher.AES as AES

def gen_key():
    return os.urandom(16)

def gen_pad():
    return os.urandom(random.randint(5, 10))

def pad_msg(m: bytes, n: int) -> bytes:
    p = n - len(m) % n
    return m + bytes([p] * p)

def unpad_msg(m: bytes) -> bytes:
    p = m[-1]
    return m[:-p]

def enc_oracle(k, m):
    mode = random.choice([AES.MODE_ECB, AES.MODE_CBC])
    data = gen_pad() + m + gen_pad()
    data = pad_msg(data, 16)
    match mode:
        case AES.MODE_ECB:
            return AES.new(k, mode).encrypt(data), mode
        case AES.MODE_CBC:
            iv = gen_key()
            return AES.new(k, mode, iv).encrypt(data), mode
    assert False

def detect_mode(ct):
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
    if len(blocks) != len(set(blocks)):
        return AES.MODE_ECB
    return AES.MODE_CBC

k = gen_key()
m = b'\x00' * 48
enc = [enc_oracle(k, m) for _ in range(1000)]
acc = sum(detect_mode(c) == md for c, md in enc)
print(f"{acc / len(enc):.2%}")
