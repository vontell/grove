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

def test_two_bit_to_one_bit():
    p = pq.Program()
    q1 = p.alloc()
    q2 = p.alloc()
    p.inst(X(q2))

    f = [0, 1, 1, 0]
    num_range_bits = 1
    outbits = add_function(p, lambda x: f[x], [q2, q1], num_range_bits)
    print p.out()
    print len(p.get_qubits())

    cxn = Connection()
    result = cxn.run_and_measure(p, [q.index() for q in outbits])
    print result

def test_three_to_three():
    """
    Currently doesn't run cuz too many qubits
    :return:
    """
    p = pq.Program()
    q1 = p.alloc()
    q2 = p.alloc()
    q3 = p.alloc()
    p.inst(X(q2))
    p.inst(X(q1))

    f = [0, 1, 2, 3, 4, 5, 6, 7]
    num_range_bits = 3
    outbits = add_function(p, lambda x: f[x], [q3, q2, q1], num_range_bits)
    print p.out()
    print len(p.get_qubits())

    # cxn = Connection()
    # result = cxn.run_and_measure(p, [q.index() for q in outbits])
    # print result

if __name__=='__main__':
    test_two_bit_to_one_bit()