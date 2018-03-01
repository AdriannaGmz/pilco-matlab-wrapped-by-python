# -*- coding: utf-8 -*-

""" 
Instead of evaluating cartPole_learn.m 
emulate its matlab commands
"""
from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals

import matlab_wrapper


def main():
    matlab = matlab_wrapper.MatlabSession()
	# 1. Initialization
    # matlab.eval('close all')  #command not supported
    matlab.eval('clear all') 
    matlab.eval('settings_cp')   			#load scenario-specific settings
	matlab.put('basename', 'cartPole_')     # filename used for saving data

	# 2. Initial J random rollouts
    matlab.put('x', 2.)


    # matlab.eval('cartPole_learn') 
    # matlab.put('x', 2.)
    # y = matlab.get('y')
    # print("We are executing:", y)
    print("Done!")


if __name__ == "__main__":
    main()
