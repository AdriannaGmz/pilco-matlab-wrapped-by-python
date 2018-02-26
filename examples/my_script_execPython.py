# -*- coding: utf-8 -*-

"""Evaluate m-file and collect the results.  A simple MATLAB script is
located in my_script.m

"""
from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals

import matlab_wrapper


def main():
    matlab = matlab_wrapper.MatlabSession()

    matlab.put('x', 2.)
    matlab.eval('my_script')
    # matlab.eval('scenarios/cartPole/cartPole_learn')   #doesnt understand directory navigation!!!
    y = matlab.get('y')
    a = matlab.get('a')

    print("And the winner is:", y)
    print(a)


if __name__ == "__main__":
    main()
