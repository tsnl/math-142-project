## Nikhil's Presentation Liners

- _sets diffusion to 0, grid lines on_
- _returns_
    - "at first, there was nothing but a solid cube of fluid, suspended in cellular space."
    - _pause_
- _sets diffusion to 0.0625_
    - "and then, things were set in motion."
- _returns_
    - "very slowly at first, our simulation of bulk properties expands"
    - "like a dense gas cloud slowly filling a room"
    - _pause_
- but fortunately, we can speed things up
    - set time rate to 1.0
    - watch simulation pass too quickly
- and run things over and over again
    - _reset simulation multiple times in a row_
      - _should be very fast_
- while learning from our mistakes
    - _lower time rate to 0.01_
    - play back again
  
- **welcome to `import antigravity`'s 2d fluid simulation tool**
  - _set spiral field, TR 0.0001, V/D=1_
  - reset, run in background with code explanation

1. Show Stam Paper

2. Show code (files will suffice)
    - `simulator.pyx` with `class Simulator` and many methods
      - can show Cython
    - `app.py` contains GUI code
    - multiple `demo` files => iterative
  
3. Stress on diffuse solver
   - used the Gauss-Seidel method for 20 iterations
   - not guaranteed to converge in practice, e.g.
      - **crank the time rate to 1000**
      - as we can see, the 'rho' aperture tends to infinity
   - but in practice, works well enough
      - imprecision can be cleaned up by sinks + sumps
      - plus the fact that simulations are unlikely to run so long/fast
   - can always replace with a more sophisticated solver: nothing so special about GS except a recommendation

4. Evaluation:
    1. wanted a 'fluid sandbox' to serve as an introduction to simulating PDEs
        - real-time => interactivity => more opportunities to learn
        - numerical methods find 'good enough' solutions for analytically intractable problems
        - 'it works! sometimes! most of the time!' is more than good enough for me
    2. had to devise visualization schemes
        - e.g. 'density aperture' helped reveal this tend to infinity behavior
        - e.g. how to visualize velocity with colors?
        
    2. improvement areas:
        1. investigate maximum over time
            - just added 'aperture' yest. night
        2. how to visualize velocity with colors?
            - could measure some kind of 'friction'
        3. performance... ;-;
            - sub 60 fps pains me
