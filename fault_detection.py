import numpy as np
from scipy.stats import chi2
from qiskit import transpile
from qiskit_aer import AerSimulator

def fault_free_simulation(qc, shots):
    
    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled, shots=shots).result()
    return result.get_counts()

def fault_detection(fault_model, qc, distribution, maximum_test_escape, maximum_overkill):
    total_shots = int(sum(distribution.values()))
    expected_counts = fault_free_simulation(qc, total_shots)

    all_outcomes = sorted(set(distribution.keys()) | set(expected_counts.keys()))
    observed = np.array([distribution.get(o, 0) for o in all_outcomes], dtype=float)
    expected = np.array([expected_counts.get(o, 0) for o in all_outcomes], dtype=float)

    eps = 1e-6
    expected = np.where(expected < eps, eps, expected)

    chi2_stat = np.sum((observed - expected) ** 2 / expected)
    df = len(all_outcomes) - 1

    if fault_model is None:
        # 正常情況：應該不被偵測，避免 overkill（false positive）
        threshold = chi2.ppf(1 - maximum_overkill, df)
    else:
        # 故障情況：應該被偵測，避免 test escape（false negative）
        threshold = chi2.ppf(maximum_test_escape, df)
    is_detected = chi2_stat > threshold
    return is_detected

# Example usage
if __name__ == "__main__":
    from Fault_model import myFault_1, myFault_2, myFault_3
    from qiskit import QuantumCircuit
    # Load a test circuit
    qc_1 = QuantumCircuit.from_qasm_file("C:\\Users\\user\\OneDrive\\桌面\\NTUEE大三下\\qATG-main\\student\\benchmarks\\qc1.qasm")
    qc_2 = QuantumCircuit.from_qasm_file("C:\\Users\\user\\OneDrive\\桌面\\NTUEE大三下\\qATG-main\\student\\benchmarks\\qc2.qasm")# Simulated faulty distribution (from your fault_simulation)
    from fault_simulation import fault_simulation
    dist1_1 = fault_simulation(myFault_1(), qc_1, 100000)
    dist1_2 = fault_simulation(myFault_1(), qc_2, 100000)
    dist2_1 = fault_simulation(myFault_2(), qc_1, 100000)
    dist2_2 = fault_simulation(myFault_2(), qc_2, 100000)
    dist3_1 = fault_simulation(myFault_3(), qc_1, 100000)
    dist3_2 = fault_simulation(myFault_3(), qc_2, 100000)
    dist0_1 = fault_free_simulation(qc_1, 100000)
    dist0_2 = fault_free_simulation(qc_2, 100000)
    detected1_1 = fault_detection(myFault_1(), qc_1, dist1_1, maximum_test_escape=0.05, maximum_overkill=0.05)
    detected1_2 = fault_detection(myFault_1(), qc_2, dist1_2, maximum_test_escape=0.05, maximum_overkill=0.05)
    detected2_1 = fault_detection(myFault_2(), qc_1, dist2_1, maximum_test_escape=0.05, maximum_overkill=0.05)
    detected2_2 = fault_detection(myFault_2(), qc_2, dist2_2, maximum_test_escape=0.05, maximum_overkill=0.05)
    detected3_1 = fault_detection(myFault_3(), qc_1, dist3_1, maximum_test_escape=0.05, maximum_overkill=0.05)
    detected3_2 = fault_detection(myFault_3(), qc_2, dist3_2, maximum_test_escape=0.05, maximum_overkill=0.05)
    detected0_1 = fault_detection(None, qc_1, dist0_1, maximum_test_escape=0.05, maximum_overkill=0.05)
    detected0_2 = fault_detection(None, qc_2, dist0_2, maximum_test_escape=0.05, maximum_overkill=0.05)
    print("Fault detected?", detected1_1)
    print("Fault detected?", detected1_2)
    print("Fault detected?", detected2_1)
    print("Fault detected?", detected2_2)
    print("Fault detected?", detected3_1)
    print("Fault detected?", detected3_2)
    print("Fault-free qc1 detected?", detected0_1)
    print("Fault-free qc2 detected?", detected0_2)

    