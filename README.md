# QATG: Quantum Automatic Test Generation

This repository implements an Automatic Test Pattern Generation (ATPG) system for quantum circuits using Qiskit. The tool is based on the qATG framework and supports fault modeling, test generation, fault simulation, and fault detection using χ² tests.

---

## Project Structure

qatg-main/
│
├── qatg/ # Core QATG source code
├── student/
│ ├── CUTs/ # Encrypted circuit under test (.pyc)
│ └── benchmarks/ # Reference quantum circuits (qc1.qasm, qc2.qasm)
├── test_configs/ # Auto-generated QASM test patterns
├── fault_detection.py # Chi-square fault detection logic
├── fault_simulation.py # Simulates faulty output distributions
├── Fault_model.py # Defines fault models (myFault_1, 2, 3)
├── gen_qasm.py # Generates test templates from faults
├── test_runner.py # End-to-end simulation + detection execution
├── requirements.txt # Python package dependencies
└── README.md # You are here!

---

## How to Run

### 1. Clone and setup environment
```bash
git clone https://github.com/boyuleentu/QDA_Final.git
cd qatg-main
python -m venv venv-qatg
source venv-qatg/bin/activate  # On Windows: venv-qatg\Scripts\activate

### 2. Generate test QASM files
python gen_qasm.py
### 3. Run the full test flow
python test_runner.py

#######
Fault Models
We implement 3 types of single-location fault models:

myFault_1: Fault on RX gate
myFault_2: CX gate coupling fault
myFault_3: Combined RX-CX-RX composite fault
#######
Fault Detection
The tool performs detection by:
Running the fault_simulation to get actual output distribution.
Running fault-free simulation using Qiskit's Aer simulator.
Performing a Pearson χ² test on the two distributions.

You can configure:
maximum_overkill (false positive rate)
maximum_test_escape (false negative tolerance)
#######
Contact
For questions, please reach out to:

[B11901074@ntu.edu.tw]
NTUEE QDA Course, 2025 Spring