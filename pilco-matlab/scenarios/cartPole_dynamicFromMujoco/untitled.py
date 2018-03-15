# Nvidia GForce 745M:   		LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so python3

from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals
# import os  
from mujoco_py import load_model_from_path, MjSim, MjViewer
import sett_cp as scp  		#python version of settings_cp.m
import roll_cp as roll 		#python version of rollout.m
import applyController_cp as appControl

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


# 1. Initialization: cartpole environment in Mujoco
	# Environment
model = load_model_from_path("./cartpole.xml") 			
sim = 	MjSim(model) 									# MjSim is the running simulation including its state
simulation_data = []

	#Rendering
viewer = MjViewer(sim) 
viewer.cam.distance = model.stat.extent * 1.2
viewer.render()


# 1. Initialization: pilco in matlab
N = 2.0   								#number controller optimizations
matlab = matlab_wrapper.MatlabSession()
# matlab.eval('clear all') 
# matlab.eval('close all') 
# matlab.workspace.N = N 	# Override Nr controller optimizations
# # matlab.put('N', N) 	# Same as line above
# # matN = matlab.get('N') 


# # ===================================
# # settings_cp   # As follows:
# scp.init(matlab)
# scp.def_state_indices(matlab)
# scp.def_scenario(matlab)
# scp.def_plant_st(matlab)
# scp.def_policy_st(matlab)
# scp.def_cost_st(matlab)
# scp.def_dyn_st(matlab)
# scp.def_param_policy(matlab)
# scp.plot_verb(matlab)
# scp.last_init(matlab)
# # ===================================
# matlab.workspace.basename= 'cartPole_py_'


# # 2. Initial J random rollouts
# # for jj in range(1,matlab.workspace.J.astype(int)+1): # for jj = 1:J
# jj=1
# matlab.workspace.jj=jj
# # **--- Mujoco step. mu0 and S0 are used in gaussian to generate the state
# sim.reset()
# state 	= sim.get_state()
# matlab.workspace.mu0 = roll.fit_stX_for_matlab(matlab,state) 	# initialize not with [0,0,0,0]' but with initial state
# # matlab.workspace.S0 = []   		#the covariance represents how much do we trust in the state observations of above. So we stick to the default = 0.01
# # **---

# # ===================================
# # [xx, yy, realCost{jj}, latent{jj}] = rollout(gaussian(mu0, S0), struct('maxU',policy.maxU), H, plant, cost) # As follows:
# matlab.eval("start_py 	= gaussian(mu0, S0)") 				#BEGINNING OF WORKAROUND for rollout function
# matlab.eval("policy_py 	= struct('maxU',policy.maxU)")
# matlab.eval("H_py 		= H")
# matlab.eval("plant_py 	= plant")
# matlab.eval("cost_py 	= cost")
# roll.rollout(matlab)    									# FUNCTION ====
# matlab.workspace.xx = matlab.workspace.x_py
# matlab.workspace.yy = matlab.workspace.y_py
# matlab.eval("realCost{jj} 	= L_py;")
# matlab.eval("latent{jj}		= latent_py;")
# matlab.eval("clear x_py")     
# matlab.eval("clear y_py")
# matlab.eval("clear L_py")
# matlab.eval("clear latent_py") 								#END OF WORKAROUND 
# # ===================================

# matlab.eval("x = [x; xx]; y = [y; yy];")       # augment training sets for dynamics model
# visualize_traj(matlab)


# matlab.eval("mu0Sim(odei,:) = mu0; S0Sim(odei,odei) = S0;")
# matlab.eval("mu0Sim = mu0Sim(dyno); S0Sim = S0Sim(dyno,dyno);")


# ######------------ 3. Controller learning
# matlab.workspace.j=1
# matlab.eval("trainDynModel;")#   # train (GP) dynamics model
# matlab.eval("learnPolicy;")#     # learn policy
# appControl.apply(matlab)		# matlab.eval("applyController;")	# apply controller to system
# input()
