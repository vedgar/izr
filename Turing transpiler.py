import itertools, collections, sys, pdb
INC, DEC, GOTO = range(3)

test = 3
if test == 1:
    eSigma = 'abcde'
    P = [
        (0, DEC, 1, 7),
        (1, DEC, 1, 7),
        (2, DEC, 1, 7),
        (3, DEC, 1, 7),
        (4, DEC, 1, 7),
        (5, INC, 0),
        (6, GOTO, 0),
    ]
    word = 'abab'
elif test == 2:
    eSigma = 'abcde'
    P = [
        (0, DEC, 1, 7),
        (1, INC, 0),
        (2, INC, 0),
        (3, INC, 0),
        (4, INC, 0),
        (5, INC, 0),
        (6, GOTO, 0),
        (7, INC, 0),
    ]
    word = 'ded'
elif test == 3:
    eSigma = '123456789A'
    P = [
        (0, DEC, 1, 4),
        (1, INC, 2),
        (2, INC, 3),
        (3, GOTO, 0),
        (4, DEC, 2, 13),
        (5, DEC, 3, 9),
        (6, INC, 0),
        (7, INC, 4),
        (8, GOTO, 5),
        (9, DEC, 4, 12),
        (10, INC, 3),
        (11, GOTO, 9),
        (12, GOTO, 4),
    ]
    word = '28'
elif test == 4:
    eSigma = '*'
    P = []
    word = '********'
elif test == 5:
    eSigma = 'xy'
    P = [
        (0, INC, 0),
        (1, INC, 2),
        (2, INC, 2),
        (3, INC, 2),
        (4, INC, 0),
        (5, GOTO, 6),
        (6, INC, 2),
    ]
    word = 'xxyxy'

delta = {}
Q = {'q0'}
ISigma = dict(enumerate(eSigma, 1))
KSigma = {char: num for num, char in ISigma.items()}
Sigma = frozenset(KSigma)
bc = len(KSigma)
Gamma = set(Sigma)
assert Gamma.isdisjoint({'#', '$'})
Gamma.update({'#', '$'})
n = len(P)
m = 2
for i, instruction in enumerate(P):
    assert i == instruction[0]
    if instruction[1] in {INC, DEC}:
        register = instruction[2]
        if register >= m: m = register + 1
Bm = set(map(''.join, itertools.product('○●', repeat=m)))
assert Gamma.isdisjoint(Bm)
Gamma.update(Bm)
space = '○' * m
r1 = '○●'.ljust(m, '○')

def rule(q1, a1, q2=None, a2=None, d=1):
    if q2 is None: q2 = q1
    if a2 is None: a2 = a1
    assert q1 in Q
    Q.add(q2)
    assert {a1, a2} <= Gamma and d in {-1, 1} and (q1, a1) not in delta
    delta[q1, a1] = q2, a2, d

def mrule(q1, b1, j, q2=None, b2=None, d=1):
    if b2 is None: b2 = b1
    for rest in itertools.product('○●', repeat=m-1):
        before, after = ''.join(rest[:j]), ''.join(rest[j:])
        rule(q1, before + b1 + after, q2, before + b2 + after, d)

for α in Sigma:
    rule('q0', α, 'n' + α, '$')  # (4.33)
    rule('n' + α, space, 'q1', α)  # (4.35)
rule('q0', space, 'q1', '$')  # (4.36)
for α, αc in itertools.product(Sigma, repeat=2):
    rule('n' + α, αc, 'n' + αc, α)  # (4.34)
rule('q1', space, 'q2', '#', -1)  # (4.37)

for γ in {r1, '#'}: rule('q2', γ, d=-1)  # (4.43)
for γ in {'$', space}: rule('q2', γ, 'q4')  # (4.45)
rule('q4', ISigma[bc], 'q3', space)  # (4.46)
for t in range(2, bc + 1): rule('q2', ISigma[t], 'q3', ISigma[t-1])  # (4.40)
for α in Sigma | {'#', r1}: rule('q3', α)  # (4.41)
rule('q3', space, 'q2', r1, -1)  # (4.42)
rule('q2', ISigma[1], 'q2', ISigma[bc], -1)  # (4.44)
rule('q4', '#', 'p0')  # (4.47)

for instruction in P:
    i = instruction[0]
    pi, si, pi1 = 'p' + str(i), 's' + str(i), 'p' + str(i + 1)
    Q.update({pi, si})
    for γ in Bm: rule(pi, γ, d=-1)  # (4.56)
    rule(pi, '#', si)  # (4.57)
    itype = instruction[1]
    if itype == INC:
        j, = instruction[2:]
        mrule(si, '●', j)  # (4.59)
        mrule(si, '○', j, pi1, '●', -1)  # (4.60)
    elif itype == DEC:
        j, l = instruction[2:]
        ti = 't' + str(i)
        mrule(si, '●', j)  # (4.61)
        mrule(si, '○', j, ti, d=-1)  # (4.62)
        mrule(ti, '●', j, pi1, '○', -1)  # (4.64)
        rule(ti, '#', 'p' + str(l))  # (4.63)
    elif itype == GOTO:
        l, = instruction[2:]
        for γ in Bm: rule(si, γ, 'p' + str(l), γ, -1)  # (4.65)
    else: assert False
pn = 'p' + str(n)
sn = 's' + str(n)
assert pn in Q
for γ in Bm: rule(pn, γ, d=-1)  # (4.56)
rule(pn, '#', sn)  # (4.57)

for γ in Bm - {space}: rule(sn, γ)  # (4.68)
rule(sn, space, 'q5', '$', -1)  # (4.69)
mrule('q5', '○', 0, d=-1)  # (4.70)
for α in Sigma: rule('q5', α, d=-1)  # (4.77)
mrule('q5', '●', 0, 'q6', '○')  # (4.71)
rule('q6', '$', 'q7', d=-1)  # (4.73)
for α in Sigma | Bm: rule('q6', α)  # (4.72)
rule('q7', ISigma[bc], 'q7', ISigma[1], -1)  # (4.74)
for t in range(1, bc): rule('q7', ISigma[t], 'q5', ISigma[t + 1], -1)  # (4.75)
for γ in Bm: rule('q7', γ, 'q5', ISigma[1], -1)  # (4.76)

rule('q5', '#', 'q8', space)  # (4.79)
for γ in Bm: rule('q8', γ, a2=space)  # (4.79)
for α in Sigma:
    rule('q8', α, 'm' + α, space, -1)  # (4.80)
    rule('m' + α, space, d=-1)  # (4.80)
    for αc in Sigma: rule('m' + α, αc, 'l' + α)  # (4.81)
    rule('m' + α, '$', 'q8', α)  # (4.82)
    rule('l' + α, space, 'q8', α)  # (4.82)
rule('q8', '$', 'q9', space, -1)  # (4.83)
rule('q9', space, d=-1)  # (4.83)
rule('q9', '$', 'qz', space, -1)  # (4.85)
for α in Sigma: rule('q9', α, 'qz')  # (4.84)

def show(q, pos, tape, steps):
    while tape and tape[max(tape)] == space: del tape[max(tape)]
    print(end=str(steps) + ':')
    for i in range(2 + max(tape, default=0)):
        if i == pos: print(end=q.join('(>'))
        print(end=tape[i].join('[]'))
    if tape[max(tape, default=0)] == space:
        del tape[max(tape)]
    print('...')
    
def simulate(tape):
    q, pos = 'q0', 0
    tape = collections.defaultdict(lambda: space, enumerate(tape))
    show(q, pos, tape, 0)
    visited, steps = set(), 0
    try:
        while q != 'qz':
            q, tape[pos], d = delta[q, tape[pos]]
            pos = max(pos + d, 0)
            steps += 1
            # if q not in visited: show(q, pos, tape, steps); visited.add(q)
        show(q, pos, tape, steps)
    except KeyError as exc:
        show(q, pos, tape, steps)
        print(repr(exc), file=sys.stderr)

simulate('8')
# 1:81,2:237,3:591,4:1320,5:2568,6:4594,7:7686,8:12180
