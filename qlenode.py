# In this code it is mapped:
#
# |"consistent"> = |1>
# |"inconsistent"> = |0>
#
# "0^" = |00>
# "1^" = |10>
# "*" = |01>
# "x" = |11>

from time import sleep
from threading import Thread
from random import *

#from SimulaQron.general.hostConfig import *
#from SimulaQron.cqc.backend.cqcHeader import *
#from SimulaQron.cqc.pythonLib.cqc import *

from cqc.pythonLib import *

from functions import *


##############################
#
# QLENode class derived from CQCConnection, with reg* attributes
#

class QLENode():

	def __init__(self, myid, n):
		self.myid = myid
		self.myself = 'node'+str(myid)
		self.n = n
		self.status = 'eligible'
		self.counter = 0
		self.counter2 = 0
		self.counter3 = 0
		self.counter4 = 0
		self.zValues = []
		self.z = 0
		self.reg = []
		self.flag = {}
		self.port = {}

		to_print = "n = {}".format(self.n)
		print(to_print)

		# Calculate neighbour nodes id
		self.otherNodes = []
		n = 1
		for i in range(0, self.n):
			if self.myid != i:
				self.otherNodes.append('node'+str(i))
				self.port[i] = n
				n += 1

		self.otherNodesId = []
		for i in range(0, self.n):
			if self.myid != i:
				self.otherNodesId.append(i)

		# Initialize flag dictionary
		for i in range(0, self.n-1):
			self.flag[self.otherNodesId[i]] = 'READY'

		# Initialize the CQC connection
		with CQCConnection(self.myself) as self.node:
			# Start local processing loop
			self.localProcessing()



	###################################
	#
	#  processing loop
	#
	def localProcessing(self):
		# for loop from k=n to 2
		for k in range(self.n, 1, -1):
			#time.sleep(self.myid)
			# prepare the state |0> in X1
			regX1 = qubit(self.node)
			# prepare the state |"consistent"> in Y
			regY = qubit(self.node)
			regY.X()
			# prepare the state |0> in X0
			regX0 = qubit(self.node)
			if self.status == 'eligible':
				# prepare the state (|0>+|1>)/sqrt(2) in X0
				regX0.H()
			# perform CONSISTENCY with X0, Y, status and n
			regX0, regY = self.consistency(regX0, regY)
			#time.sleep(10) # wait for all nodes to complete consistency
			# measure the qubit in Y in the {|"consistent">,|"inconsistent">} basis to get an outcome y
			y = regY.measure()
			if (y == 1 and self.status == 'eligible'):
				# perform BREAK_SIMMETRY with X0, X1 and k
				regX0, regX1 = self.break_simmetry(regX0, regX1, k)
			if self.status == 'eligible':
				# measure the qubit in Xi in the {|0>,|1>} basis to get an outcome xi for each i in {0,1}
				x0 = regX0.measure()
				x1 = regX1.measure()
				# let z be the non-negative integer expressed by x1x0 (i.e., z=2*x1+x0)
				self.z = (2*x1)+x0
			else:
				# let z=-1
				self.z = -1
			# perform FIND_MAX with z and n to know the maximum value zmax of z over all parties
			# send z value to all the parties
			zmax = self.find_max()
			if self.z != zmax:
				self.status = 'ineligible'
			# output status
			to_print = "Output status of {} is {}".format(self.node.name, self.status)
			print(to_print)

	####################################
	#
	#  CONSISTENCY
	#  Input: single-qubit registers X0 and Y
	#  Output: single-qubit registers X0 and Y
	#
	def consistency(self, regX0, regY):
		print("Executing CONSISTENCY")
		# prepare two-qubit quantum registers R0(1),...,Rn-1(1),...,R0(n-1),...,Rn-1(n-1),R0(n)
		self.reg.clear()
		# Ri(t) is reg[t][i]
		# reg[t][i][0] is the first qubit
		# reg[t][i][1] is the second qubit
		for t in range(0, self.n):
			self.reg.append([])
			if not t == self.n:
				for i in range(0, self.n): # MA: n posti per i, solo se t < n-1
					self.reg[t].append([])
		# initialize R1(t),...,Rn-1(t) with |00>, for all t < n-1
		for t in range(0, self.n):  # qui t va da 0 a n-1 (nel paper da 1 a n)
			for i in range(0, self.n):
				self.reg[t][i].append(qubit(self.node))
				self.reg[t][i].append(qubit(self.node))
		# MA: missing the initialization of reg[n-1][0] (R0(n) in the paper)
		# self.reg[n-1][0].append(qubit(self.node))
		# self.reg[n-1][0].append(qubit(self.node))

		# local initialization (init)
		# N.B. R0(1) of the paper here is reg[0][0]
		if self.status == 'ineligible':
			self.reg[0][0][0] = qubit(self.node)
			self.reg[0][0][1] = qubit(self.node).X()
		else:
			# entangle X0 and R0(1)
			self.reg[0][0][0] = qubit(self.node) # set R0(1)[0] to |0>
			self.reg[0][0][1] = qubit(self.node) # set R0(1)[1] to |0>
			regX0.cnot(self.reg[0][0][0])

		# computing fo (comp)
		for t in range(0, self.n-1):
			# copy the content of R0(t) to the content of each of R1(t),...,Rn-1(t)
			for i in range(1, self.n):
				self.reg[t][0][0].cnot(self.reg[t][i][0])
				self.reg[t][0][1].cnot(self.reg[t][i][1])
			self.counter2 = 0
			tComm = Thread(target=self.listenReg, args=(self.node, self.reg, t, self.n, self.otherNodes, self.otherNodesId, self.flag, self.port))
			tComm.start()
			wt = randint(1, 10)
			time.sleep(wt)
			# exchange the qubits in Ri(t)
			for i in range(1, self.n):
				if (self.flag[self.otherNodesId[i-1]] == 'DONE'):
					continue
				loop = True
				while loop:
					wt = randint(2, 8)
					time.sleep(wt)
					if (self.flag[self.otherNodesId[i-1]] == 'READY'):
						print("--------------------------------------")
						to_print = "{} sending start to {}".format(self.myself, self.otherNodes[i-1])
						print(to_print)
						self.node.sendClassical(self.otherNodes[i-1], str.encode(str(self.myid)+":start"))
						# wait to finish
						wait = True
						while wait:
							time.sleep(2)
							if (self.counter2):
								wait = False
						self.counter2 = 0
					elif (self.flag[self.otherNodesId[i-1]] == 'BUSY'):
						wt = randint(5, 10)
						time.sleep(wt)
					elif (self.flag[self.otherNodesId[i-1]] == 'DONE'):
						loop = False

			for i in range(0, self.n-1):
				self.node.sendClassical(self.otherNodes[i], str.encode(str(self.myid)+":finish"))

			# wait all to finish
			wait = True
			while wait:
				time.sleep(2)
				if (self.counter3 == self.n-1):
					wait = False
			self.counter3 = 0

			to_print = "{} starting 'o' function".format(self.myself)
			print(to_print)

			# set the content of R0(t+1) to r0(t) o r1(t) o ... o rn-1(t)
			# where ri(t) is the content of Ri(t) for 0 <= i <= n-1

			# In the classical case, f_o is represented by a logic circuit with 4-bit inputs and 2-bit output,
			# if we encode {0^, 1^, *, x} by the computational basis {00,01,10,11}
			# (Inputs x and y are each represented two bits).
			# From Table 1 (p.13 in Tani's TOCT paper), it is easy to represent each of the output bits
			# as a logic formula over 4 input variables by using, say, Karnaugh map,
			# which consists of AND and NOT (and thus OR).
			# Then just replace ANDs with Toffoli gates and and NOTs with X gates.

			q0 = self.reg[t][0][0]
			q1 = self.reg[t][0][1]
			for i in range(1, self.n):
				aq0 = qubit(self.node)
				apply1_o(q0, q1, self.reg[t][i][0], self.reg[t][i][1], aq0)
				to_print = "{} apply1_o() done".format(self.myself)
				print(to_print)
				q0 = aq0
				aq1 = qubit(self.node)
				apply2_o(q0, q1, self.reg[t][i][0], self.reg[t][i][1], qubit(self.node), qubit(self.node), aq1)
				to_print = "{} apply2_o() done".format(self.myself)
				print(to_print)
				q1 = aq1
			#if (t < self.n-2):
			#to_print = "t = {}".format(t)
			#print(to_print)
			self.reg[t+1][0][0] = q0
			self.reg[t+1][0][1] = q1
			#elif (t == self.n-2):
				#self.reg[t+1][0].append(q0)
				#self.reg[t+1][0].append(q1)

		# judge
		# flip the content of Y if R0(n) is "x"
		toffoli(self.reg[self.n-1][0][0], self.reg[self.n-1][0][1], regY)
		to_print = "{} Toffoli done".format(self.myself)
		print(to_print)

		for i in range(0, self.n-1):
			self.node.sendClassical(self.otherNodes[i], str.encode(str(self.myid)+":end_consistency"))

		# wait all to complete consistency
		wait = True
		while wait:
			time.sleep(4)
			if (self.counter4 == self.n-1):
				wait = False
		self.counter4 = 0

		return regX0, regY

	####################################
	#
	#  BREAK_SIMMETRY
	#  Input: single-qubit registers X0 and X1, and positive integer k
	#  Output: single-qubit registers X0 and X1
	#
	def break_simmetry(self, regX0, regX1, k):
		to_print = "{} executes BREAK_SIMMETRY".format(self.myself)
		print(to_print)
		if k%2 == 0:
			# apply the tensor products between Uk and I to the qubits in X0 and X1
			Uk(k, regX0)
		else:
			# copy the content of X0 to that of X1
			# i.e., apply CNOT to the qubit in X1 with the control qubit in X0
			regX0.cnot(regX1)
			# apply Vk to the qubits in X0 and X1
			Vk(k, regX0, regX1)
		return regX0, regX1

	####################################
	#
	#  FIND_MAX
	#  Output: max z over all parties
	def find_max(self):
		to_print = "{} executes FIND_MAX".format(self.myself)
		print(to_print)
		self.zValues.clear()
		self.counter = 0
		tComm = Thread(target=self.listen, args=(self.node, self.zValues, self.n))
		tComm.start()
		for i in range(len(self.otherNodes)):
			self.node.sendClassical(self.otherNodes[i], str.encode(self.myself+":z:"+str(self.z)))
			time.sleep(0.2)
		# wait z value from all the parties
		wait = True
		while wait:
			time.sleep(0.2)
			if (self.counter == self.n-1):
				wait = False
		self.zValues.append(self.z)
		#to_print = "Node {} = {}".format(self.myid, self.zValues)
		#print(to_print)
		# get the maximum value zmax of z over all parties
		zmax = max(self.zValues)
		return zmax

	####################################
	#
	#  listening loop (starting message handling in a separate thread)
	#
	def listenReg(self, node, reg, t, n, otherNodes, otherNodesId, flag, port):
		while True:
			data = self.node.recvClassical()
			content = data.decode().split(":")
			sender = content[0]
			msg = content[1]

			#to_print = "{} received {} from node{}".format(self.myself, msg, sender)
			#print(to_print)

			if (msg == "start"):
				to_print = "{}, received start msg".format(self.myself)
				print(to_print)
				tComm = Thread(target=self.startCommHandler, args=(node, reg, t, n, otherNodes, otherNodesId, flag, port, sender))
				tComm.start()
			elif (msg == "busy"):
				to_print = "{}, received busy msg".format(self.myself)
				print(to_print)
				flag[int(sender)] = 'BUSY'
			elif (msg == "end_busy"):
				to_print = "{}, received end busy msg".format(self.myself)
				print(to_print)
				flag[int(sender)] = 'READY'
			elif (msg == "ack"):
				to_print = "{}, received ack msg".format(self.myself)
				print(to_print)
				tComm = Thread(target=self.ackCommHandler, args=(node, reg, t, n, otherNodes, otherNodesId, flag, port, sender))
				tComm.start()
			elif (msg == "finish"):
				to_print = "{}, received finish msg".format(self.myself)
				print(to_print)
				self.counter3 += 1
			elif (msg == "end_consistency"):
				to_print = "{}, received end consistency msg".format(self.myself)
				print(to_print)
				self.counter4 += 1
				if (self.counter4 == self.n-1):
					break


	####################################
	#
	#  thread to manage 'start' message
	#
	def startCommHandler(self, node, reg, t, n, otherNodes, otherNodesId, flag, port, sender):
		to_print = "{}, startCommHandler".format(self.myself)
		print(to_print)
		regSup = []
		flag[int(sender)] = 'DONE'
		for i in range(0, self.n-1):
			if (flag[int(otherNodesId[i])] == 'READY' and int(otherNodesId[i]) != int(sender)):
				to_print = "{} sending busy to {}".format(self.myself, otherNodes[i])
				print(to_print)
				node.sendClassical(otherNodes[i], str.encode(str(self.myid)+":busy"))
		node.sendClassical('node'+sender, str.encode(str(self.myid)+":ack"))
		j = 0
		while j < 2:
			try:
				time.sleep(0.2)
				regSup.append(node.recvQubit())
				print("{} received the qubit {} from node{}".format(node.name, j, sender))
			except CQCTimeoutError:
				print("{} did not receive the qubit {} from node{}".format(node.name, j, sender))
			j += 1
		time.sleep(0.2)
		node.sendQubit(reg[t][port[int(sender)]][0], 'node'+sender)
		time.sleep(0.2)
		node.sendQubit(reg[t][port[int(sender)]][1], 'node'+sender)
		to_print = "{}, sent qubits at startCommHandler".format(self.myself)
		print(to_print)
		reg[t][port[int(sender)]][0] = regSup[0]
		reg[t][port[int(sender)]][1] = regSup[1]
		for i in range(0, self.n-1):
			if (flag[int(otherNodesId[i])] == 'READY' and int(otherNodesId[i]) != int(sender)):
				to_print = "{} sending end_busy to {}".format(self.myself, otherNodes[i])
				print(to_print)
				node.sendClassical(otherNodes[i], str.encode(str(self.myid)+":end_busy"))


	####################################
	#
	#  thread to manage 'ack' message
	#
	def ackCommHandler(self, node, reg, t, n, otherNodes, otherNodesId, flag, port, sender):
		for i in range(0, self.n-1):
			if (flag[int(otherNodesId[i])] == 'READY' and int(otherNodesId[i]) != int(sender)):
				to_print = "{} sending busy to {}".format(self.myself, otherNodes[i])
				print(to_print)
				node.sendClassical(otherNodes[i], str.encode(str(self.myid)+":busy"))
		time.sleep(0.2)
		node.sendQubit(reg[t][port[int(sender)]][0], 'node'+sender)
		time.sleep(0.2)
		node.sendQubit(reg[t][port[int(sender)]][1], 'node'+sender)
		time.sleep(0.2)
		j = 0
		while j < 2:
			try:
				time.sleep(0.2)
				reg[t][port[int(sender)]][j] = node.recvQubit()
				print("{} received the qubit {} from node{}".format(node.name, j, sender))
			except CQCTimeoutError:
				print("{} did not receive the qubit {} from node{}".format(node.name, j, sender))
			j += 1
		flag[int(sender)] = 'DONE'
		for i in range(0, self.n-1):
			if (flag[int(otherNodesId[i])] == 'READY' and int(otherNodesId[i]) != int(sender)):
				to_print = "{} sending end_busy to {}".format(self.myself, otherNodes[i])
				print(to_print)
				node.sendClassical(otherNodes[i], str.encode(str(self.myid)+":end_busy"))
		self.counter2 = 1


	####################################
	#
	#  listening loop (starting message handling in a separate thread)
	#
	def listen(self, node, zVal, n):
		while True:
			data = node.recvClassical()
			content = data.decode().split(":")
			sender = content[0]
			msg = content[1]
			to_print = "App {}: received message '{}' from: {}".format(node.name, msg, sender)
			print(to_print)

			if (msg == 'z'):
				z = int(content[2])
				zVal.append(z)
				to_print = "z = {} arrived from {} has been appended.".format(z, sender)
				print(to_print)
				self.counter += 1

			if self.counter == n-1:
				break



##############################
#
# main
#
def main():

	print('Number of arguments:', len(sys.argv), 'arguments.')
	print('Argument List:', str(sys.argv))

	# Node id
	myid = int(sys.argv[1])
	# Number of nodes
	n = int(sys.argv[2])
	qlenode = QLENode(myid, n)


##############################
main()
