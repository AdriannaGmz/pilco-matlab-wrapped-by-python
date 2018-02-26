import matlab_wrapper

# import numpy as np
# from numpy import pi
# start_state = np.array( [ pi/2.0, 0.0, 0.0, 0.0 ] )


# Initiate a Matlab session
matlab = matlab_wrapper.MatlabSession() 

# Low level
matlab.put('a', 12.3)
matlab.eval('b = a * 2')
b = matlab.get('b')
print b

# Workspace:
s = matlab.workspace.sin([0.1, 0.2, 0.3])
sorted,idx = matlab.workspace.sort([3,1,2], nout=2)
matlab.workspace.c = 29.3
d = matlab.workspace.c*2



