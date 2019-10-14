import re

def StringToList(Data):
	MyList=list(Data.split(' '))
	data=re.sub('[^A-Za-z0-9]+', '', MyList[-1]) #for removing /n from operand 

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
		OpCodeInFile=re.sub('[^A-Za-z0-9]+', '', oplist[-1]) #for removing /n from operand 

		if(OpCodeInFile==Opcode):
			OptableFile.close()
			return(int(oplist[0]))
	OptableFile.close()
	return(-1)

InputFile=open("input.txt","r")
SymboltableFile=open("symboltable.txt","w")
IntermediateFile=open("Intermediate.txt","w")
StartAddress=0
LocationCounter=0

data=InputFile.readline()
MyList=StringToList(data)

# Error handle if no memeory address with start

if MyList[1]=="START":
	StartAddress=int(MyList[2])
	LocationCounter=StartAddress
	LineToWrite=""
	
	for element in MyList[:-1]:
		LineToWrite+=str(element)+" "
	
	LineToWrite+=MyList[-1]+'\n'
	IntermediateFile.write(str(LineToWrite)+'\n')
else:
	LocationCounter=0

for data in InputFile:
	MyList=StringToList(data)

	LineToWrite=str(LocationCounter)+" "	
	
	for element in MyList[:-1]:
		LineToWrite+=str(element)+" "
	LineToWrite+=MyList[-1]+'\n'
	IntermediateFile.write(str(LineToWrite)+'\n')

	if(MyList[1]=="END"): # Handle if no end provided
		print("Program length : "+ str(LocationCounter-StartAddress))
		break

	if(MyList[0]!=' '):
		SymboltableFile.write(str(LocationCounter)+" "+str(MyList[0])+'\n')


	if(CheckForOptable(MyList[1])!=-1):
		LocationCounter+=3 # check value of add
	elif(MyList[1]=="Word"):

		LocationCounter+=4
	elif(MyList[1]=="RESW"): # handling variable

		LocationCounter+=2
	elif(MyList[1]=="BYTES"): # handling literal
		LocationCounter+=2
	print(MyList)
	print(LineToWrite)
print(LocationCounter)
