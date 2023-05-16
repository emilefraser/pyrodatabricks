General Tips
============

- use real data
- turn off anti-virus programs
- have a test suite ready
- know when to measure - code has warm up time


Measuring Time
==============

Why
 - choose between alternatives
 - gauge code improvement
 - get metrics on runtime

Python Methods:
 - time module
 - timeit module
 - python3 includes monotonic and perf_Counter functions for high-resolution monotonic timers

Computers and time:
 - it's tricky - https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time
 - Measurements of elapsed time include time when processes are sleeping
 
CPU Profiling
=============

- cProfile is recommended by python - deterministic
- Deterministic profilers record every function call, return, exception
- Where-as statistical profilers - record where the profiler is at small intervals
- Pstats module -> displays profiler stats file

Line Profile
============

- line_profile -> measure lower grain than functions
- includes cmd-line program kernprof
- prfiles explicit decorators @profile







