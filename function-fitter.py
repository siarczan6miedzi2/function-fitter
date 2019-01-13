import math
import time as tm

def maxVal(lst): # position of max value in the input list
	val = lst[0][1]
	arg = lst[0][0]
	
	pos = 0
	
	for i in range(1, len(lst)):
		if (lst[i][1] > val): # in case of multiple maximum values returns the first one
			val = lst[i][1]
			pos = i
	
	return pos
	
def minVal(lst): # position of max value in the input list
	val = lst[0][1]
	arg = lst[0][0]
	
	pos = 0
	
	for i in range(1, len(lst)):
		if (lst[i][1] < val): # in case of multiple minimum values returns the first one
			val = lst[i][1]
			pos = i
	
	return pos

def create():
	file = open("input", 'r')
	temp = file.readlines()
	s = []
	for item in temp:
		if (item[0] == '#'): pass
		elif (item == '\n'): pass
		else:
			s.append(item[:-1]) if item[-1] == '\n' else s.append(item)
	#for i in range(len(s)):
	#	s[i] = s[i].split()
	#	for j in range(len(s[i])):
	#		s[i][j] = float(s[i][j])
	#for i in s:
	#	print(i, end = "")
	return s
	
def substitute(expr, x, vars):
	s = expr
	s = s.replace("[x]", '(' + str(x) + ')')
	for item in vars:
		name = item[0]
		exp = item[1]
		val = item[2]
#		dst = item[3]
		oldstr = "<"
		oldstr += name
		if exp: oldstr += '*'
		oldstr += '>'
		newstr = '(' + str(val) + ')'
		s = s.replace(oldstr, newstr)
	
	return s
	
def substitutelow(expr, x, vars, i):
	s = expr
	s = s.replace("[x]", '(' + str(x) + ')')
	for item in range(len(vars)):
		name = vars[item][0]
		exp = vars[item][1]
		val = vars[item][2]
		dst = vars[item][3]
		oldstr = "<"
		oldstr += name
		if exp: oldstr += '*'
		oldstr += '>'
		newstr = ""
		if (item == i):
			if (exp): # exponential difference
				newstr += '(' + str(val/(1+dst)) + ')'
			else: # linear difference
				newstr += '(' + str(val-dst) + ')'
		else: newstr += '(' + str(val) + ')'
		s = s.replace(oldstr, newstr)
	
	return s
	
def substitutehigh(expr, x, vars, i):
	s = expr
	s = s.replace("[x]", '(' + str(x) + ')')
	for item in range(len(vars)):
		name = vars[item][0]
		exp = vars[item][1]
		val = vars[item][2]
		dst = vars[item][3]
		oldstr = "<"
		oldstr += name
		if exp: oldstr += '*'
		oldstr += '>'
		newstr = ""
		if (item == i):
			if (exp): # exponential difference
				newstr += '(' + str(val*(1+dst)) + ')'
			else: # linear difference
				newstr += '(' + str(val+dst) + ')'
		else: newstr += '(' + str(val) + ')'
		s = s.replace(oldstr, newstr)
	
	return s

def main():

#	print("\n\n-----FUNCTION FITTER-----\n")
	
	lines = create()
	
#	for i in lines:
#		print(i)
	
	
	#expression, exps, inp = create()
	#inp.sort()

	expression = lines.pop(0) # transfer first line into <expression>

	# find variables in the expression	
	temp = expression.split('<')	
	vars = set()
	
	for item in temp:
		temppos = item.find('>')
		if not temppos == -1: # found
			vars.add(item[:temppos])

	vars = list(vars)
	vars.sort()

	for i in range(len(vars)):
		if (vars[i][-1] == '*'): vars[i] = [vars[i][:-1], True] # treat exponentially and trim name
		else: vars[i] = [vars[i], False] # treat linearly
		
	# prepare  initial value expressions
	
	tempval = []
	tempvald = []
	
	for i in range(len(vars)):
		tempval.append(lines.pop(0)) # transfer conputed initial value expression to <tempval>
		tempvald.append(lines.pop(0)) # transfer conputed initial distance expression to <tempval>
		
	# find maximum, minimum and their difference from neighbors
	
	inp = lines
	for i in range(len(inp)):
		inp[i] = inp[i].split()
		for j in range(len(inp[i])):
			inp[i][j] = float(inp[i][j])
	inp.sort() # <lines> list is (should be) now identical with <inp> list like in gauss-fitter.py
	
	maxpos = maxVal(inp)
	maxarg = inp[maxpos][0]
	maxval = inp[maxpos][1]
	maxvald = None
	maxargd = None
	if (maxpos == 0): # maximum value at the beginning
		maxargd = inp[1][0] - inp[0][0]
		maxvald = inp[1][1]
	elif (maxpos == len(inp)-1): # maximum value at the end
		maxargd = inp[-1][0] - inp[-2][0]
		maxvald = inp[-2][1]
	elif ((inp[maxpos+1][0] - inp[maxpos][0] > inp[maxpos][0] - inp[maxpos-1][0]) and not (inp[maxpos+1][1] == inp[maxpos][1])): # right-hand argument is more distant and does not have another maximum value
		maxargd = inp[maxpos+1][0] - inp[maxpos][0]
		maxvald = inp[maxpos+1][1]
	else: # left-hand argument is more (or equally) distant or the right-hand argument's value is another maximum
		maxargd = inp[maxpos][0] - inp[maxpos-1][0]
		maxvald = inp[maxpos-1][1]
	
	if (maxvald == 0): maxvald = maxval/1000 # a small non-zero value, to possibly enable further computetions
	
	minpos = maxVal(inp)
	minarg = inp[minpos][0]
	minval = inp[minpos][1]
	minvald = None
	minargd = None
	if (minpos == 0): # maximum value at the beginning
		minargd = inp[1][0] - inp[0][0]
		minvald = inp[1][1]
	elif (minpos == len(inp)-1): # maximum value at the end
		minargd = inp[-1][0] - inp[-2][0]
		minvald = inp[-2][1]
	elif ((inp[minpos+1][0] - inp[minpos][0] > inp[minpos][0] - inp[minpos-1][0]) and not (inp[minpos+1][1] == inp[minpos][1])): # right-hand argument is more distant and does not have another maximum value
		minargd = inp[minpos+1][0] - inp[minpos][0]
		minvald = inp[minpos+1][1]
	else: # left-hand argument is more (or equally) distant or the right-hand argument's value is another maximum
		minargd = inp[minpos][0] - inp[maxpos-1][0]
		minvald = inp[minpos-1][1]
		
	if (maxvald == 0): maxvald = maxval/1000 # a small non-zero value, to possibly enable further computetions
	
	# compute initial values
	# computations are not right after extractions, because they need maxval, maxarg, etc.

	for i in range(len(vars)):
		tempval[i] = float(eval(tempval[i])) # transfer conputed initial value expression to <tempval>
		tempvald[i] = float(eval(tempvald[i])) # transfer conputed initial distance expression to <tempval>
		vars[i].extend([tempval[i], tempvald[i]])
	
	
	# now each element of <vars> list is a list of (name, exponentiality, value, distance)
	# TODO (maybe): create a class for it
	

	step = 0
	
	endFLAG = False
	
	while (True):
		
		step += 1
		if (step > 1000): break

		msg = "Optimization step " + str(step) + ":\n"
		for item in vars:
			msg += "{0:3} = {1:8.5f} ± {2:.2e}\n".format(item[0], item[2], item[3])
			
		print(msg)
	
		mainerrorvalue = 0
		errorvalues = []
		for i in range(len(vars)):
			errorvalues.append([0, 0])
		
		for item in inp: # for every input pair
			# compute current error value
			s = substitute(expression, item[0], vars)
			mainerrorvalue += (item[1] - eval(s))**2
		#	print(item[1], '\t', s, eval(s), '\t', mainerrorvalue)
			
			for i in range(len(errorvalues)): # for every variable
				# compute value for lowered valiable
				s = substitutelow(expression, item[0], vars, i)
				errorvalues[i][0] += (item[1] - eval(s))**2
				# compute value for increased valiable
				s = substitutehigh(expression, item[0], vars, i)
				errorvalues[i][1] += (item[1] - eval(s))**2
		
	#	print(mainerrorvalue)
	#	print(errorvalues)
			
		slideFLAG = False	
		
		# slide if needed
		for i in range(len(errorvalues)):
			if (errorvalues[i][0] < mainerrorvalue): # less is better
				if (vars[i][1]): # exponential
					vars[i][2] /= (1+vars[i][3])
				else: # linear
					vars[i][2] -= vars[i][3]
				slideFLAG = True
				break # slide only one value at a time
			if (errorvalues[i][1] < mainerrorvalue): # more is better
				if (vars[i][1]): # exponential
					vars[i][2] *= (1+vars[i][3])
				else: # linear
					vars[i][2] += vars[i][3]
				slideFLAG = True
				break # slide only one value at a time
		
	#	print(slideFLAG)
		if (slideFLAG): continue # slided - end of step
		
		# tighten values
		errorsums = [item[0] + item[1] for item in errorvalues]
	
		for i in range(len(errorsums)):
			if (errorsums[i] == max(errorsums)): vars[i][3] /= 1.5
			else: vars[i][3] /= 1.2
		
		# finish if converged
		
		if (sum(errorsums) < 10**(-30)): # very small difference - converged
			break
		if all(item[3] < 10**(-30) for item in vars): # extremely small uncertainties - converged
			break
	
	print("OPTIMIZATION COMPLETED:")
	for item in vars:
		print("{0:3} = {1:8.5f} ± {2:.2e}".format(item[0], item[2], item[3]))	
	

	
	
if __name__ == "__main__": main()
