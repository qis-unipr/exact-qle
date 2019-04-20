Install SimulaQron with:

pip3 install SimulaQron

To setup the network, type:

simulaqron set backend projectq
simulaqron set nodes-file /Users/micheleamoretti/Documents/SVILUPPO/exact-qle/config/Nodes.cfg
simulaqron set app-file /Users/micheleamoretti/Documents/SVILUPPO/exact-qle/config/appNodes.cfg
simulaqron set cqc-file /Users/micheleamoretti/Documents/SVILUPPO/exact-qle/config/cqcNodes.cfg
simulaqron set vnode-file /Users/micheleamoretti/Documents/SVILUPPO/exact-qle/config/virtualNodes.cfg
simulaqron set topology-file /Users/micheleamoretti/Documents/SVILUPPO/exact-qle/config/topology.json
simulaqron set max-qubits 40
simulaqron set max-registers 100
simulaqron set recv-timeout 2.0
simulaqron set log-level debug
