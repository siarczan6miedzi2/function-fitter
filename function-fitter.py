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

def createList():
	file = open("gauss-input.txt", 'r')
	s = file.readlines()
	for i in range(len(s)):
		s[i] = s[i].split()
		for j in range(len(s[i])):
			s[i][j] = float(s[i][j])
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

	print("\n\n-----FUNCTION FITTER-----\n")

	inp = createList()
	inp.sort()

	expression = "<k*>*(1/math.sqrt(2*math.pi*<var*>))*math.exp(-(([x]-<med>)**2/(2*<var*>)))"

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
		
		
	# find maximum, minimum and their difference from neighbors (TODO: create for minimum)
	
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
	
	
	# compute initial values
	
	vars[0].extend([float(eval("maxval*math.sqrt(2*math.pi*maxargd**2/(2*(math.log(maxval/maxvald))))")), float(eval("10"))])
	vars[1].extend([float(eval("maxarg")), float(eval("maxargd**2/(2*(math.log(maxval/maxvald)))"))])
	vars[2].extend([float(eval("maxargd**2/(2*(math.log(maxval/maxvald)))")), float(eval("10"))])
	
	# now each element of <vars> list is a list of (name, exponentiality, value, distance)
	# TODO (maybe): create a class for it
	

	step = 0
	
	endFLAG = False
	
	while (True):
		
		step += 1
		if (step > 1000): break
	
		print("Optimization step", step, "\b:")
		for item in vars:
			print("{0:3} = {1:8.5f} ± {2:.2e}".format(item[0], item[2], item[3]))
	
		mainerrorvalue = 0
		errorvalues = []
		for i in range(len(vars)):
			errorvalues.append([0, 0])
		
		for item in inp: # for every input pair
			# compute current error value
			s = substitute(expression, item[0], vars)
			mainerrorvalue += (item[1] - eval(s))**2
		#	print("\t", mainerrorvalue)
			
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
