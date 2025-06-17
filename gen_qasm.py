import numpy as np
from qatg.qatgMain import QATG
from qatg.qatgConfiguration import QATGConfiguration
import qiskit.circuit.library as qGate
from qiskit import QuantumCircuit
from qiskit.qasm2 import dumps
from Fault_model import myFault_1, myFault_2, myFault_3
from IPython.display import display

# QATG generator
generator = QATG(
    circuitSize=2,
    basisSingleQubitGateSet=[qGate.SXGate, qGate.RZGate],
    circuitInitializedStates={
        1: [1, 0],
        2: [1, 0, 0, 0]
    },
    minRequiredStateFidelity=0.1
)
generator.basisGateSetString = ['sx', 'rz']

# faults define
fault_list = [myFault_1, myFault_2, myFault_3]
file_names = ["Sx_test.qasm", "Rz_test.qasm", "Cnot_test.qasm"]

for fault_class, filename in zip(fault_list, file_names):
    fault = fault_class()

    # create config
    config = QATGConfiguration(generator.circuitSetup, generator.simulationSetup, fault)

    # create template
    init_state = generator.circuitInitializedStates[len(fault.getQubits())]
    template, fidelity = generator.generateTestTemplate(faultObject=fault, initialState=init_state)
    config.setTemplate(template, fidelity)
    config.simulate()
    # save as qasm
    qasm_str = dumps(config.circuit)
    qasm_path = f"C:\\Users\\user\\OneDrive\\桌面\\NTUEE大三下\\qATG-main\\s{filename}"
    with open(qasm_path, 'w') as f:
        f.write(qasm_str)
    print(f" {filename} 儲存完成")

    # print
    print(f" Fault: {type(fault).__name__}")
    print(config)
    display(config.circuit.draw())