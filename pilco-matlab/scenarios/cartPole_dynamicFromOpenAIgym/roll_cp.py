# Python translation of rollout.m
# Overrides the matlab cart pole dynamic solver and uses the model from OpenAI gym
#################################################################
## rollout.m
# *Summary:* Generate a state trajectory using an ODE solver (and any additional 
# dynamics) from a particular initial state by applying either a particular 
# policy or random actions.
#
#   function [x y L latent] = rollout(start, policy, H, plant, cost)
#
# *Input arguments:*
#   
#   start       vector containing initial states (without controls)   [nX  x  1]
#   policy      policy structure
#     .fcn        policy function
#     .p          parameter structure (if empty: use random actions)
#     .maxU       vector of control input saturation values           [nU  x  1]
#   H           rollout horizon in steps
#   plant       the dynamical system structure
#     .subplant   (opt) additional discrete-time dynamics
#     .augment    (opt) augment state using a known mapping
#     .constraint (opt) stop rollout if violated
#     .poli       indices for states passed to the policy
#     .dyno       indices for states passed to cost
#     .odei       indices for states passed to the ode solver
#     .subi       (opt) indices for states passed to subplant function
#     .augi       (opt) indices for states passed to augment function
#   cost    cost structure
#
# *Output arguments:*
#
#   x          matrix of observed states                           [H   x nX+nU]
#   y          matrix of corresponding observed successor states   [H   x   nX ]
#   L          cost incurred at each time step                     [ 1  x    H ]
#   latent     matrix of latent states                             [H+1 x   nX ]
#
## High-Level Steps
#
# # Compute control signal $u$ from state $x$:
# either apply policy or random actions
# # Simulate the true dynamics for one time step using the current pair $(x,u)$
# # Check whether any constraints are violated (stop if true)
# # Apply random noise to the successor state
# # Compute cost (optional)
# # Repeat until end of horizon
import numpy as np

def fit_stX_for_matlab(matlab,ob): #x          matrix of observed states                           [H   x nX+nU]
  # OpenAI vector state is:     x, x_dot, theta,  theta_dot         % is an array
  # Matlab vector state needs:  x, x_dot, dtheta, theta,  sin(theta), cos(theta)
  #  1  x          cart position
  #  2  v          cart velocity
  #  3  dtheta     angular velocity
  #  4  theta      angle of the pendulum
  #  5  sin(theta) complex representation ...
  #  6  cos(theta) of theta
  #***  7  u          force applied to cart
  # stheta = math.sin(theta)
  # ctheta = math.cos(theta)
  # ob_for_matlab = np.array([ob[0],ob[1],ob[3],ob[2], math.sin(ob[2]), math.cos(ob[2])])
  # return np.array([ob[0],ob[1],ob[3],ob[2], math.sin(ob[2]), math.cos(ob[2])])
  return np.array([ob[0],ob[1],ob[3],ob[2]])

# def fit_stY_for_matlab(matlab,ob): #y          matrix of corresponding observed successor states   [H   x   nX ]
#   # OpenAI vector state is:     x, x_dot, theta,  theta_dot         % is an array
#   # Matlab vector state needs:  x, x_dot, dtheta, theta
#   return np.array([ob[0],ob[1],ob[3],ob[2]])

def map_u_discrete(matlab):
  # print(matlab.workspace.u.shape)
  u = matlab.workspace.u.copy() 
  if u[matlab.workspace.i-1] < 0:  # i-1 in python corresponds to i in matlab
    u[[matlab.workspace.i-1]] = 0
    # print("negative")
  else:
    u[[matlab.workspace.i-1]] = 1
    # print("positive")
  # print(u.shape)
  matlab.workspace.u = u.copy()
  # print(matlab.workspace.u.shape)



def rollout(matlab,env):       # function [x y L latent] = rollout(start, policy, H, plant, cost)
  # WORKAROUND:    USE NAMES  _py for the incoming / outgoing arguments
  # matlab.workspace.start_py 
  # matlab.workspace.policy_py 
  # matlab.workspace.H_py
  # matlab.workspace.plant_py 
  # matlab.workspace.cost_py 

  # matlab.workspace.x_py 
  # matlab.workspace.y_py 
  # matlab.workspace.L_py 
  # matlab.workspace.latent_py 

  # sort out indices!
  matlab.eval("if isfield(plant_py,'augment'), augi = plant_py.augi;else plant_py.augment = inline('[]'); augi = []; end")
  matlab.eval("if isfield(plant_py,'subplant'), subi = plant_py.subi;else plant_py.subplant = inline('[]',1); subi = []; end")
  matlab.eval("odei = plant_py.odei; poli = plant_py.poli; dyno = plant_py.dyno; angi = plant_py.angi;")
  matlab.eval("simi = sort([odei subi]);")
  matlab.eval("nX = length(simi)+length(augi); nU = length(policy_py.maxU); nA = length(angi);")
  # initializations
  matlab.eval("state(simi) = start_py; state(augi) = plant_py.augment(state);")      
  matlab.eval("x_py = zeros(H_py+1, nX+2*nA);")
  matlab.eval("x_py(1,simi) = start_py' + randn(size(simi))*chol(plant_py.noise);")
  matlab.eval("x_py(1,augi) = plant_py.augment(x_py(1,:));")
  matlab.eval("u = zeros(H_py, nU); latent_py = zeros(H_py+1, size(state,2)+nU);")
  matlab.eval("y_py = zeros(H_py, nX); L_py = zeros(1, H_py); next = zeros(1,length(simi));")

# for i = 1:H_py # --------------------------------------------- generate trajectory
  for i in range(1,matlab.workspace.H_py.astype(int)+1): 
    matlab.workspace.i=i
    matlab.eval("s = x_py(i,dyno)'; sa = gTrig(s, zeros(length(s)), angi); s = [s; sa];")
    matlab.eval("x_py(i,end-2*nA+1:end) = s(end-2*nA+1:end);")

    # 1. Apply policy ... or random actions --------------------------------------
    if matlab.eval("isfield(policy_py, 'fcn')"):      # apply policy
      matlab.eval("u(i,:) = policy_py.fcn(policy_py,s(poli),zeros(length(poli))); ")
    else:                                             # apply random action
      matlab.eval("u(i,:) = policy_py.maxU.*(2*rand(1,nU)-1); ")
    # print(matlab.workspace.u[matlab.workspace.i-1])    
    map_u_discrete(matlab)                                            # maps from [-1,...,+1] to (0,1)
    # matlab.eval("latent_py(i,:) = [state u(i,:)];")                                  # latent state
    matlab.eval("u = u'; latent_py(i,:) = [state u(i,:)];")                            # openai. latent state

    # 1a. step openai env with the requested action---------------------------------    
    action_env = matlab.workspace.u[i-1].astype(int)
    print("Action %d for timestep i=%d" %(action_env,i))
    state, reward, done, _ = env.step(action_env) 
    env.render()
    if done: 
      break
      print("\t\t Episode over!!! ")


    # 2. Simulate dynamics -------------------------------------------------------
    # matlab.eval("next(odei) = simulate(state(odei), u(i,:), plant_py);")
    # matlab.eval("next(subi) = plant_py.subplant(state, u(i,:));")
    matlab.workspace.next_state = fit_stX_for_matlab(matlab,state)               # openai. dyns
    matlab.eval("next(odei) = next_state;")

    # 3. Stop rollout if constraints violated ------------------------------------
    if matlab.eval("isfield(plant_py,'constraint') && plant_py.constraint(next(odei))"):
      matlab.eval("H_py = i-1;")
      matlab.workspace.stConstrain = 1
      print("Constraints violated \n")
      break
    else:
      matlab.workspace.stConstrain = 0
    matlab.eval("clear stConstrain")

    
    # 4. Augment state and randomize ---------------------------------------------
    matlab.eval("state(simi) = next(simi); state(augi) = plant_py.augment(state);")
    matlab.eval("x_py(i+1,simi) = state(simi) + randn(size(simi))*chol(plant_py.noise);")
    matlab.eval("x_py(i+1,augi) = plant_py.augment(x_py(i+1,:));")

    # 5. Compute Cost ------------------------------------------------------------
    # matlab.eval("L_py(i) = cost_py.fcn(cost_py,state(dyno)',zeros(length(dyno)));")
    # print("matlab cost %f" %matlab.workspace.L_py[matlab.workspace.i-1])        #0.99

      # OPENAI Environment reward:
      # A reward of +1 is provided for every timestep that the pole remains upright. 
      # The episode ends when the pole is more than 15 degrees from vertical, 
      # or the cart moves more than 2.4 units from the center.               
    print("\t openai env reward %f" %reward)                                             #1
    matlab.workspace.cost_env = -reward;         
    matlab.eval("L_py(i) = cost_env;")
    print("\t supposedly modf cost %f" %matlab.workspace.L_py[matlab.workspace.i-1])        #-1


  matlab.eval("y_py = x_py(2:H_py+1,1:nX); x_py = [x_py(1:H_py,:) u(1:H_py,:)]; ")
  matlab.eval("latent_py(H_py+1, 1:nX) = state; latent_py = latent_py(1:H_py+1,:); L_py = L_py(1,1:H_py);")



  matlab.eval("clear start_py")       #CLEANING WORKAROUND 
  matlab.eval("clear policy_py")
  matlab.eval("clear H_py")
  matlab.eval("clear plant_py")
  matlab.eval("clear cost_py")
  return
