from cmath import exp
import math

#from qiskit import Aer
from qiskit.quantum_info.synthesis import two_qubit_cnot_decompose
import numpy as np

from projectq.setups.decompositions import arb1qubit2rzandry as arb1q

#from SimulaQron.general.hostConfig import *
#from SimulaQron.cqc.backend.cqcHeader import *
#from SimulaQron.cqc.pythonLib.cqc import *

from cqc.pythonLib import *

from toffoli import *


###################################
#
#  Vk matrix for odd k >= 3
#
def Vk(k, q0, q1):
	print("Executing Vk")
	e = exp(1j*(math.pi/k))
	e2 = exp(1j*(math.pi/(2*k)))
	f = 1/math.sqrt(e.real+1)
	u11 = 1/math.sqrt(2)
	u13 = math.sqrt(e.real)
	u14 = e/math.sqrt(2)
	u21 = 1/math.sqrt(2)
	u23 = -math.sqrt(e.real)*exp(-1j*(math.pi/k))
	u24 = exp(-1j*(math.pi/k))/math.sqrt(2)
	u31 = math.sqrt(e.real)
	u33 = (exp(-1j*(math.pi/(2*k)))*e.imag)/(1j*math.sqrt(2)*e2.real)
	u34 = -math.sqrt(e.real)
	u42 = math.sqrt(e.real+1)
	matrix_to_decompose =  np.array([[u11*f, 0, u13*f, u14*f],
                     		[u21*f, 0, u23*f, u24*f],
                     		[u31*f, 0, u33*f, u34*f],
                     		[0, u42*f, 0, 0]], dtype=complex)
	circuit = two_qubit_cnot_decompose(matrix_to_decompose)
	i = 0
	while i < len(circuit):
		if circuit[i]['name'] == 'u1':
			lambd = float(circuit[i]['params'][2])
			q_num = int(circuit[i]['args'][0])
			step = int(lambd*256/(2*math.pi))
			if step > 255:
				step -= 255
			if q_num == 0:
				q0.rot_Z(step)
			else:
				q1.rot_Z(step)
		elif circuit[i]['name'] == 'u3':
			theta = float(circuit[i]['params'][0])
			phi = float(circuit[i]['params'][1])
			lambd = float(circuit[i]['params'][2])
			q_num = int(circuit[i]['args'][0])
			#to_print = "theta = {}, phi = {}, lambd = {}".format(theta, phi, lambd)
			#print(to_print)
			step1 = int((phi+(3*math.pi))*256/(2*math.pi))
			step2 = int((math.pi/2)*256/(2*math.pi))
			step3 = int((theta+math.pi)*256/(2*math.pi))
			step4 = int((math.pi/2)*256/(2*math.pi))
			step5 = int(lambd*256/(2*math.pi))
			if step1 > 255:
				step1 -= 255
			if step2 > 255:
				step2 -= 255
			if step3 > 255:
				step3 -= 255
			if step4 > 255:
				step4 -= 255
			if step5 > 255:
				step5 -= 255
			if q_num == 0:
				q0.rot_Z(step1)
				q0.rot_X(step2)
				q0.rot_Z(step3)
				q0.rot_X(step4)
				q0.rot_Z(step5)
			else:
				q1.rot_Z(step1)
				q1.rot_X(step2)
				q1.rot_Z(step3)
				q1.rot_X(step4)
				q1.rot_Z(step5)
		elif circuit[i]['name'] == 'cx':
			control_qubit = int(circuit[i]['args'][0])
			target_qubit = int(circuit[i]['args'][1])
			if control_qubit == 0:
				q0.cnot(q1)
			else:
				q1.cnot(q0)
		i += 1
	return


###################################
#
#  Uk matrix for even k >= 2
#
def Uk(k, q):
	print("Executing Uk")
	matrix_to_decompose = [[1/math.sqrt(2), 1/math.sqrt(2) * exp(-1j*(math.pi/k))],
            				[-1/math.sqrt(2) * exp(1j*(math.pi/k)), 1/math.sqrt(2)]]
	a, b_half, c_half, d_half = arb1q._find_parameters(matrix_to_decompose)
	d = float(d_half*2)
	c = float(c_half*2)
	b = float(b_half*2)
	#to_print = "b = {}, c = {}, d = {}".format(b, c, d)
	#print(to_print)
	step_d = int(d*256/(2*math.pi))
	step_c = int(c*256/(2*math.pi))
	step_b = int(b*256/(2*math.pi))
	if step_d > 255:
		step_d -= 255
	if step_c > 255:
		step_c -= 255
	if step_b > 255:
		step_b -= 255
	q.rot_Z(step_d)
	q.rot_Y(step_c)
	q.rot_Z(step_b)
	return


###################################
#
#  'o' operator of the fo function (1)
#
def apply1_o(q1, q2, q3, q4, aq):
	q1.X()
	q3.X()
	toffoli(q1, q3, aq)
	aq.X()
	return


###################################
#
#  'o' operator of the fo function (2)
#
def apply2_o(q1, q2, q3, q4, aq1, aq2, aq3):
	toffoli(q2, q4, aq1)
	toffoli(aq1, q3, aq2)
	toffoli(aq2, q1, aq3)
	aq3.X()
	return
