In this folder, the idea is to interact directly with the Model of Mujoco
and NOT to learn from the matlab Model specified in the settings_cp_forPython.m

The key idea is to succeed in this connection 

#### FUTURE

As another stage, would be the transfer of learning:
* not knowing the dynamics of mujoco and obviously it will be different from the one that will be learnt in Matlab. 

the idea would be to learn from a Dynamic Model (specified in the settings_cp_forPython.m) and take that learning to the Dynamic Model of Mujoco, which provides the environment. 

I dont know the dynamics of Mujoco AI and obviously it will be different from the one that will be learnt in Matlab. but here the key idea is to manage the connection from matlab into providing commands at a certain time step so they are fed in the environment (generated in python, OpenAI gym runs in python).
*although that would be a plus bc obviously both systems have different dyns

