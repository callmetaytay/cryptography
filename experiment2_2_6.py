import base64, os, random, string
import Crypto.Cipher.AES as AES

rnd_pre_len = random.randint(0, 64)
rnd_pre = os.urandom(rnd_pre_len)

def pad_msg(msg: bytes, blk: int) -> bytes:
    p = blk - len(msg) % blk
    return msg + bytes([p] * p)

def unpad_msg(msg: bytes) -> bytes:
    p = msg[-1]
    return msg[:-p]

def ecb_oracle(user: bytes) -> bytes:
    k = os.urandom(16)
    suf = base64.b64decode(
b"""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""")
    pt = pad_msg(rnd_pre + user + suf, 16)
    return AES.new(k, AES.MODE_ECB).encrypt(pt)

def compute_unknown_info():
    base_len = len(ecb_oracle(b""))
    unk_len = base_len
    for n in range(16):
        if len(ecb_oracle(b"A" * n)) != base_len:
            unk_len = base_len - n
            break
    left = 0
    while True:
        left += 1
        ct = ecb_oracle(b"A" * left)
        blks = [ct[i:i+16] for i in range(0, len(ct), 16)]
        for i in range(len(blks) - 1):
            if blks[i] == blks[i+1]:
                return unk_len - i * 16 + left % 16, i * 16, left % 16

unknown_length, start_offset, pad_mod = compute_unknown_info()
pad_zeros = b"\x00" * pad_mod

alphabet = string.printable.encode()

def recover(prefix: bytes):
    while True:
        tail = prefix[-15:]
        tail = b"\x00" * (15 - len(tail)) + tail
        candidates = []
        for ch in alphabet:
            probe = pad_zeros + tail + bytes([ch]) + b"\x00" * (15 - len(prefix) % 16)
            ct = ecb_oracle(probe)[start_offset:]
            if ct[15] == ct[len(prefix) // 16 * 16 + 31]:
                candidates.append(ch)
        if len(candidates) == 1:
            prefix += bytes(candidates)
            if len(prefix) == unknown_length:
                print(prefix.decode())
                return True
            continue
        elif len(candidates) == 0:
            return False
        else:
            for c in candidates:
                if recover(prefix + bytes([c])):
                    return True

recover(b"")
