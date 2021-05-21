# Project Report

You can follow our up-to-date work at [https://github.com/tsnl/math-142-project]
- all file-path links refer to this repository
- all individuals referred to in the 3rd person

We are working on a real-time fluid simulation based on the work of Jos Stam.
- `tsnl`/Nikhil has had a deep pre-existing fascination with fluid simulations
- `tsnl` has recently taken MATH 151AB on numerical analysis and wanted to apply 
  these techniques now that he could understand them.
    - e.g. Gauss-Seidel Relaxation
- Stam et al published a shockingly stable method to integrate the Navier-Stokes 
  equations.
    - today, there exists no analytic solution for this equation system
    - we want to learn about using numerical techniques to understand such systems
    - numerical methods are much easier to deploy and adapt to complexities unseen
      except by the most skilled analysts.
    - numerical methods can be made interactive, to help illuminate aspects of a 
      solution's behavior in an intuitive way for technical and non-technical 
      audiences alike.
    - who doesn't love voxels, especially nowadays with ray-tracing?

Inspired by [this online demo](https://www.cs.utexas.edu/~teammco/projects/fluids_simulation/)...

Nikhil implemented [Stam's Paper](/doc/Jos%20Stam%20-%20Real%20Time%20Fluid%20Sim%20-%20GDC03.pdf)
as found on his website.
- architecturally speaking, our project uses a `kernel/shell` design
  - we use a **C-level 'kernel'** to perform heavy number-crunching operations: cf [`simulator.pyx`](/fluids/simulator.pyx)
    - the kernel has relatively few runtime protections, and is kept very simple-- C-level
    - each `FluidGrid` models a square grid of cells that each contain `float density` and `vec2f velocity` 
      components.
    - kernel uses lowest-level matrix arithmetic and parallelization techniques to speed up solving this
      system.
      - **NOTE:** Work in progress, may be rendered unnecessary & out of scope, listed as an extension
      - **NOTE:** Nikhil wants to continue working on this code after this class ends, so not just a bluff--
        code and interfaces architected to reflect this intent.
    - kernel written in `cython` programming language: a union of `C` and `Python3` that is excellent for 
      these use-cases.
      - `Cython` also supports interop with `C++` libraries via a `C` FFI and the hard work of contributors to create wrappers.
      - There are few languages better-suited to our needs.
      - This lets us elide `numpy`
    - Future extensions:
      - If we understand the matrix math, write a `tensorflow` backend to leverage GPU acceleration
      - If we understand parallelizability, improve the `cython` software backend to use multiple cores
      - Support for multiple backends out of scope of this project, but vital for real-world use.
        - Requires clearly defined interface
      - [3d version available here, courtesy Mike Ash](https://mikeash.com/pyblog/fluid-simulation-for-dummies.html)
  - the kernel interfaces with **a Python shell** that manages user input and presents the simulation state
    - `input`: the shell handles buttons, sliders, and/or text-boxes to allow user-input
    - `input`: the shell allows the user to 'draw' density and velocity using their cursor
    - `output`: the simulation is slow for many cells, so it is better for each simulation cell to correspond to
        a 16 x 16 block of pixels. This rendering multi-plexing as well as color assignment is the shell's
        responsibility.
    - the shell communicates with the kernel via a well-defined interface
      - all the kernel's 'inputs' are persistent, and exist in retained mode
      - the shell can modify retained data that is initialized at program startup
      - each iteration of the kernel works on this retained data
      - cf. OpenGL 3.3+, Vulkan
- this architecture lets us divide work among programmers easily:
  - `@tsnl` works on the kernel
  - `@zach-wong` works on the shell

Nikhil is especially proud of the `time rate` parameter:
- a simple trick borrowed from video-games
- multiply the `dt` by a scale factor called the `time rate`
  - `time rate = 1` => real-time simulation, `dt` corresponds 1:1 with wall-clock time.
  - `time rate < 1` => slow-motion, `dt` artificially lowered
  - `time rate > 1` => fast-forward
- **leveraging Stam's method's stability over large/varying `dt`**
  - this technique _never drops frames_, even in slow-motion, preserving an even frame-time
  - this technique _never rarely loses precision upon being sped up_
  - this technique really makes fluid simulations look pretty
  - this feature helped debug our fluid states, by letting us examine extremely quick events.

Recognizing that it is easier to understand something once implemented,
**we are now working on rigorously understanding the mathematics used**
- Haoran is spearheading the theoretical portion.
- Stam's papers in the `/doc/` folder outline these ideas within the course's analytical framework
- What is the _method of characteristics_?
- How can we use quiver and countour plots to better illustrate velocity and density?
- What do phase plots look like?

Summary:
- Nikhil delivered the kernel and demos 1-3 on May 18
- Zach is working on the shell
- Haoran is working on the mathematics
