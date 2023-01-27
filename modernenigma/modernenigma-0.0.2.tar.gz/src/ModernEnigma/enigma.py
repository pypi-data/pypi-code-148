#Enigma Machine Emulator - enigma.py
import string

# PLUGBOARD #
class Plugboard:
	def __init__(self,size):
		self.size = size
		i = 0
		while i < self.size:
			plugArray.append(i)
			i+=1
	
	# RESET #
	def reset(self):
		i = 0
		while i < self.size:
			plugArray[i] = i
			i+=1
	
	# ADD PLUG #
	def addPlug(self, s1, s2):
		temp = plugArray[s1]
		plugArray[s1] = plugArray[s2]
		plugArray[s2] = temp
	
	# ENCRYPT #
	def traceIn(self, value):
		value = plugArray[value]
		return value
	
	# DECRYPT #
	def traceOut(self, value):
		value = plugArray.index(value)
		return value
	
# ROTOR #
class Rotor:
	def __init__(self, net, att):
		self.net = net
		self.att = att
		self.rotation = 0
		
	# ROTATE #
	def rotate(self, turnDir):
		if turnDir==True:
			self.rotation+=1
		elif turnDir==False:
			self.rotation-=1	
		self.rotation = normalize(self.rotation)
	
	# STEP #
	def step(self, stepDir, attitude):
		self.rotate(stepDir)
		if stepDir:
			attitude+=1
		elif not stepDir:
			attitude-=1
		if self.rotation == normalize(attitude):
			return True
		else:
			return False
		
# CRADLE #
class Cradle:
	def __init__(self,slot, plug):
		self.slot = slot
		self.plug = plug

	# TICK #
	def tick(self, tickDir):
		flag = True #Step flag	
		
		i=0 #Slot index start val
		while i < len(self.slot)-1:
			if flag:
				flag = self.slot[i].step(tickDir, self.slot[i].att)
			i+=1
	
	# SET ROTOR #
	def setRotor(self, r, tickDir):
		self.slot[r].step(tickDir, self.slot[r].att)
	

	# READ ROTORS #
	def readRotors(self):
		i= len(self.slot)-1
		temp=[]
		while i > 0:
			i-=1
			temp.append(self.slot[i].rotation)
		return temp
		
	# RESET ROTORS #
	def resetRotors(self):
		for r in self.slot:
			r.rotation=0
			
	# ENCODE KEY #
	def encodeKey(self, key):
			self.tick(True)
			path = self.plug.traceIn(key)
			
			#Encode In
			i=0
			while i < len(self.slot):
				path += self.slot[i].rotation
				path = normalize(path)
				path = self.slot[i].net[path]
				i+=1
			
			#Encode Out
			i = len(self.slot)-1
			while i > 0:
				i-=1
				path = normalize(path)
				path = self.slot[i].net.index(path)
				path -= self.slot[i].rotation
				path = normalize(path)
			
			path = self.plug.traceOut(path)
			print(path)
			return path
			
	# ENCODE STRING #
	def encode(self, msg):
		newMsg = list(msg.replace(' ','').lower())
		i=0
		while  i < len(newMsg):
			newMsg[i] = self.encodeKey(letters.index(newMsg[i]))
			newMsg[i]=letters[newMsg[i]]
			i+=1
		return listToString(newMsg)


#Alphabet enumerated
letters = list(string.ascii_lowercase)

# ROTOR WIRING #
wP = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] #Passive Array
w0 = [4,10,12,5,11,6,3,16,21,25,13,19,14,22,24,7,23,20,18,15,0,8,1,17,2,9] #Rotor Arrays
w1 = [0,9,3,10,18,8,17,20,23,1,11,7,22,19,12,2,16,6,25,13,15,24,5,21,14,4] #...
w2 = [1,3,5,7,9,11,2,15,17,19,23,21,25,13,24,4,8,22,6,0,10,12,20,18,16,14] #...
wR = [24,17,20,7,16,18,11,3,15,23,13,6,14,10,12,8,4,1,5,25,2,22,21,9,0,19] #Reflector Array

#Rotors Size
rotorSize = len(wR)-1

# ROTOR OBJS #
r0 = Rotor(w0, 17)#Ring Settings
r1 = Rotor(w1, 6.)#...
r2 = Rotor(w2, 22)#...
#
rR = Rotor(wR, rotorSize*2)#Reflector

# NORMALIZE #
def normalize(val, length=rotorSize+1):
	return val % length

# LIST TO STRING #	
def listToString(arr, buff=""):  
    msg = ""  
    for c in arr:  
        msg+=c
        msg+=buff
    return msg

# INT TO LETTER 
def intToLetter(arr):
	newArr = []
	for i in arr:
		newArr.append(letters[i])
	return newArr

# GET PLUGS #
def getPlugs():
		return listToString(intToLetter(plugArray), buff=" ")

#Plugboard Array
plugArray=[]

#Load cradle
cradle = [r0, r1, r2, rR]

#Instantiate a Plugboard
p = Plugboard(rotorSize+1)

#Instantiate a Labyrinth
c = Cradle(cradle, p)


