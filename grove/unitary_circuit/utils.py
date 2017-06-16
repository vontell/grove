from pyquil.gates import X, NOT, CNOT, CCNOT
from grove.grover.grover import n_qubit_control
import numpy as np

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

# product by n bit controlled not with qubits controls and scratch bit as the target
def and_all(p, qubits):
    if len(qubits) == 0:
        return p.alloc()
    scratch_bit = p.alloc()
    control_prog = n_qubit_control(qubits, scratch_bit, np.array([[0, 1], [1, 0]]), 'NOT')
    p.inst(control_prog)
    p.defined_gates = control_prog.defined_gates
    return p, scratch_bit

# summation by successive CNOTs on every qubit to a target scratch bit
def or_all(p, qubits):
    if len(qubits) == 0:
        print("or all zero qubits")
        return p.alloc()
    scratch_bit = p.alloc()
    for qubit in qubits:
        p.inst(CNOT(qubit, scratch_bit))
    return scratch_bit

# Using the basic algorithm found here: https://s2.smu.edu/~mitch/class/8381/papers/MMD-DAC03.pdf
# assume qubits are ordered from most significant to least significant
def add_reversible_function(p, f, qubits):
    """
    Add a gate that simulates a reversible function to program p
    :param p: program to add gates to
    :param f: for n := len(qubits), f is a one-to-one mapping of {0,1}^n -> {0,1}^n
    :param qubits: input qubits, from most to least significant
    :return: output qubits, to be measured
    """
    n = len(qubits)
    rev_qubits = qubits[::-1]
    mappings = {x: f(x) for x in xrange(2**n)}
    #print "Initial mappings: ", mappings

    gates = []
    all_ones = 2**n - 1
    not_array = np.array([[0, 1], [1, 0]])
    not_name = "NOT"
    unique_gates = set()
    #debug = []
    for i in xrange(n):
        # if the i-th bit is a 1
        if not not(mappings[0] & (1 << i)):
            gates.append(X(rev_qubits[i]))
            #debug.append("X " + str(i))
            for x in xrange(2**n):
                mappings[x] = mappings[x] ^ 2**i

    for x in xrange(1, 2**n):
        if mappings[x] == x:
            continue
        p_controls = set()
        p_targets = set()
        q_controls = set()
        q_targets = set()
        for i in xrange(n):
            # if the ith digit in x is a 1
            if (not not (x & (1 << i))):
                q_controls.add(i)
                # if the ith digit in f'(x) is a 0
                if (not (mappings[x] & (1 << i))):
                    p_targets.add(i)
            # if the ith digit in f'(x) is a 1
            if (not not (mappings[x] & (1 << i))):
                p_controls.add(i)
                # if the ith digit in x is a 0
                if (not (x & (1 << i))):
                    q_targets.add(i)
        p_qubit_controls = map(lambda j: rev_qubits[j], p_controls)
        p_and_mask = reduce(lambda prev, new: prev + (1 << new), p_controls, 0)
        p_or_mask = p_and_mask ^ all_ones
        for y in xrange(x, 2**n):
            if all_ones == ((mappings[y] & p_and_mask) | p_or_mask):
                mappings[y] = mappings[y] ^ sum(map(lambda j: 1 << j, p_targets))
        for p_target in p_targets:
            n_toffoli = n_qubit_control(p_qubit_controls, rev_qubits[p_target], not_array, not_name)
            unique_gates |= set(n_toffoli.defined_gates)
            #debug.append("TOFF Ctrl: " + ", ".join(list(map(str, p_controls))) + " Tar: " + str(p_target))
            gates.append(n_toffoli)

        q_qubit_controls = map(lambda j: rev_qubits[j], q_controls)
        q_and_mask = reduce(lambda prev, new: prev + (1 << new), q_controls, 0)
        q_or_mask = q_and_mask ^ all_ones
        for y in xrange(x, 2**n):
            if all_ones == (mappings[y] & q_and_mask) | q_or_mask:
                mappings[y] = mappings[y] ^ sum(map(lambda j: 1 << j, q_targets))

        for q_target in q_targets:
            n_toffoli = n_qubit_control(q_qubit_controls, rev_qubits[q_target], not_array, not_name)
            unique_gates |= set(n_toffoli.defined_gates)
            #debug.append("TOFF Ctrl " + ", ".join(list(map(str, q_controls))) + " Tar: " + str(q_target))
            gates.append(n_toffoli)

    for gate in gates[::-1]:
        p.inst(gate)
    p.defined_gates = list(unique_gates)
    #print "Final mappings: ", mappings

    #print "\n".join(debug[::-1])
    return p

def add_function(p, f, qubits, num_range_bits):
    outbits = []
    num_qubits = len(qubits)

    for m in xrange(num_range_bits):
        bits_to_or = []
        for x in xrange(2**len(qubits)):
            if (f(x) >> m) % 2 == 0: continue
            bits_to_and = []

            for n in xrange(num_qubits):
                if (x >> n) % 2 == 0:
                    bits_to_and.append(add_cnot(p, qubits[num_qubits - 1 - n]))
                else:
                    bits_to_and.append(qubits[num_qubits - 1 - n])
            p, bit_to_or = and_all(p, bits_to_and)
            bits_to_or.append(bit_to_or)
        if len(bits_to_or) == 0: continue
        outbits.append(or_all(p, bits_to_or))
    outbits.reverse()
    return outbits