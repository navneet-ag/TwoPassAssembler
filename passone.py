import re

def StringToList(Data):
	MyList=list(Data.split(' '))
	data=re.sub('\n', '', MyList[-1]) #for removing /n from operand

	MyList=MyList[0:len(MyList)-1]+[data]
	
	TemporaryList=[]

	for element in MyList:

		if(element!=''):
			TemporaryList=TemporaryList+[element]

	if(":" not in TemporaryList[0]):
		TemporaryList=[" "]+TemporaryList

	else:
		data=re.sub('[^A-Za-z0-9]+', '', TemporaryList[0]) #for removing : 
		TemporaryList=[data]+TemporaryList[1:]
	return (TemporaryList)


def CheckForOptable(Opcode):
	OptableFile=open("optable.txt","r")
	for data in OptableFile:
		oplist=list(data.split('\t'))
		OpCodeInFile=re.sub('\n', '', oplist[-1]) #for removing /n from operand 

		if(OpCodeInFile==Opcode):
			OptableFile.close()
			return(int(oplist[0]))
	OptableFile.close()
	return(-1)

def WriteinSymbolTable(value):
	ReadSymboltableFile=open("symboltable.txt","r")
	# print("Start with "+value)

	for data in ReadSymboltableFile:
	
		symbollist=list(data.split(' '))
		symbol=re.sub('\n', '', symbollist[-1]) #for removing /n from operand 
		symbollist=symbollist[:-1]+[symbol]
		# print(symbollist[0])
		if(symbollist[0]==value):
			# print("End")
			return

	ReadSymboltableFile.close()
	SymboltableFile=open("symboltable.txt","a")
	SymboltableFile.write(value+'\n')
	SymboltableFile.close()
	# print("End2")

def WriteLabelInSymbolTab(value,address):
	ReadSymboltableFile=open("symboltable.txt","r")
	LabelFoundFlag=False
	# print("Start with "+value)
	string=""
	for data in ReadSymboltableFile:
		
		symbollist=list(data.split(' '))
		symbol=re.sub('\n', '', symbollist[-1]) #for removing /n from operand 
		symbollist=symbollist[:-1]+[symbol]
		# print(symbollist[0])
		if(symbollist[0]==value and not(LabelFoundFlag)):
			# print(value)
			LabelFoundFlag=True
			string=string+symbollist[0]+" "+str(address)+'\n'
		else:
			string+=data
	ReadSymboltableFile.close()
	if(LabelFoundFlag):
		SymboltableFile=open("symboltable.txt","w")
		SymboltableFile.write(string)
		SymboltableFile.close()
	else:
		SymboltableFile=open("symboltable.txt","a")
		SymboltableFile.write(value+" "+str(address)+'\n')
		SymboltableFile.close()

def AssignMemoryAddressToVariables(LocationCounter):
	ReadSymboltableFile=open("symboltable.txt","r")
	# print("Start with "+value)
	string=""
	string2=""
	for data in ReadSymboltableFile:
		
		symbollist=list(data.split(' '))
		symbol=re.sub('\n', '', symbollist[-1]) #for removing /n from operand 
		symbollist=symbollist[:-1]+[symbol]
		# print(symbollist[0])
		if(len(symbollist)==1):
			# print(value)
			string2=string2+symbollist[0]+" "+str(LocationCounter)+'\n'
			LocationCounter+=12
		else:
			string+=data
	ReadSymboltableFile.close()
	SymboltableFile=open("symboltable.txt","w")
	SymboltableFile.write(string+string2)
	SymboltableFile.close()
	return(LocationCounter-12)


InputFile=open("input.txt","r")
SymboltableFile=open("symboltable.txt","w")
SymboltableFile.close()
IntermediateFile=open("Intermediate.txt","w")
StartAddress=0
LocationCounter=0
LineNumber=0
ExecutionSuccessful=False
StopFoundStatus=False
DivisionUsedFlag=False
data=InputFile.readline()
MyList=StringToList(data)

# Error handle if no memory address with start

if MyList[1]=="START":
	StartAddress=int(MyList[2])
	LocationCounter=StartAddress
	LineToWrite=""
	
	for element in MyList[:-1]:
		LineToWrite+=str(element)+" "
	
	LineToWrite+=MyList[-1]+'\n'
	IntermediateFile.write(str(LineToWrite))
else:
	LocationCounter=0


LineNumber=1
try:
	for data in InputFile:
		MyList=StringToList(data)
		LineToWrite=str(LocationCounter)+" "	
		for element in MyList[:-1]:
			LineToWrite+=str(element)+" "
		LineToWrite+=MyList[-1]+'\n'

		if(MyList[1]=="END"): # Handle if no end provided
			ExecutionSuccessful=True
			print("Program length : "+ str(LocationCounter-StartAddress))
			IntermediateFile.write("  "+"END"+'\n')
			break
		else:
			IntermediateFile.write(str(LineToWrite))

		if(MyList[0]!=' '):
			SymboltableFile=open("symboltable.txt","a")
			WriteLabelInSymbolTab(MyList[0],LocationCounter)
			SymboltableFile.close()

		if(CheckForOptable(MyList[1])!=-1):
			
			if(MyList[1]=="DIV"):
				DivisionUsedFlag=True
				WriteinSymbolTable("R1")
				WriteinSymbolTable("R2")

			if(MyList[1]=="CLA"):
				if (not((len(MyList)==2) or (len(MyList)==4 and MyList[2]==";"))):
					print("Error in line "+str(LineNumber+1) +" : Incorrect number of operands")
					break
			elif(MyList[1]=="STP" ):
		
				if (not((len(MyList)==2) or (len(MyList)==4 and MyList[2]==";"))):
					print("Error in line "+str(LineNumber+1) +" : Incorrect number of operands")
					break
				else:
					StopFoundStatus=True
			else:
				if((len(MyList)==3) or (len(MyList)==5 and MyList[3]==";")):
					WriteinSymbolTable(MyList[2])
					
				else:
					print("Error in line "+str(LineNumber+1) +" : Incorrect number of operands")
					break

			LocationCounter+=12 # check value of add
		else:
			print("Error in line "+str(LineNumber+1) + ":Not a Legal Opcode") #Error 
			break

		LineNumber+=1

		# print(MyList)
		# print(LineToWrite)
	LocationCounter= AssignMemoryAddressToVariables(LocationCounter)

	if(ExecutionSuccessful):
		print(LocationCounter)
except IndexError:
	print("Please remove empty line in between two instructions")