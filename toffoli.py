from cmath import exp
import math

#from SimulaQron.general.hostConfig import *
#from SimulaQron.cqc.backend.cqcHeader import *
#from SimulaQron.cqc.pythonLib.cqc import *
from cqc.pythonLib import *

from gates import *


###################################
#
#  Toffoli Gate
#
def toffoli(q1, q2, q3):
	q3.H()
	q2.cnot(q3)
	Td(q3)
	q1.cnot(q3)
	q3.T()
	q2.cnot(q3)
	Td(q3)
	q1.cnot(q3)
	Td(q2)
	q3.T()
	q3.H()
	q1.cnot(q2)
	Td(q2)
	q1.cnot(q2)
	q1.T()
	S(q2)
	return
