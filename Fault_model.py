import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import SXGate, RZGate, RYGate, RXGate, CXGate, UnitaryGate
from qiskit.quantum_info import Operator
from qatg.qatgFault import QATGFault
# Fault 1: SX + undesired RZ drift
class myFault_1(QATGFault):
    def __init__(self):
        super().__init__(SXGate, 0, "SX + RZ(π/20)")
        self.target_gate_class = SXGate
        self.target_qubits = [0]
    def createOriginalGate(self):
        return SXGate()

    def createFaultyGate(self, faultfreeGate):
        qc = QuantumCircuit(1)
        qc.sx(0)
        qc.rz(np.pi / 20, 0)  
        mat = Operator(qc).data
        return UnitaryGate(mat, label="SX+RZdrift")


# Fault 2: RZ + Ry(0.1θ)
class myFault_2(QATGFault):
    def __init__(self):
        super().__init__(RZGate, 0, "RZ + RY(0.1θ)")
        self.target_gate_class = RZGate
        self.target_qubits = [0]
    def createOriginalGate(self):
        return RZGate(np.pi / 2)

    def createFaultyGate(self, faultfreeGate):
        θ = faultfreeGate.params[0]
        qc = QuantumCircuit(1)
        qc.rz(θ, 0)
        qc.ry(0.1 * θ, 0)
        mat = Operator(qc).data
        return UnitaryGate(mat, label="RZ+RY(0.1θ)")

# Fault 3: RX-RX sandwiching CNOT
class myFault_3(QATGFault):
    def __init__(self):
        super().__init__(CXGate, [0, 1], "RX sandwich CX")
        self.target_gate_class = CXGate
        self.target_qubits = [0, 1]
    def createOriginalGate(self):
        return CXGate()

    def createFaultyGate(self, faultfreeGate):
        qc = QuantumCircuit(2)
        qc.append(RXGate(0.1 * np.pi), [0])
        qc.append(CXGate(), [0, 1])
        qc.append(RXGate(-0.1 * np.pi), [0])
        mat = Operator(qc).data
        return UnitaryGate(mat, label="RX-CX-RX")
