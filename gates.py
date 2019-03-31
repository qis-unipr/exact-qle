from cmath import exp
import math

#from SimulaQron.general.hostConfig import *
#from SimulaQron.cqc.backend.cqcHeader import *
#from SimulaQron.cqc.pythonLib.cqc import *
from cqc.pythonLib import *

###################################
#
#  T^\dagger Gate
#
def Td(q):
	step = int((math.pi*(3/4))*256/(2*math.pi))
	q.rot_Z(step)
	return


###################################
#
#  S Gate
#
def S(q):
	step = int((math.pi*(3/2))*256/(2*math.pi))
	q.rot_Z(step)
	return
