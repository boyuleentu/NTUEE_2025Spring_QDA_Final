from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from Fault_model import myFault_1, myFault_2, myFault_3
from copy import deepcopy

def fault_simulation(fault_model, qc: QuantumCircuit, shots: int) -> dict:
    
    # Deep copy to avoid mutating the original circuit
    faulty_qc = deepcopy(qc)
    injected = False

    # Replace matching gate
    for idx, instr in enumerate(faulty_qc.data):
        gate = instr.operation
        # Determine the qubit indices for this instruction
        qubit_indices = [faulty_qc.qubits.index(q) for q in instr.qubits]

        # Match by class and qubit positions
        if isinstance(gate, fault_model.target_gate_class) and qubit_indices == fault_model.target_qubits:
            # Create the faulty gate and replace
            faulty_gate = fault_model.createFaultyGate(gate)
            faulty_qc.data[idx] = (faulty_gate, instr.qubits, instr.clbits)
            injected = True

    
    if not injected and fault_model is not None:
        print(f"Warning: No matching gate found for {fault_model.__class__.__name__}")

    
    if not any(inst.operation.name == "measure" for inst in faulty_qc.data):
        faulty_qc.measure_all()

    # Simulate
    sim = AerSimulator()
    compiled = transpile(faulty_qc, sim)
    result = sim.run(compiled, shots=shots).result()
    return result.get_counts()

if __name__ == "__main__":
    from qiskit import QuantumCircuit
    shots = 100_000

    
    qc1 = QuantumCircuit.from_qasm_file("C:/Users/boyulee/Desktop/QDA/qATG-main/student/benchmarks/qc1.qasm")
    qc2 = QuantumCircuit.from_qasm_file("C:/Users/boyulee/Desktop/QDA/qATG-main/student/benchmarks/qc2.qasm")

    faults = [None, myFault_1(), myFault_2(), myFault_3()]
    names  = ["Fault-free", "Fault 1", "Fault 2", "Fault 3"]

    def run_all(qc, label):
        print(f"\\n{label} results:")
        for f, n in zip(faults, names):
            if f is None:
                sim = AerSimulator()
                comp = transpile(qc, sim)
                res = sim.run(comp, shots=shots).result().get_counts()
            else:
                res = fault_simulation(f, qc, shots)
            print(f"{n}: {res}")

    run_all(qc1, "qc1.qasm")
    run_all(qc2, "qc2.qasm")

