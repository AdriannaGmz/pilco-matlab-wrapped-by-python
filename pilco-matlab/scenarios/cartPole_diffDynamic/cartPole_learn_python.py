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

def visualize_traj(matlab):
	if matlab.workspace.plotting.verbosity>0 : 
			if ~matlab.workspace.ishandle(1):
				matlab.eval('figure(1)')
			else:
				matlab.eval("set(0,'CurrentFigure',1)")
			matlab.eval('clf(1)')
			matlab.eval('draw_rollout_cp')	

def main():

	N = 2.0   					#number controller optimizations 

	matlab = matlab_wrapper.MatlabSession()
	matlab.eval('clear all') 
	matlab.eval('close all') 
	matlab.workspace.N = N 	# Override Nr controller optimizations
	# matlab.put('N', N) 	# Same as line above
	# matN = matlab.get('N') 
	# matlab.put('basename', 'cartPole_py_')

	matN = matlab.workspace.N 
	print("Overriding Nr controller optimizations from here:", matN)

	matlab.eval('settings_cp_forPython') 
	matlab.workspace.basename= 'cartPole_py_'


	# % 2. Initial J random rollouts
	for jj in range(1,matlab.workspace.J.astype(int)+1): # for jj = 1:J
		matlab.workspace.jj=jj
		matlab.eval("[xx, yy, realCost{jj}, latent{jj}] = rollout(gaussian(mu0, S0), struct('maxU',policy.maxU), H, plant, cost)")
		matlab.eval("x = [x; xx]; y = [y; yy];")       # augment training sets for dynamics model
		visualize_traj(matlab)
		# if matlab.workspace.plotting.verbosity>0 : 
		# 	if ~matlab.workspace.ishandle(1):
		# 		matlab.eval('figure(1)')
		# 	else:
		# 		matlab.eval("set(0,'CurrentFigure',1)")
		# 	matlab.eval('clf(1)')
		# 	matlab.eval('draw_rollout_cp')	

	matlab.eval("mu0Sim(odei,:) = mu0; S0Sim(odei,odei) = S0;")
	matlab.eval("mu0Sim = mu0Sim(dyno); S0Sim = S0Sim(dyno,dyno);")

	# matlab.workspace.x.ndim   # gives the nr of dims bc they're numpy arrays
	# matlab.workspace.x.shape   # gives the size bc they're numpy arrays
	# matlab.workspace.x[0,:]  # access row nr 0,  40 x 7 [H x nX+nU]

	# % 3. Controlled learning (N iterations)
	for j in range(1,matlab.workspace.N.astype(int)+1): # for j = 1:N
		matlab.workspace.j=j
		matlab.eval("trainDynModel;")#   % train (GP) dynamics model
		matlab.eval("learnPolicy;")#     % learn policy
		matlab.eval("applyController;")# % apply controller to system
		print("controlled trial # %d" % j)
		visualize_traj(matlab)







	# matlab.eval('cartPole_learn_forPython') # here happens the magic

	matN = matlab.workspace.N 
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