# python translation of  settings_cp.m
# to override the matlab dynamic cart pole sovler and use the one from OpenAI gym
#################################################################
## settings_cp.m
# *Summary:* Script set up the cart-pole scenario
# High-Level Steps
	# Define state and important indices
	# Set up scenario
	# Set up the plant structure
	# Set up the policy structure
	# Set up the cost structure
	# Set up the GP dynamics model structure
	# Parameters for policy optimization
	# Plotting verbosity
	# Some array initializations


# intiialize random seeds and include some paths
def init(matlab):
  matlab.eval("rand('seed',1); randn('seed',1); format short; format compact; ")
  matlab.eval("rd = '../../'; addpath([rd 'base'],[rd 'util'],[rd 'gp'],[rd 'control'],[rd 'loss']);")

# # # 1. Define state and important indices
# # # 1a. Full state representation (including all augmentations)
# # #  1  x          cart position
# # #  2  v          cart velocity
# # #  3  dtheta     angular velocity
# # #  4  theta      angle of the pendulum
# # #  5  sin(theta) complex representation ...
# # #  6  cos(theta) of theta
# # #  7  u          force applied to cart
# # #
# # # 1b. Important indices
# # # odei  indicies for the ode solver
# # # augi  indicies for variables augmented to the ode variables
# # # dyno  indicies for the output from the dynamics model and indicies to loss
# # # angi  indicies for variables treated as angles (using sin/cos representation)
# # # dyni  indicies for inputs to the dynamics model
# # # poli  indicies for the inputs to the policy
# # # difi  indicies for training targets that are differences (rather than values)
def def_state_indices(matlab):
	matlab.eval("odei = [1 2 3 4];") 	#  varibles for the ode solver
	matlab.eval("augi = [];") 			#  variables to be augmented
	matlab.eval("dyno = [1 2 3 4];") 	#  variables to be predicted (and known to loss)
	matlab.eval("angi = [4];") 			#  angle variables
	matlab.eval("dyni = [1 2 3 5 6];") 	#  variables that serve as inputs to the dynamics GP
	matlab.eval("poli = [1 2 3 5 6];") 	#  variables that serve as inputs to the policy
	matlab.eval("difi = [1 2 3 4];") 	#  variables that are learned via differences

# # 2. Set up the scenario
def def_scenario(matlab):
	matlab.eval("dt = 0.10; ")                       # [s] sampling time
	matlab.eval("T = 4.0; ")                         # [s] initial prediction horizon time
	matlab.eval("H = ceil(T/dt); ")                  # prediction steps (optimization horizon)
	matlab.eval("mu0 = [0 0 0 0]'; ")                 # initial state mean
	matlab.eval("S0 = diag([0.1 0.1 0.1 0.1].^2); ")   # initial state covariance
	#N = 4; ")                             # number controller optimizations
	matlab.eval("J = 1; ")                             # initial J trajectories of length H
	matlab.eval("K = 1; ")                             # no. of initial states for which we optimize
	matlab.eval("nc = 10; ")                         # number of controller basis functions

# # 3. Plant structure
def def_plant_st(matlab):
	matlab.eval("plant.dynamics = @dynamics_cp; ")                    # dynamics ode function
	matlab.eval("plant.noise = diag(ones(1,4)*0.01.^2); ")            # measurement noise
	matlab.eval("plant.dt = dt;")
	matlab.eval("plant.ctrl = @zoh;")                                # controler is zero order hold
	matlab.eval("plant.odei = odei;")
	matlab.eval("plant.augi = augi;")
	matlab.eval("plant.angi = angi;")
	matlab.eval("plant.poli = poli;")
	matlab.eval("plant.dyno = dyno;")
	matlab.eval("plant.dyni = dyni;")
	matlab.eval("plant.difi = difi;")
	matlab.eval("plant.prop = @propagated;")

# # 4. Policy structure
def def_policy_st(matlab):
	matlab.eval("policy.fcn = @(policy,m,s)conCat(@congp,@gSat,policy,m,s);")# controller representation
	# matlab.eval("policy.maxU = 10;")                                         # max. amplitude of control
	matlab.eval("policy.maxU = -3;")                                         # max. amplitude of control
	matlab.eval("[mm ss cc] = gTrig(mu0, S0, plant.angi);")                  # represent angles 
	matlab.eval("mm = [mu0; mm]; cc = S0*cc; ss = [S0 cc; cc' ss];")         # in complex plane          
	matlab.eval("policy.p.inputs = gaussian(mm(poli), ss(poli,poli), nc)';") # init. location of basis functions
	matlab.eval("policy.p.targets = 0.1*randn(nc, length(policy.maxU));")    # init. policy targets (close to zero)
	matlab.eval("policy.p.hyp = log([1 1 1 0.7 0.7 1 0.01])';")              # initialize policy hyper-parameters

# # 5. Set up the cost structure
def def_cost_st(matlab):
	matlab.eval("cost.fcn = @loss_cp;")                       # cost function
	matlab.eval("cost.gamma = 1;")                            # discount factor
	matlab.eval("cost.p = 0.5;")                              # length of pendulum
	matlab.eval("cost.width = 0.25;")                         # cost function width
	matlab.eval("cost.expl =  0.0;")                          # exploration parameter (UCB)
	matlab.eval("cost.angle = plant.angi;")                   # index of angle (for cost function)
	matlab.eval("cost.target = [0 0 0 pi]';")                 # target state

# # 6. Dynamics model structure
def def_dyn_st(matlab):
	matlab.eval("dynmodel.fcn = @gp1d;")                # function for GP predictions
	matlab.eval("dynmodel.train = @train;")             # function to train dynamics model
	matlab.eval("dynmodel.induce = zeros(300,0,1);")    # shared inducing inputs (sparse GP)
	matlab.eval("trainOpt = [300 500];")                # defines the max. number of line searches
	             				                        # when training the GP dynamics models
	                                     				# trainOpt(1): full GP,
	                                     				# trainOpt(2): sparse GP (FITC)

# # 7. Parameters for policy optimization
def def_param_policy(matlab):
	matlab.eval("opt.length = 150;")                        # max. number of line searches
	matlab.eval("opt.MFEPLS = 30;")                         # max. number of function evaluations
				                                        	# per line search
	matlab.eval("opt.verbosity = 1;")                       # verbosity: specifies how much 
	                                         # information is displayed during
	                                         # policy learning. Options: 0-3

# # 8. Plotting verbosity
def plot_verb(matlab):
	matlab.eval("plotting.verbosity = 1;") # 0: no plots
#                                    # 1: some plots
#                                    # 2: all plots

# # 9. Some initializations
def last_init(matlab):
	matlab.eval("x = []; y = [];")
	matlab.eval("fantasy.mean = cell(1,N); fantasy.std = cell(1,N);")
	matlab.eval("realCost = cell(1,N); M = cell(N,1); Sigma = cell(N,1);")