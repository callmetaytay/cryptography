def pad_msg(msg: bytes, size: int) -> bytes:
    p = size - len(msg) % size
    return msg + bytes([p] * p)

def unpad_msg(msg: bytes) -> bytes:
    p = msg[-1]
    return msg[:-p]

m = pad_msg(b'YELLOW SUBMARINE', 16)
print(m)
print(unpad_msg(m))
