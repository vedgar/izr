import itertools, collections, sys, pdb, typing

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
            yield '_' if tape[i] == machine.space else tape[i]
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
Q = {'q0/'}
Sigma = {'●', '/'}
Gamma = set(Sigma) | set('{}()[]>○_...')
space = '_'

def rule(q1, a1, q2=None, a2=None, d=1):
    if q2 is None: q2 = q1
    if a2 is None: a2 = a1
    assert q1 in Q
    Q.add(q2)
    assert {a1, a2} <= Gamma
    assert d in {-1, 1}
    assert (q1, a1) not in delta
    delta[q1, a1] = q2, a2, d


k=3
rule('q0/', '●', 'q1●', '[')
rule('q0/', '/', 'q1/')
for i in range(1, k-1):
    rule('q' + str(i) + '●', '●')
    rule('q' + str(i) + '●', '/', 'q' + str(i) + '/', '●')
    rule('q' + str(i) + '/', '/', 'q' + str(i+1) + '/')
    rule('q' + str(i) + '/', '●', 'q' + str(i+1) + '●', '/')
rule('q' + str(k-1) + '/', '●', 'q' + str(k) + '●', '/')
rule('q' + str(k-1) + '/', space, 'q1', '/')
rule('q' + str(k) + '●', '●')
rule('q' + str(k) + '●', space, 'q1', '●')
rule('q1', space, 'q2', ']')
rule('q2', space, 'q3', '>')

M = TuringMachine(Q, Sigma, Gamma, space, delta, 'q0/', 'q3')

M.simulate('●●●//●', debug=False)
