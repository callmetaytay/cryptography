from Crypto.Cipher import AES
from Crypto import Random

def pad_msg(msg: bytes, blk: int) -> bytes:
    p = blk - len(msg) % blk
    return msg + bytes([p] * p)

def unpad_msg(msg: bytes) -> bytes:
    p = msg[-1]
    return msg[:-p]

def ecb_encrypt(pt: bytes, k: bytes) -> bytes:
    c = AES.new(k, AES.MODE_ECB)
    return c.encrypt(pad_msg(pt, AES.block_size))

def ecb_decrypt(ct: bytes, k: bytes) -> bytes:
    c = AES.new(k, AES.MODE_ECB)
    return c.decrypt(ct)

def make_profile(email: str) -> dict:
    s = email.replace('&', '').replace('=', '')
    return {'email': s, 'uid': 10, 'role': 'user'}

def kv_encode(obj: dict) -> str:
    out = ''
    for k, v in obj.items():
        out += k + '=' + str(v) + '&'
    return out[:-1]

def kv_decode(s: str) -> dict:
    d = {}
    for pair in s.split('&'):
        k, v = pair.split('=')
        d[k] = v
    return d

class ECBOracle:
    def __init__(self):
        self._key = Random.new().read(AES.key_size[0])
    def encrypt(self, email: str) -> bytes:
        data = kv_encode(make_profile(email)).encode()
        return ecb_encrypt(data, self._key)
    def decrypt(self, ct: bytes) -> bytes:
        return unpad_msg(ecb_decrypt(ct, self._key))

def attack_cut_and_paste(oracle: ECBOracle) -> bytes:
    pre_len = AES.block_size - len('email=')
    suf_len = AES.block_size - len('admin')
    e1 = 'x' * pre_len + 'admin' + (chr(suf_len) * suf_len)
    ct1 = oracle.encrypt(e1)
    e2 = "master@xd.com"
    ct2 = oracle.encrypt(e2)
    return ct2[:32] + ct1[16:32]

oracle = ECBOracle()
ct = attack_cut_and_paste(oracle)
dec = oracle.decrypt(ct).decode()
result = kv_decode(dec)
print(result)
