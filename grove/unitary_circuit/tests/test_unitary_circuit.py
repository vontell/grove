"""Utils for Black Box Algorithm."""

import pyquil.quil as pq
from pyquil.gates import *
import numpy as np
from pyquil.gates import CCNOT
from grove.unitary_circuit.utils import *
from pyquil.forest import Connection

def try_and_or():
    p = pq.Program()
    q1 = p.alloc()
    q2 = p.alloc()
    p.inst(X(q1))
    sb = add_or(p, q1, q2)
    print p.out()

    cxn = Connection()
    result = cxn.run_and_measure(p, [q.index() for q in [q1, q2, sb]])
    print result

if __name__=='__main__':
    p = pq.Program()
    q1 = p.alloc()
    q2 = p.alloc()
    p.inst(X(q2))

    f = [0, 1, 1, 0]
    num_range_bits = 1
    outbits = add_function(p, lambda x: f[x], [q2, q1], 1)
    print p.out()

    cxn = Connection()
    result = cxn.run_and_measure(p, [q.index() for q in outbits])
    print result