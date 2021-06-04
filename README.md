# math-142-project

<!-- For some infernal reason, iMovie will not export weird aspect ratios. Good enough, I say. -->
<img
    src="doc/Project Demo 1.gif"
    style="object-fit: none; object-position: -290px 0; width: 700px; height: 720px"
 />

A project on fluid simulation for MATH 142.

## Getting Started

0.  First, ensure you have `python3.9` installed with `pip`.
    Further ensure you have a working C++ compiler.
    Open a terminal with the directory containing this file as the working directory.
    Enter each command below to set-up this project.
    The commands are meant for Unix systems.
    If you use Windows, getting a Python toolchain working may be tricky, but if you 
    have one, translating the below commands will be a cinch. 
    I've not tried running GUI apps under WSL2, but apparently, it is now supported?

    1.  Run `$ /usr/bin/env python3.9 ./setup.py build_ext --inplace`
        
        This command compiles an extension 

    2.  Run `$ /usr/bin/env python3.9 -m pip install -r ./requirements.txt`

        This command installs all Python package dependencies to the system-wide 
        location.

        If you would rather not pollute your system installations, try
        `virtualenv`s-- the same `requirements.txt` file is used.

1.  Run 

    ```
    $ python3.9 run-demo4.py
    ```

    to view our latest and greatest demo in `500x500px` glory (compatible monitor required).



## Resources

0. Jos Stam - Real-Time Fluid Dynamics for Games (2D) 

    https://www.dgp.toronto.edu/public_user/stam/reality/Research/pdf/GDC03.pdf

    - explains how to perform a 2D fluid simulation with C code

1.  Demo of this fluid simulation in JavaScript

    https://www.cs.utexas.edu/~teammco/projects/fluids_simulation/

2.  Jos Stam | `wavefront`- Stable Fluids (2D/3D)

    https://d2f99xq7vri1nk.cloudfront.net/legacy_app_files/pdf/ns.pdf
    - copy available locally in [/doc](/doc/Jos%20Stam%20-%20Stable%20Fluids.pdf).

3.  Mike Ash - Fluid Simulation for Dummies  (Applying Stam for 3D)

    https://mikeash.com/pyblog/fluid-simulation-for-dummies.html
