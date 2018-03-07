# PILCO in Python
* PILCO's author (M. Deisenroth) published the [Matlab Code](http://mlg.eng.cam.ac.uk/pilco/).
* Marek Rudnicki published a [python wrapper for Matlab programs](https://zenodo.org/badge/latestdoi/24233/mrkrd/matlab_wrapper)

So here I combined both in order to have PILCO working in Python



# Goal
To get [PILCO matlab implementation](http://mlg.eng.cam.ac.uk/pilco/) working in Python scripts enabled by the [matlab wrapper](https://github.com/mrkrd/matlab_wrapper).


# Requirements

* [Matlab's PILCO implementation](http://mlg.eng.cam.ac.uk/pilco/)
* [Matlab-python wrapper](https://github.com/mrkrd/matlab_wrapper)
* Matlab-python wrapper reqs:
	* Python 2.7
	* MATLAB (various versions)
	* Numpy
	* csh  install by ``sudo apt-get install csh``


# Installing

Although I don't remember installing the wrapper by pip (I just downloaded the project from the github), they recommend it:
```sh
pip install matlab_wrapper
```


# Execute it

We assume that the three directories are in the same path (same level)

* pilco-matlab  		(Matlab code for PILCO)
* matlab_wrapper 		(the wrapper)
* examples			 	(self explaining)



## Pilco from Matlab in Python: cartPole

From  _pilco-matlab/scenarios/cartPole-diffDynamic_

execute
```sh
python cartPole_learn_python.py
```



## other examples of matlab wrapper

In _examples_ directory, execute
```sh
python simpleCommands.py
```
or
```sh
python my_script_execPython.py
```



# Limitations

* Command matlab.eval('my_script') does not understand directory navigating system (../ or /myfolder/), that's why the python Files are directly where the .m file is



# References

* [PILCO in Matlab by Marc Deisenroth, 2010](http://mlg.eng.cam.ac.uk/pilco/)
* [Matlab wrapper for python, March 2017](https://zenodo.org/badge/latestdoi/24233/mrkrd/matlab_wrapper)

---
# README from Original PILCO Matlab Github

PILCO Software Package V0.9 (2013-07-04)

I. Introduction
This software package implements the PILCO RL policy search framework. The learning framework can be applied to MDPs with continuous states and controls/actions and is based on probabilistic modeling of the dynamics and approximate Bayesian inference for policy evaluation and improvement.



II. Quick Start
We have already implemented some scenarios that can be found in
<PILCO-ROOT>/scenarios .

If you want to get started immediately, go to
<PILCO-ROOT>/scenarios/cartPole

and execute

cartPole_learn



III. Documentation
A detailed documentation can be found in

<PILCO-ROOT>/doc/doc.pdf

which also includes a description of how to set up your own scenario (there are only a few files that are scenario specific).



IV. Contact
If you find bugs, have questions, or want to give us feedback, please send an email to
m.deisenroth@imperial.ac.uk


V. References
M.P. Deisenroth and C.E. Rasmussen: PILCO: A Data-Efficient and Model-based Approach to Policy Search (ICML 2011)
M.P. Deisenroth: Efficient Reinforcement Learning Using Gaussian Processes (KIT Scientific Publishing, 2010)



Marc Deisenroth
Andrew McHutchon
Joe Hall
Carl Edward Rasmussen
