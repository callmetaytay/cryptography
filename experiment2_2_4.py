import base64, os, string
import Crypto.Cipher.AES as AES

def pad_msg(msg: bytes, blk: int) -> bytes:
    p = blk - len(msg) % blk
    return msg + bytes([p] * p)

def unpad_msg(msg: bytes) -> bytes:
    p = msg[-1]
    return msg[:-p]

def oracle_ecb(user: bytes) -> bytes:
    k = os.urandom(16)
    suf = base64.b64decode(
b"""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""")
    pt = pad_msg(user + suf, 16)
    return AES.new(k, AES.MODE_ECB).encrypt(pt)

base_len = len(oracle_ecb(b""))
target_len = base_len
for n in range(16):
    if len(oracle_ecb(b"A" * n)) != base_len:
        target_len = base_len - n
        break

alphabet = string.printable.encode()

def recover(prefix: bytes):
    while True:
        block_tail = prefix[-15:]
        block_tail = b"\x00" * (15 - len(block_tail)) + block_tail
        cand_list = []
        for ch in alphabet:
            probe = block_tail + bytes([ch]) + b"\x00" * (15 - len(prefix) % 16)
            ct = oracle_ecb(probe)
            if ct[15] == ct[len(prefix) // 16 * 16 + 31]:
                cand_list.append(ch)
        if len(cand_list) == 1:
            prefix += bytes(cand_list)
            if len(prefix) == target_len:
                print(prefix.decode())
                return True
            continue
        elif len(cand_list) == 0:
            return False
        else:
            for c in cand_list:
                if recover(prefix + bytes([c])):
                    return True

recover(b'')
