# Quantum Leader Election (QLE)

Implementation of the exact quantum leader election algorithm proposed by [Tani et al](https://arxiv.org/abs/0712.4213).

## Prerequisites

* [SimulaQron](http://www.simulaqron.org/)

  Please refer to the [Getting started](https://softwarequtech.github.io/SimulaQron/html/GettingStarted.html) page for installation instructions. Tested with version 2.2.0

* [ProjectQ](https://projectq.ch/)

  Please refer to the [Getting started](https://projectq.readthedocs.io/en/latest/tutorials.html#getting-started) page for installation instructions.

* [Qiskit](https://qiskit.org/)

  Please refer to the [Qiskit Tutorials](https://github.com/Qiskit/qiskit-tutorials/blob/master/INSTALL.md) page for installation instructions.

## Configuration

1. Clone the *exact-qle* folder.

2. Configure SimulaQron with the following commands:
   - simulaqron set backend projectq
   - simulaqron set nodes-file *path*/exact-qle/config/Nodes.cfg
   - simulaqron set app-file *path*/exact-qle/config/appNodes.cfg
   - simulaqron set cqc-file *path*/exact-qle/config/cqcNodes.cfg
   - simulaqron set vnode-file *path*/exact-qle/config/virtualNodes.cfg
   - simulaqron set topology-file *path*/exact-qle/config/topology.json
   - simulaqron set max-qubits 40
   - simulaqron set max-registers 100
   - simulaqron set recv-timeout 2.0
   - simulaqron set log-level debug

## Execution

1. Open a first shell and execute:
   ```
   simulaqron start
   ```

2. Open a second shell and execute:
   ```
   *path*/exact-qle/config/run.sh
   ```
