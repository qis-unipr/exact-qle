# Quantum Leader Election (QLE)

Implementation of the exact quantum leader election algorithm proposed by [Tani et al](https://arxiv.org/abs/0712.4213).

## Prerequisites

* [SimulaQron](http://www.simulaqron.org/)

  Please refer to the [Getting started](https://softwarequtech.github.io/SimulaQron/html/GettingStarted.html) page for installation instructions.
  
  Tested with the Develop version.

* [ProjectQ](https://projectq.ch/)

  Please refer to the [Getting started](https://projectq.readthedocs.io/en/latest/tutorials.html#getting-started) page for installation instructions.

* [Qiskit](https://qiskit.org/)

  Please refer to the [Qiskit Tutorials](https://github.com/Qiskit/qiskit-tutorials/blob/master/INSTALL.md) page for installation instructions.

## Installing

1. Clone the *exact-qle* folder in: *SimulaQron/examples/cdc/pythonLib*.

2. Enter in: *SimulaQron/config* and edit the following files:
   - *appNodes.cfg*
   - *cqcNodes.cfg*
   - *virtualNodes.cfg*

   in order to set the number of virtual nodes and CQC servers (node0, node1, node2, ...).
   
   Note: you also need to set the number of nodes using the 'n' variable in the main function of the *qlenode.py* file.
   
   In the same folder edit the *settings.ini* file in order to set the maximum number of qubits per node. For example:
   ```
   maxqubits_per_node = 1000
   ```
   
3. Move the *myStarter.sh* file to *SimulaQron/run*.

## Running

1. Open a first shell and execute:
   ```
   cd SimulaQron/run
   sh myStarter.sh
   ```

2. Open a second shell and execute:
   ```
   cd examples/cqc/pythonLib/exact-qle
   sh run.sh
   ```