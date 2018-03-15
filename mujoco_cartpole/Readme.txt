To execute it in Asus Ubuntu with NVIDIA GFORCE 745M:

LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so python3 cartSim.py 

else:

python3 cartSim.py 




Displays:  (constant control input 2, but may be changed)

simulation time: 1.040 
	qpos = 0.991109	-12.028946 	 qvel = -0.027222	-10.374097 	 ctrl = 2.000000



#Simulation
		# sim.data.qpos 	#position of states
		# sim.data.qvel
		# sim.data.nf  		# nr of joints
		# sim.data.ctrl 	# nr of control inputs (1, range -3 a 3)

state is 
	MjSimState(time=0.0, qpos=array([0., 0.]), qvel=array([0., 0.]), act=None, udd_state={})
