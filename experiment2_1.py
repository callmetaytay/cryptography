from hashlib import sha1
from base64 import b64decode
from Crypto.Cipher import AES

C0 = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
K0 = '12345678<8<<<1110182<111116?<<<<<<<<<<<<<<<4'

def f1(s):
    s = list(s)
    w = [7,3,1,7,3,1]
    x = 0
    for i in range(21,27):
        x = (x + int(s[i]) * w[i-21]) % 10
    s[27] = str(x)
    return ''.join(s)

def f2(s):
    v = s[:10] + s[13:20] + s[21:28]
    h = sha1(v.encode()).hexdigest()
    return h[:32]

def f3(s):
    r = []
    b = bin(int(s,16))[2:]
    for i in range(0,len(b),8):
        r.append(b[i:i+7])
        if b[i:i+7].count('1') % 2 == 0:
            r.append('1')
        else:
            r.append('0')
    return hex(int(''.join(r),2))[2:]

def f4(s):
    s = s + '00000001'
    h = sha1(bytes.fromhex(s)).hexdigest()
    return f3(h[:16]) + f3(h[16:32])

def f5(c,k):
    c = b64decode(c)
    aes = AES.new(bytes.fromhex(k), AES.MODE_CBC, bytes.fromhex('0'*32))
    return aes.decrypt(c).decode()

if __name__ == '__main__':
    K0 = f1(K0)
    K1 = f2(K0)
    K2 = f4(K1)
    P0 = f5(C0,K2)
    print(P0)
