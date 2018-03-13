# -*- coding: utf-8 -*-

""" 
Evaluates 
* settings_cp_forPython.m
* rollout.m
* trainDynModel;")#   # train (GP) dynamics model
* learnPolicy;")#     # learn policy
* applyController;")# # apply controller to system

displays the cart pole

""" 

from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals
# import os  
# from sett_cp import *
import sett_cp as scp  		#python version of settings_cp.m
import roll_cp as roll 		#python version of rollout.m

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
	# 1. Initialization: cartpole environment in gym
	env = gym.make('CartPole-v0')
	ob = env.reset()
	# print("cartpole-v0 is on!")
	# for _ in range(10):
	#     env.render()
	#     # x, reward, done, info = env.step(action) 
	#     ob, reward, done, _ = env.step(env.action_space.sample()) #random action


	# 1. Initialization: pilco in matlab
	N = 2.0   					#number controller optimizations
	matlab = matlab_wrapper.MatlabSession()
	matlab.eval('clear all') 
	matlab.eval('close all') 
	matlab.workspace.N = N 	# Override Nr controller optimizations
	# matlab.put('N', N) 	# Same as line above
	# matN = matlab.get('N') 
	# matN = matlab.workspace.N 
	# print("Overriding Nr controller optimizations from here:", matN)
	# os.system("settings_cp.py")   	# :( CREATES A SUBSHELL and loses all memory. BETTER WITH FUNCTIONS! 

	# settings_cp   # As follows:
	# ===================================
	scp.init(matlab)
	scp.init(matlab)
	scp.def_state_indices(matlab)
	scp.def_scenario(matlab)
	scp.def_plant_st(matlab)
	scp.def_policy_st(matlab)
	scp.def_cost_st(matlab)
	scp.def_dyn_st(matlab)
	scp.def_param_policy(matlab)
	scp.plot_verb(matlab)
	scp.last_init(matlab)
	# ===================================
	matlab.workspace.basename= 'cartPole_py_'




	# 2. Initial J random rollouts
	for jj in range(1,matlab.workspace.J.astype(int)+1): # for jj = 1:J
		matlab.workspace.jj=jj

		# [xx, yy, realCost{jj}, latent{jj}] = rollout(gaussian(mu0, S0), struct('maxU',policy.maxU), H, plant, cost)
		matlab.eval("start_py 	= gaussian(mu0, S0)") 				#BEGINNING OF WORKAROUND for rollout function
		matlab.eval("policy_py 	= struct('maxU',policy.maxU)")
		matlab.eval("H_py 		= H")
		matlab.eval("plant_py 	= plant")
		matlab.eval("cost_py 	= cost")
		roll.rollout_py(matlab)    									# FUNCTION ====
		matlab.workspace.xx = matlab.workspace.x_py
		matlab.workspace.yy = matlab.workspace.y_py
		matlab.eval("realCost{jj} 	= L_py;")
		matlab.eval("latent{jj}		= latent_py;")
		matlab.eval("clear x_py")     
		matlab.eval("clear y_py")
		matlab.eval("clear L_py")
		matlab.eval("clear latent_py") 								#END OF WORKAROUND 

		matlab.eval("x = [x; xx]; y = [y; yy];")       # augment training sets for dynamics model
		visualize_traj(matlab)




	matlab.eval("mu0Sim(odei,:) = mu0; S0Sim(odei,odei) = S0;")
	matlab.eval("mu0Sim = mu0Sim(dyno); S0Sim = S0Sim(dyno,dyno);")

	# matlab.workspace.x.ndim   # gives the nr of dims bc they're numpy arrays
	# matlab.workspace.x.shape   # gives the size bc they're numpy arrays
	# matlab.workspace.x[0,:]  # PYTHON HIERARCHY! row nr 0,  40 x 7 [H x nX+nU]

	# # 3. Controlled learning (N iterations)
	for j in range(1,matlab.workspace.N.astype(int)+1): # for j = 1:N
		matlab.workspace.j=j
		matlab.eval("trainDynModel;")#   # train (GP) dynamics model
		matlab.eval("learnPolicy;")#     # learn policy
		matlab.eval("applyController;")# # apply controller to system
		print("controlled trial # %d" %j)
		visualize_traj(matlab)

	# # Saving controller outputs per timestep to a file
	f1=open('u.txt', 'w+')
	for u_item in matlab.workspace.x[:,6]:  #all rows, column 7 in MAtlab, 6 in python
		f1.write("%s\n" %u_item)
	f1.close()







	matN = matlab.workspace.N 
	print("we verify N here:", matN)


    # matlab.eval('cartPole_learn') 
	# s = matlab.workspace.sin([0.1, 0.2, 0.3])
	# sorted,idx = matlab.workspace.sort([3,1,2], nout=2)

	print("Done!")
	input()  # to hold the window
	# when Matlab finishes the code or executions, 
	# closes all windows, clears all and closes all
	# but saves the data in cartPole_X_H40.mat

if __name__ == "__main__":
    main()