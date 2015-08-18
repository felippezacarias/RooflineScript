import sys
import re
import shutil
import regexkernel

# Markers that will delimit where the parsing and operation couting will occur.
kernelBeginMarker = "// KERNEL START!!!"
kernelEndMarker = "// KERNEL END!!!"
forChar = "for"
forRegex = "for\s*\([^;]*?;[^;]*?;[^)]*?\)"
forConditionSeparator = ";"
equalChar = "="


# Will get the kernels and put it on a array of strings, to be parsed separatedly.
# Input argument is the whole code.
def extractKernels(code):
	
	openBrackets = 0
	closeBrackets = 0
	
	matchBeginIndex = 0
	matchEndIndex = 0
        nextSearchIndex = 0
	kernelList = []

        while matchBeginIndex != -1:

                # Find the begin of the kernel.
		matchBeginIndex = code.find(kernelBeginMarker, nextSearchIndex)
                
		# Bail out if not found.
		if matchBeginIndex == -1:
			break

		# Increment the next search index on the lenght of the marker to search next occurences.
		nextSearchIndex = matchBeginIndex + len(kernelBeginMarker)

		# Look for the end kernel marker.
		matchEndIndex = code.find(kernelEndMarker, nextSearchIndex)

		# Bail out if not found.
		if matchEndIndex == -1:
			break

		# Increment the next search index on the lenght of the marker to search next occurences.
		nextSearchIndex = matchEndIndex + len(kernelEndMarker)

		# Extract the kernel, and add to the list.
		kernelList.append(code[matchBeginIndex + len(kernelBeginMarker) : matchEndIndex - 1 ])


	return kernelList


# Generic method to get things inside parenteses, or brackets and so on. Counts the opened and closed,
# chars, and extract whats inside.
def getEnclosingContent(code, beginIndex, openChar, closeChar):

	openCharIndex = -1 
	iterIndex = beginIndex
	openCharCount = 0
	closeCharCount = 0
	
	# Get the code content contained in the block.
	while True:
			
		if code[iterIndex] == openChar:
			openCharCount += 1

		# Save the index of the first parenteses open.
		if (openCharCount == 1) and (openCharIndex == -1):
			openCharIndex = iterIndex
					
		if code[iterIndex] == closeChar:
			closeCharCount += 1
								
		
		# If all parenteses were openned and closed, break out of the loop.
		if (openCharCount > 0) and  (openCharCount == closeCharCount):
				break

		iterIndex += 1

	return [openCharIndex, iterIndex]

	
#def parseKernel(code):


#def getInnerLoop(code):

# Gets the "for" declarations.
def extractFor(code):
	
	matchBeginIndex = 0
	matchEndIndex = 0

	openParenteseCount = 0
	closedParenteseCount = 0
	
	parentesesContent = ""
	expressions = []
	enclosingIndexes = []

	bracketContent = ""

	result = {}
	result['code'] = ""
	result['expressions'] = []
	
	# Makes the pattern to search for the fors.
	forPattern = re.compile(forRegex)

	# Gets to the "for" declaration.
	forMatch = forPattern.search(code, 0)
	
	if forMatch == None:
		result['code'] = code
		return result

	# Get the expression contained in the parentesis.
	# for ().
	iterIndex = forMatch.start() + len(forChar)
	openParIndex = 0
	
	enclosingIndexes = getEnclosingContent(code, iterIndex, '(', ')')

	# Take out the initial and the final parenteses.
	if enclosingIndexes != []:
		parentesesContent = code[enclosingIndexes[0] + 1 : enclosingIndexes[1]]

	# Break the expressions inside of the loop.
	expressions = parentesesContent.split(';');

	# Updates the "cursor" position to keep parsing.
	iterIndex = enclosingIndexes[1] + 1

	# Get the code content contained in the block.
	enclosingIndexes = []

	enclosingIndexes = getEnclosingContent(code, iterIndex, '{', '}')

	# Take out the initial and the final brackets.
	if enclosingIndexes != []:
		bracketContent = code[enclosingIndexes[0] + 1 : enclosingIndexes[1] - 1]
	
	if bracketContent != "":
		res = extractFor(bracketContent)
		result['code'] = res['code']
		if res['expressions'] != []:
			for exp in res['expressions']:
				result['expressions'].append(exp)
		
	#print expressions
	result['expressions'].append(expressions)
	
	return result	
	
		

#def printKernelResult():


#def printOverallResult():


#def getLoadStores():


#def getOpCounts():


if sys.argv.count < 2:
	print "Need to provide at least 1 argument. File to be processed."
	sys.exit()

sourceFile = sys.argv[1]
fileContent = ""

try:
	
	f = open(sourceFile, 'r')

	fileContent = f.read()

	f.close()

except ErroExcep:

	print "Error while opening file!!!"
	sys.exit(0)

kernelList = extractKernels(fileContent)

for kernel in kernelList:
	res = extractFor(kernel)
	regexkernel.kernel_count(res['code'])
	#print res['code']
	for expression in res['expressions']:
		print expression

