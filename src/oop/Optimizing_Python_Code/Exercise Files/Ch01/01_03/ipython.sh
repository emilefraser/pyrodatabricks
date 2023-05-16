# measuring time
# ==============
ipython
%run -n using_timeit.py 
%timeit use_get('a')
%timeit use_catch('a') 

# profiling
# =========

# text UI
python -m pstats prof.out
stats 10
sort cumtime

# graphical snakeviz
snakeviz prof.out

# ipython
%run -n prof.py
cases = list(gen_cases(1000))
%prun bench_login(cases)
%prun ?
%prun -s cumulative bench_login(cases)      

