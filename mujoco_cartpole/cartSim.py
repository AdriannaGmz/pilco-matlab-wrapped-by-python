# Nvidia GForce 745M:   		LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so python3
from mujoco_py import load_model_from_path, MjSim, MjViewer
import numpy as np
import os




# Environment
model = load_model_from_path("./xml/cartpole.xml") 		# initialisation / loading the model
sim = 	MjSim(model) 									# MjSim is the running simulation including its state
simulation_data = []

#Rendering
viewer = MjViewer(sim) 
viewer.cam.distance = model.stat.extent * 1.2
viewer.render()

ref_pose = np.array([0,0,0,0])

#Simulation
		# sim.data.qpos 	#position of states
		# sim.data.qvel
		# sim.data.nf  		# nr of joints
		# sim.data.ctrl 	# nr of control inputs (1, range -3 a 3)
while True:
    state 	= sim.get_state()     			# MjSimState(time=0.0, qpos=array([0., 0.]), qvel=array([0., 0.]), act=None, udd_state={})
    simulation_data.append(state)
    print('simulation time: {0:.3f} \n'.format(state.time), end='\r')
    print('\tqpos = %f\t%f \t qvel = %f\t%f \t ctrl = %f' %(state.qpos[0],state.qpos[1],state.qvel[0],state.qvel[1],sim.data.ctrl[0]), end='\r')

    # reset environment every 3 sec
    	# ref_pose = random_pose(-2,2,sim.data.nf) # change to random joint configuration
    # print('\n\t\tmy time contidion = %f' %(state.time%1.0))
    # if state.time%1.0 == 0.0:
    	# sim.reset()   #Resets the simulation data and clears buffers

    sim.step()
    viewer.render()
    # sim.data.ctrl[:] = input("\n\tGive the control -3 to 3 ..")
    sim.data.ctrl[:] = 2
    input()
