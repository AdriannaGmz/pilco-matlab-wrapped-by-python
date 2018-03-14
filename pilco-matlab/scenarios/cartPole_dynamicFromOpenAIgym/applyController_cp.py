# Python translation of applyController.m
# Overrides the matlab cart pole dynamic solver and uses the model from OpenAI gym
#################################################################
## applyController.m
# *Summary:* Script to apply the learned controller to a (simulated) system
#
## High-Level Steps
# # Generate a single trajectory rollout by applying the controller
# # Generate many rollouts for testing the performance of the controller
# # Save the data

import roll_cp as roll    #python version of rollout.m

def visualize_cost(matlab):
  if matlab.workspace.plotting.verbosity>0 : 
    if ~matlab.workspace.ishandle(3):
      matlab.eval('figure(3)')
    else:
      matlab.eval("set(0,'CurrentFigure',3)")
    matlab.eval("hold on")
    matlab.eval("plot(1:length(realCost{J+j}),realCost{J+j},'r');")  
    matlab.eval("drawnow")


def apply(matlab,env):
  # 1. Generate trajectory rollout given the current policy
  matlab.eval("if isfield(plant,'constraint'), HH = maxH; else HH = H; end")
  
  matlab.workspace.mu0 = roll.fit_stX_for_matlab(matlab,ob) # initialize not with [0,0,0,0]' but with initial state

  # =================================== ROLLOUT
  # [xx, yy, realCost{j+J}, latent{j}] = rollout(gaussian(mu0, S0), policy, HH, plant, cost);   # As follows:
  matlab.eval("start_py   = gaussian(mu0, S0)")    #BEGINNING OF WORKAROUND for rollout function
  matlab.eval("policy_py  = policy")
  matlab.eval("H_py       = HH")
  matlab.eval("plant_py   = plant")
  matlab.eval("cost_py    = cost")
  roll.rollout(matlab)                              # FUNCTION 
  matlab.workspace.xx         = matlab.workspace.x_py
  matlab.workspace.yy         = matlab.workspace.y_py
  matlab.eval("realCost{j+J}  = L_py;")
  matlab.eval("latent{j}      = latent_py;")
  matlab.eval("clear x_py")     
  matlab.eval("clear y_py")
  matlab.eval("clear L_py")
  matlab.eval("clear latent_py")                    #END OF WORKAROUND 
  # ===================================
  print(matlab.workspace.xx)          # disp(xx); # display states of observed trajectory
  matlab.eval("x = [x; xx]; y = [y; yy];")        # augment training sets 

  # # 2. Make many rollouts to test the controller quality
  if matlab.workspace.plotting.verbosity>1 : 
    matlab.eval("lat = cell(1,10);")
    for i in range(1,10+1):
      matlab.workspace.i = i
      # =================================== ROLLOUT
      # [~,~,~,lat{i}] = rollout(gaussian(mu0, S0), policy, HH, plant, cost);   # As follows:
      matlab.eval("start_py   = gaussian(mu0, S0)")   #BEGINNING OF WORKAROUND for rollout function
      matlab.eval("policy_py  = policy")
      matlab.eval("H_py       = HH")
      matlab.eval("plant_py   = plant")
      matlab.eval("cost_py    = cost")
      roll.rollout(matlab)                            #FUNCTION 
      matlab.eval("lat{i}      = latent_py;")
      matlab.eval("clear x_py")     
      matlab.eval("clear y_py")
      matlab.eval("clear L_py")
      matlab.eval("clear latent_py")                  #END OF WORKAROUND 
      # ===================================
    if ~matlab.workspace.ishandle(4):
      matlab.eval('figure(4)')
    else:
      matlab.eval("set(0,'CurrentFigure',4)")
    matlab.eval("clf(4)")

    matlab.eval("ldyno = length(dyno);")
    for i in range(1,matlab.workspace.ldyno.astype(int)+1):     #for i=1:ldyno       # plot the rollouts on top of predicted error bars
      matlab.workspace.i = i
      matlab.eval("subplot(ceil(ldyno/sqrt(ldyno)),ceil(sqrt(ldyno)),i); hold on;")
      matlab.eval("errorbar( 0:length(M{j}(i,:))-1, M{j}(i,:), 2*sqrt(squeeze(Sigma{j}(i,i,:))) );")
      for ii in range (1,10+1):       # for ii=1:10
        matlab.workspace.ii = ii
        matlab.eval("plot( 0:size(lat{ii}(:,dyno(i)),1)-1, lat{ii}(:,dyno(i)), 'r' );")
      matlab.eval("plot( 0:size(latent{j}(:,dyno(i)),1)-1, latent{j}(:,dyno(i)),'g');")
      matlab.eval("axis tight")
    matlab.eval("drawnow;")

  # # 3. Save data
  matlab.eval("filename = [basename num2str(j) '_H' num2str(H)]; save(filename);")
