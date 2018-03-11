# -*- coding: utf-8 -*-

""" 
Evaluates 
* settings_cp_forPython.m
* rollout.m
* trainDynModel;")#   % train (GP) dynamics model
* learnPolicy;")#     % learn policy
* applyController;")# % apply controller to system

displays the cart pole

""" 

from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals

import matlab_wrapper
import gym

def visualize_traj(matlab):
	if matlab.workspace.plotting.verbosity>0 : 
			if ~matlab.workspace.ishandle(1):
				matlab.eval('figure(1)')
			else:
				matlab.eval("set(0,'CurrentFigure',1)")
			matlab.eval('clf(1)')
			matlab.eval('draw_rollout_cp')	

def main():
	# initialization of cartpole in gym env
	env = gym.make('CartPole-v0')
	ob = env.reset()
	for _ in range(10):
	    env.render()
	    # x, reward, done, info = env.step(action) 
	    ob, reward, done, _ = env.step(env.action_space.sample()) #random action
	print("cartpole-v0 is on!")

	N = 1.0   					#number controller optimizations

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
	# matlab.workspace.x[0,:]  # PYTHON HIERARCHY! row nr 0,  40 x 7 [H x nX+nU]

	# % 3. Controlled learning (N iterations)
	for j in range(1,matlab.workspace.N.astype(int)+1): # for j = 1:N
		matlab.workspace.j=j
		matlab.eval("trainDynModel;")#   % train (GP) dynamics model
		matlab.eval("learnPolicy;")#     % learn policy
		matlab.eval("applyController;")# % apply controller to system
		print("controlled trial # %d" % j)
		visualize_traj(matlab)

	# % Saving controller outputs per timestep to a file
	f1=open('u.txt', 'w+')
	for u_item in matlab.workspace.x[:,6]:  #all rows, column 7 in MAtlab, 6 in python
		f1.write("%s\n" % u_item)
	f1.close()







	matN = matlab.workspace.N 
	print("we verify N here:", matN)


    # matlab.eval('cartPole_learn') 
	# s = matlab.workspace.sin([0.1, 0.2, 0.3])
	# sorted,idx = matlab.workspace.sort([3,1,2], nout=2)

	print("Done!")
	# when Matlab finishes the code or executions, 
	# closes all windows, clears all and closes all
	# but saves the data in cartPole_X_H40.mat

if __name__ == "__main__":
    main()