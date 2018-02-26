# -*- coding: utf-8 -*-

"""Evaluate m-file and collect the results.  A simple MATLAB script is
located in my_script.m

"""
from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals

import matlab_wrapper


def main():
    matlab = matlab_wrapper.MatlabSession()

    # matlab.put('x', 2.)
    matlab.eval('cartPole_learn')
    # y = matlab.get('y')
    label = matlab.get('basename')

    print("We are executing:", label)


if __name__ == "__main__":
    main()