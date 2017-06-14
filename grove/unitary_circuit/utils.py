from pyquil.gates import X, CNOT, CCNOT

def add_nand(p, qubit1, qubit2):
    scratch_bit = p.alloc()
    p.inst(X(scratch_bit))
    p.inst(CCNOT(qubit1, qubit2, scratch_bit))

    return scratch_bit

def add_and(p, qubit1, qubit2):
    sb = add_nand(p, qubit1, qubit2)
    return add_nand(p, sb, sb)

def add_or(p, qubit1, qubit2):
    sb1 = add_nand(p, qubit1, qubit1)
    sb2 = add_nand(p, qubit2, qubit2)
    return add_nand(p, sb1, sb2)

def add_cnot(p, qubit):
    scratch_bit = p.alloc()
    p.inst(X(scratch_bit))
    p.inst(CNOT(qubit, scratch_bit))
    return scratch_bit

def and_all(p, qubits):
    if len(qubits) < 2: raise ValueError("qubits must be at least size 2")
    return reduce(lambda prev, new: add_and(p, prev, new), qubits)

def or_all(p, qubits):
    if len(qubits) < 2: raise ValueError("qubits must be at least size 2")
    return reduce(lambda prev, new: add_or(p, prev, new), qubits)

# assume qubits are ordered from most significant to least significant

def add_function(p, f, qubits, num_range_bits):
    outbits = []
    for m in xrange(num_range_bits):
        print "Range bit #", m
        num_qubits = len(qubits)
        bits_to_or = []
        for x in xrange(2**len(qubits)):
            print "Domain number", x
            if (f(x) >> m) % 2 == 0: continue
            bits_to_and = []

            for n in xrange(len(qubits)):
                if (x >> n) % 2 == 0:
                    bits_to_and.append(add_cnot(p, qubits[num_qubits - 1 - n]))
                else:
                    bits_to_and.append(qubits[num_qubits - 1 - n])
            bits_to_or.append(and_all(p, bits_to_and))
        outbits.append(or_all(p, bits_to_or))
    outbits.reverse()
    return outbits