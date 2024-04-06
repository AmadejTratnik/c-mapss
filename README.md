# Fault Detection of JET engine
*Reading an article *Damage Propagation Modelling for Aircraft Engine Run-to-Failure Simulation* and trying to reformat it into a fault detection pipeline of a jet engine, with the help of C-MAPPS dataset and reccurent neural networks.*

[<img src="app/assets/image.png" width="250"/>](app/assets/image.png) 

## Installation
Download the project from GitHub and change your current directory:
```
$ (base) cd c-mapps
```
Use a virtual environment to isolate your environment, and install the required dependencies.
```
$ (base) python3 -m venv venv
$ (base) source venv/bin/activate
$ (venv) pip3 install -r requirements.txt
```

To start Fault Detector app, simply write:
```
$ (venv) python3 app/visualisation.py
```
# [Modelling](./modelling/README.md)


