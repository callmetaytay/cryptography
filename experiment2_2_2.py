from Crypto.Cipher import AES
from base64 import b64decode

def pad_msg(m: bytes, n: int) -> bytes:
    p = n - len(m) % n
    return m + bytes([p] * p)

def unpad_msg(m: bytes) -> bytes:
    p = m[-1]
    return m[:-p]

def ecb_enc(pt: bytes, k: bytes) -> bytes:
    c = AES.new(k, AES.MODE_ECB)
    return c.encrypt(pad_msg(pt, AES.block_size))

def ecb_dec(ct: bytes, k: bytes) -> bytes:
    c = AES.new(k, AES.MODE_ECB)
    return c.decrypt(ct)

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def cbc_enc(pt: bytes, k: bytes, iv: bytes) -> bytes:
    out = b''
    prev = iv
    pt = pad_msg(pt, AES.block_size)
    for i in range(0, len(pt), AES.block_size):
        blk = pt[i:i+AES.block_size]
        x = xor_bytes(blk, prev)
        y = ecb_enc(x, k)
        out += y
        prev = y
    return out

def cbc_dec(ct: bytes, k: bytes, iv: bytes) -> bytes:
    out = b''
    prev = iv
    for i in range(0, len(ct), AES.block_size):
        blk = ct[i:i+AES.block_size]
        x = ecb_dec(blk, k)
        y = xor_bytes(x, prev)
        out += y
        prev = blk
    return out

v = b'\x00' * AES.block_size
k = b'YELLOW SUBMARINE'
with open('10.txt') as f:
    data = b64decode(f.read())
print(cbc_dec(data, k, v).decode().rstrip())
