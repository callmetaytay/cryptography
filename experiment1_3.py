import base64, itertools

freq = {
    'a':0.0651738,'b':0.0124248,'c':0.0217339,'d':0.0349835,'e':0.1041442,'f':0.0197881,
    'g':0.0158610,'h':0.0492888,'i':0.0558094,'j':0.0009033,'k':0.0050529,'l':0.0331490,
    'm':0.0202124,'n':0.0564513,'o':0.0596302,'p':0.0137645,'q':0.0008606,'r':0.0497563,
    's':0.0515760,'t':0.0729357,'u':0.0225134,'v':0.0082903,'w':0.0171272,'x':0.0013692,
    'y':0.0145984,'z':0.0007836,' ':0.1918182
}

def score(b):
    return sum(freq.get(chr(x).lower(),0) for x in b)

def xor1(b,k):
    return bytes([x^k for x in b])

def best1(b):
    r=[]
    for k in range(256):
        p=xor1(b,k)
        r.append({'k':k,'s':score(p),'p':p})
    return max(r,key=lambda x:x['s'])

def xorrep(b,k):
    n=len(k)
    return bytes([b[i]^k[i%n] for i in range(len(b))])

def hdist(a,b):
    return sum(bin(x^y).count('1') for x,y in zip(a,b))

def crack(b):
    d={}
    for n in range(2,41):
        c=[b[i:i+n] for i in range(0,len(b),n)][:4]
        t=0
        for x,y in itertools.combinations(c,2):
            t+=hdist(x,y)
        d[n]=t/6/n
    ks=sorted(d,key=d.get)[:3]
    print(ks)
    res=[]
    for n in ks:
        k=b''
        for i in range(n):
            blk=b[i::n]
            k+=bytes([best1(blk)['k']])
        res.append((xorrep(b,k),k))
    return max(res,key=lambda x:score(x[0]))

with open("ciphertext.txt") as f:
    data=base64.b64decode(f.read())
out=crack(data)
print("The Key is",out[1].decode())
print("The Length is",len(out[1].decode()))
print(out[0].decode().rstrip())
