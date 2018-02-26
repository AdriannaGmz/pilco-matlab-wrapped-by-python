# -*- coding: utf-8 -*-

""" 
Evaluates cartPole_learn.m file
Modified 		cartPole_learn 				and settings_cp
to 			cartPole_learn_forPython 	and settings_cp_forPython

for specific N overriding and requirements
""" 

from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals

import matlab_wrapper


def main():
	N = 2.0   					#number controller optimizations 

	matlab = matlab_wrapper.MatlabSession()
	matlab.eval('clear all') 
	matlab.put('N', N) 			# Override Nr controller optimizations
	# matlab.workspace.N = N 	# Same as line above

	matN = matlab.get('N')
	print("Overriding Nr controller optimizations from here:", matN)

	matlab.eval('cartPole_learn_forPython') # here happens the magic

	matN = matlab.get('N')
	# matN = matlab.workspace.N # Same as line above
	print("we verify N here:", matN)


    # matlab.eval('cartPole_learn') 
	# s = matlab.workspace.sin([0.1, 0.2, 0.3])
	# sorted,idx = matlab.workspace.sort([3,1,2], nout=2)
	# matlab.workspace.a = 12.3
	# b = matlab.workspace.b
	# matlab.put('x', 2.)
    # y = matlab.get('y')
    # print("We are executing:", y)

	print("Done!")
	# when Matlab finishes the code or executions, 
	# closes all windows, clears all and closes all
	# but saves the data in cartPole_X_H40.mat

if __name__ == "__main__":
    main()