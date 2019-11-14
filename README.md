# Quantum Leader Election (QLE)

Implementation of the exact quantum leader election algorithm proposed by [Tani et al](https://arxiv.org/abs/0712.4213).

## Prerequisites

* [SimulaQron](http://www.simulaqron.org/)

  Please refer to the [Getting started](https://softwarequtech.github.io/SimulaQron/html/GettingStarted.html) page for installation instructions. Tested with version 3.0.10

* [ProjectQ](https://projectq.ch/)

  Please refer to the [Getting started](https://projectq.readthedocs.io/en/latest/tutorials.html#getting-started) page for installation instructions.

* [Qiskit](https://qiskit.org/)

  Please refer to the [Qiskit Tutorials](https://github.com/Qiskit/qiskit-tutorials/blob/master/INSTALL.md) page for installation instructions.

### Setup

1. To change the setup of the network, edit the .simulaqron.json file in the exact-qle/ folder.
    See: https://softwarequtech.github.io/SimulaQron/html/ConfNodes.html
    The default configuration is:
```
{
    "backend": "projectq",
    "log-level": 10
    "max-qubits": 40
    "max-registers":100
    "recv-timeout":2.0
}
```

## Execution

1. Open a first shell and execute:
   ```
   simulaqron start --nodes node0,node1,node2
   ```

2. Open a second shell, enter the exact-qle/ folder and execute:
   ```
   ./run.sh
   ```
