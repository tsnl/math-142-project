## Nikhil's Presentation Liners

- _sets diffusion to 0, tr = 0.1, grid lines on_
- _returns_
    - "at first, there was nothing but a solid cube of fluid, suspended in cellular space."
    - _pause_
- _sets diffusion to 0.0625_
    - "and then, things were set in motion."
- _returns_
    - "our simulation of bulk properties expands"
    - "like a dense gas cloud slowly filling a room"
    - _pause_
- fortunately, we can speed things up
    - set time rate to 1.0
    - watch simulation pass too quickly
- and run things over and over again
    - _reset simulation multiple times in a row_
      - _should be very fast_
- while learning from our mistakes
    - _lower time rate to 0.1_
    - play back again
- and making changes
    - add downward velocity field
- as many times as we want
    - set time rate to 0.01
    - turn off grid lines

- **welcome to `import antigravity`'s 2d fluid simulation tool**
  - _set spiral field, TR 0.0001, V/D=1_
  - reset, run in background with code explanation

- all of our work was based on this paper by Jos Stam,
    - who discusses the strengths of our diffuse solver in greater depth
    - the 'diffuse' step iteratively transfers weighted density
        - 20 times using Gauss-Seidel method
        - can also use multi-grid to avoid small t-step for smooth surface
    - **stability** of this method is key: converges for small perturbations
    - e.g. setting large time rate does cause divergence, but this can be limited and compensated for
        - e.g. by running more iterations

- also had to apply visualization techniques
    - e.g. density range mimics changing aperture of human eye, highlighting contrast, not abs-val
    - haven't found this 'density aperture' elsewhere, but a useful trick for you ;)
    - open qs:
        - e.g. how to encode velocity?
        - e.g. make mean 0.5f brightness with +- variation: easy enough, just no time :(

- conclusion: this tool debugged itself
    - 'time rate', velocity fields, and 'density aperture' came together really well
    - for me, this course is about exploring DEs with Python, and this tool accomplishes this.

- Questions?
-
