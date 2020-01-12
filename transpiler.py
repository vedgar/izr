import itertools, collections, sys, pdb, typing
INC, DEC, GOTO = range(3)

test = 5
if test == 1:
    eSigma = 'abcde'
    P = [
        (0, DEC, 1, 1),
        (1, DEC, 1, 8),
        (2, DEC, 1, 8),
        (3, DEC, 1, 8),
        (4, DEC, 1, 8),
        (5, DEC, 1, 8),
        (6, INC, 0),
        (7, GOTO, 1),
    ]
    word = 'deda'
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
    word = '21'
elif test == 4:
    eSigma = '*'
    P = []
    word = '********'
elif test == 5:
    eSigma = 'xy'
    P = [
        (0, INC, 0),
        (1, DEC, 1, 3),
        (2, GOTO, 0),
    ]
    word = 'xyxyy'

class TuringMachine(typing.NamedTuple):
    states: set
    alphabet: set
    work_alphabet: set
    space: str
    transition: dict
    initial: str
    final: str

    def simulate(machine, input, debug=True):
        q, pos = machine.initial, 0
        tape = collections.defaultdict(lambda: machine.space, enumerate(input))
        machine.show(q, pos, tape, 0)
        visited, steps = set(), 0
        states = []
        try:
            while q != machine.final:
                q, tape[pos], d = machine.transition[q, tape[pos]]
                pos = max(pos + d, 0)
                steps += 1
                if debug and q not in visited:
                    if len(states) > 1:
                        statnum = 0
                        for statkey, statgroup in itertools.groupby(states[1:]):
                            statcount = sum(1 for stat in statgroup)
                            print(statkey.replace(machine.space, '_'), end='')
                            if statcount > 1: print('*', statcount, end=' ', sep='')
                            else: print(end=' ')
                            statnum += 1
                            if statnum > 99: print(end='...'); break
                        print()
                    states.clear()
                    machine.show(q, pos, tape, steps)
                    visited.add(q)
                states.append(q)
            machine.show(q, pos, tape, steps)
        except KeyError as exc:
            machine.show(q, pos, tape, steps)
            print(repr(exc), file=sys.stderr)

    def show_gen(machine, q, pos, tape, steps):
        while tape and tape[max(tape)] == machine.space: del tape[max(tape)]
        yield str(steps) + ': '
        for i in range(2 + max(tape, default=0)):
            if i == pos: yield q.replace(machine.space,'_').join('(>')
            yield '_' if tape[i] == machine.space else tape[i].join('[]')
        if tape[max(tape, default=0)] == machine.space:
            del tape[max(tape)]
        yield '...'

    def show(machine, q, pos, tape, steps):
        for key, group in itertools.groupby(machine.show_gen(q, pos, tape, steps)):
            print(end=key)
            count = sum(1 for cell in group)
            if count > 5: print(end='^' + str(count) + ' ')
            else: print(end=key*(count-1))
        print()
delta = {}
Q = {'n$'}
alfa = dict(enumerate(eSigma, 1))
KSigma = {char: num for num, char in alfa.items()}
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

for α, β in itertools.product(['$', *Sigma], {*Sigma, space}):
    rule('n' + α, β, 'n' + β, α)  # (δ1a)
rule('n' + space, space, 'q0', '#', -1)  # (δ1b)

for t in range(2, bc + 1): rule('q0', alfa[t], 'q1', alfa[t-1])  # (δ2a)
for γ in {'$', space}: rule('q0', γ, 'q2')  # (δ2f)
rule('q2', alfa[bc], 'q1', space)  # (δ2g)
for α in Sigma | {'#', r1}: rule('q1', α)  # (δ2b)
rule('q1', space, 'q0', r1, -1)  # (δ2c)
for γ in {r1, '#'}: rule('q0', γ, d=-1)  # (δ2d)
rule('q0', alfa[1], 'q0', alfa[bc], -1)  # (δ2e)
rule('q2', '#', 'p0')  # (δ2h)

for instruction in P:
    i, itype, *iargs = instruction
    pi, si, pi1 = 'p' + str(i), 's' + str(i), 'p' + str(i + 1)
    Q.update({pi, si})
    for γ in Bm: rule(pi, γ, d=-1)  # (δ3a)
    rule(pi, '#', si)  # (δ3b)
    if itype == INC:
        j, = iargs
        mrule(si, '●', j)  # (δ3c)
        mrule(si, '○', j, pi1, '●', -1)  # (δ3d)
    elif itype == DEC:
        j, l = iargs
        ti = 't' + str(i)
        mrule(si, '●', j)  # (δ3e)
        mrule(si, '○', j, ti, d=-1)  # (δ3f)
        rule(ti, '#', 'p' + str(l))  # (δ3g)
        mrule(ti, '●', j, pi1, '○', -1)  # (δ3h)
    elif itype == GOTO:
        l, = iargs
        for γ in Bm: rule(si, γ, 'p' + str(l), γ, -1)  # (δ3i)
    else: assert False

pn = 'p' + str(n)
for γ in {'#'} | Bm - {space}: rule(pn, γ)  # (δ4a)
rule(pn, space, 'q3', '$', -1)  # (δ4b)
for γ in Bm: rule('q3', γ, d=-1)  # (δ4c)
rule('q3', '#', 'q3', space, -1)  # (δ4d)
rule('q3', '$', 'q4')  # (δ4e)
mrule('q4', '○', 0)  # (δ4f)
mrule('q4', '●', 0, 'q5', '○', -1)  # (δ4g)
for γ in Bm: rule('q5', γ, d=-1)  # (δ4h)
rule('q5', alfa[bc], 'q5', alfa[1], -1)  # (δ4i)
for t in range(1, bc): rule('q5', alfa[t], 'q4', alfa[t + 1])  # (δ4j)
rule('q5', '$', 'q6')  # (δ4k)
rule('q6', alfa[1])  # (δ4l)
for γ in Bm: rule('q6', γ, 'q4', alfa[1])  # (δ4m)
rule('q4', alfa[1])  # (δ4m')
rule('q4', '$', 'l' + space, space, -1)  # (δ4n)
for γ in Bm: rule('l' + space, γ, 'l' + space, space, -1)  # (δ4n')

for α, β in itertools.product([space, *Sigma], {*Sigma, '$'}):
    rule('l' + α, β, 'l' + β, α, -1)  # (δ5a)

M = TuringMachine(Q, Sigma, Gamma, space, delta, 'n$', 'l$')
M.simulate(word, debug=True)
