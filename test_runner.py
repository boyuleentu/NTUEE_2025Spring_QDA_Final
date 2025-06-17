import os, sys
from subprocess import run, PIPE
from qiskit import QuantumCircuit
from Fault_model import myFault_1, myFault_2, myFault_3
from fault_detection import fault_detection
from qatg.qatgMain import QATG
from qatg.qatgConfiguration import QATGConfiguration
import qiskit.circuit.library as qGate
from qiskit.circuit.library import UnitaryGate
from qiskit.qasm2 import dumps
python_exec = sys.executable
SHOTS = 100000
MAX_ESCAPE = 0.05
MAX_OVERKILL = 0.05

ROOT = os.path.dirname(os.path.abspath(__file__))
CUT_DIR = os.path.join(ROOT, "student", "C:\\Users\\user\\OneDrive\\桌面\\NTUEE大三下\\qATG-main\\student\\CUTs_qATG0.8_py3.10")
OUT_DIR = os.path.join(ROOT, "test_configs")
os.makedirs(OUT_DIR, exist_ok=True)


gen = QATG(
    circuitSize=2,
    basisSingleQubitGateSet=[qGate.SXGate, qGate.RZGate],
    circuitInitializedStates={1:[1,0], 2:[1,0,0,0]},
    minRequiredStateFidelity=0.1
)
gen.basisGateSetString = ['sx','rz']

fault_classes = [myFault_1, myFault_2, myFault_3]
configs = []
for i, FaultClass in enumerate(fault_classes, start=1):
    fault = FaultClass()
    init_state = gen.circuitInitializedStates[len(fault.getQubits())]
    template, fid = gen.generateTestTemplate(fault, initialState=init_state)
    cfg = QATGConfiguration(gen.circuitSetup, gen.simulationSetup, fault)
    cfg.setTemplate(template, fid)
    
    qasm_path = os.path.join(OUT_DIR, f"Test{i}.qasm")
    with open(qasm_path, "w") as f:
        f.write(dumps(cfg.circuit))
    
    print(f"[Generated] {qasm_path}")
    configs.append((qasm_path, fault))

backends = sorted([
    os.path.join(CUT_DIR, f)
    for f in os.listdir(CUT_DIR)
    if f.startswith("backend_") and f.endswith(".pyc")
])

# ==== 執行 encrypted backend ====
def run_backend(pyc_path, qasm_path, shots):
    cmd = [python_exec, pyc_path, qasm_path, str(shots)]
    proc = run(cmd, stdout=PIPE, stderr=PIPE, text=True)
    
    if proc.returncode != 0:
        print(f"=== ERROR in {pyc_path} ===")
        print(proc.stderr)
        sys.exit(1)
    
    try:
        return eval(proc.stdout.strip())
    except Exception as e:
        raise ValueError(f"Invalid backend output from {pyc_path}: {e}")


def main():
    print("Quantum Backend Simulator | Config 1 | Config 2 | Config 3")
    print("--------- | ------ | ------ | ------")
    for idx, backend in enumerate(backends, start=1):
        row = [f"Backend {idx}"]
        for qasm_file, fault in configs:
            dist = run_backend(backend, qasm_file, SHOTS)
            qc = QuantumCircuit.from_qasm_file(qasm_file)
            detected = fault_detection(fault, qc, dist, MAX_ESCAPE, MAX_OVERKILL)
            row.append("Failed" if detected else "Passed")
        print(" | ".join(row))

if __name__ == "__main__":
    main()
