#Contributors:
#Navneet Agarwal 
#2018348
#Sarthak Arora
#2018307

import re

def IntermediateStringToList(Data):
	MyList=list(Data.split(' '))
	data=re.sub('\n', '', MyList[-1]) #for removing /n from operand

	MyList=MyList[0:len(MyList)-1]+[data]
	
	TemporaryList=[]

	for element in MyList:

		if(element!=''):
			TemporaryList=TemporaryList+[element]

	return (TemporaryList)

def GiveOpCode(Opcode):
	OptableFile=open("optable.txt","r")
	for data in OptableFile:
		oplist=list(data.split('\t'))
		OpCodeInFile=re.sub('\n', '', oplist[-1]) #for removing /n from operand 
		if(OpCodeInFile==Opcode):
			OptableFile.close()
			return(oplist[0])
	OptableFile.close()
	return("-1")

def GiveAdress(Symbol):
	SymbolFile=open("symboltable.txt","r")
	for data in SymbolFile:
		symbollist=list(data.split(' '))
		symbollist[-1]=re.sub('\n', '', symbollist[-1]) #for removing /n from operand 
		if(symbollist[0]==Symbol):
			SymbolFile.close()
			return(int(symbollist[-1]))
	SymbolFile.close()
	return(-1)

def passtwo():
	InputFile=open("Intermediate.txt","r")
	SymboltableFile=open("symboltable.txt","r")
	data=InputFile.readline()
	MyList=IntermediateStringToList(data)
	OutputFile=""
	if MyList[0]=="START":
		OutputFile=open("ObjectCode.txt","w")
	else:
		print("Error : START Not Found")
		return(-1)
	for data in InputFile:
		MyList=IntermediateStringToList(data)
		# print(MyList)
		if(MyList[0]=="END"):
			break
		opcode=GiveOpCode(MyList[2])
		# print(opcode)
		if (opcode=="-1"):
			print("Error : Not a valid opcode")
			return(-1)
			break
		address='000000000000'
		if(MyList[2]!='CLA' and MyList[2]!='STP'):
			address=GiveAdress(MyList[3])
			if(address==-1):
				address=0
			address=bin(address)	
			length=len(address)
			length-=2
			address=address[2:]
			while length<=11:
				length+=1
				address='0'+address
			address=str(address)
		OutputFile.write(str(opcode)+address+'\n')
		print(str(opcode)+address)
		# print(data)
if __name__ == '__main__':
	passtwo()