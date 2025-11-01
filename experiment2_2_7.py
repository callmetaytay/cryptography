def pad_msg(msg: bytes, blk: int) -> bytes:
    p = blk - len(msg) % blk
    return msg + bytes([p] * p)

def unpad_msg(msg_pad):
    p_len = msg_pad[-1]
    m, p = msg_pad[:-p_len], msg_pad[-p_len:]
    assert all(x == p_len for x in p)
    return m

print(unpad_msg(b"ICE ICE BABY\x04\x04\x04\x04"))
print(unpad_msg(b"ICE ICE BABY\x05\x05\x05\x05"))
