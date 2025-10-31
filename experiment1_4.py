import hashlib, itertools, time

TARGET = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"
SETS = [['Q','q'], ['W','w'], ['5','%'], ['8','('], ['=','0'], ['I','i'], ['*','+'], ['n','N']]

def sha1_hex(s):
    return hashlib.sha1(s.encode()).hexdigest()

t0 = time.time()
base = list("00000000")
for a in range(2):
    base[0] = SETS[0][a]
    for b in range(2):
        base[1] = SETS[1][b]
        for c in range(2):
            base[2] = SETS[2][c]
            for d in range(2):
                base[3] = SETS[3][d]
                for e in range(2):
                    base[4] = SETS[4][e]
                    for f in range(2):
                        base[5] = SETS[5][f]
                        for g in range(2):
                            base[6] = SETS[6][g]
                            for h in range(2):
                                base[7] = SETS[7][h]
                                s = "".join(base)
                                for perm in itertools.permutations(s, 8):
                                    cand = "".join(perm)
                                    if sha1_hex(cand) == TARGET:
                                        print("password:", cand)
                                        print("time:", time.time() - t0)
                                        raise SystemExit
