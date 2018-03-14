from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals
import numpy as np
import math
import matlab_wrapper
import gym
import sett_cp as scp  		
import roll_cp as roll 		
import applyController_cp as appControl


def visualize_traj(matlab):
	if matlab.workspace.plotting.verbosity>0 : 
		if ~matlab.workspace.ishandle(1):
			matlab.eval('figure(1)')
		else:
			matlab.eval("set(0,'CurrentFigure',1)")
		matlab.eval('clf(1)')
		matlab.eval('draw_rollout_cp')	



# 1. Initialization: cartpole environment in gym
env = gym.make('CartPole-v0')
# ob = env.reset()
# fit_state_for_matlab(matlab,ob)
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

# ===================================   # settings_cp   # As follows:
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
# for jj in range(1,matlab.workspace.J.astype(int)+1): # for jj = 1:J
jj=1
matlab.workspace.jj=jj

# **--- Gym step, mu0 and S0 are used in gaussian to generate the state
ob = env.reset()					# gym environment, reset
matlab.workspace.mu0 = roll.fit_stX_for_matlab(matlab,ob) # initialize not with [0,0,0,0]' but with initial state
# matlab.workspace.S0 = []   		#the covariance represents how much do we trust in the state observations of above. So we stick to the default = 0.01
# **---

# ===================================
# [xx, yy, realCost{jj}, latent{jj}] = rollout(gaussian(mu0, S0), struct('maxU',policy.maxU), H, plant, cost) # As follows:
matlab.eval("start_py 	= gaussian(mu0, S0)") 				#BEGINNING OF WORKAROUND for rollout function
matlab.eval("policy_py 	= struct('maxU',policy.maxU)")
matlab.eval("H_py 		= H")
matlab.eval("plant_py 	= plant")
matlab.eval("cost_py 	= cost")
roll.rollout(matlab,env)    									# FUNCTION ====
matlab.workspace.xx = matlab.workspace.x_py
matlab.workspace.yy = matlab.workspace.y_py
matlab.eval("realCost{jj} 	= L_py;")
matlab.eval("latent{jj}		= latent_py;")
matlab.eval("clear x_py")     
matlab.eval("clear y_py")
matlab.eval("clear L_py")
matlab.eval("clear latent_py") 								#END OF WORKAROUND 
# ===================================

matlab.eval("x = [x; xx]; y = [y; yy];")       # augment training sets for dynamics model
visualize_traj(matlab)


# matlab.eval("mu0Sim(odei,:) = mu0; S0Sim(odei,odei) = S0;")
# matlab.eval("mu0Sim = mu0Sim(dyno); S0Sim = S0Sim(dyno,dyno);")

# 	# matlab.workspace.x.ndim   # gives the nr of dims bc they're numpy arrays
# 	# matlab.workspace.x.shape   # gives the size bc they're numpy arrays
# 	# matlab.workspace.x[0,:]  # PYTHON HIERARCHY! row nr 0,  40 x 7 [H x nX+nU]



# ######------------ 3. Controller learning
# # for j = 1:N
# j=1
# matlab.workspace.j=j
# matlab.eval("trainDynModel;")#   # train (GP) dynamics model
# matlab.eval("learnPolicy;")#     # learn policy
# appControl.apply(matlab,env)		# matlab.eval("applyController;")	# apply controller to system


# print("controlled trial # %d" %j)
# visualize_traj(matlab)



# # Saving controller outputs per timestep to a file
# f1=open('u.txt', 'w+')
# for u_item in matlab.workspace.x[:,6]:  #all rows, column 7 in Matlab, 6 in python
# 	f1.write("%s\n" %u_item)
# f1.close()



# # s = matlab.workspace.sin([0.1, 0.2, 0.3])
# # sorted,idx = matlab.workspace.sort([3,1,2], nout=2)

# print("Done!")
input()