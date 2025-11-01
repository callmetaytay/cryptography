import Crypto.Cipher.AES as AES
import os

K = os.urandom(16)

def pad_msg(msg: bytes, blk: int) -> bytes:
    p = blk - len(msg) % blk
    return msg + bytes([p] * p)

def unpad_msg(pad_msg_bytes):
    p_len = pad_msg_bytes[-1]
    m, p = pad_msg_bytes[:-p_len], pad_msg_bytes[-p_len:]
    assert all(x == p_len for x in p)
    return m

def cbc_encrypt(user_bytes: bytes):
    data = (
        b"comment1=cooking MCs;userdata="
        + user_bytes.replace(b";", b"%3B").replace(b"=", b"%3D")
        + b";comment2= like a pound of bacon"
    )
    return AES.new(K, AES.MODE_CBC, os.urandom(16)).encrypt(pad_msg((b"\x00" * 16) + data, 16))

def cbc_decrypt(ct_bytes: bytes):
    data = unpad_msg(AES.new(K, AES.MODE_CBC, os.urandom(16)).decrypt(ct_bytes))[16:]
    return {(kv := item.split(b"=", maxsplit=1))[0].decode(): kv[1] for item in data.split(b";")}

def check_admin(ct_bytes: bytes):
    dec = cbc_decrypt(ct_bytes)
    return dec.get("admin") == b"true"

p_len = 2
ud = b"A" * p_len + b":admin<true"
ct = bytearray(cbc_encrypt(ud))
ct[p_len + 30] ^= ord(":") ^ ord(";")
ct[p_len + 36] ^= ord("<") ^ ord("=")
if check_admin(ct):
    print("Success!")
else:
    print("Fail!")
