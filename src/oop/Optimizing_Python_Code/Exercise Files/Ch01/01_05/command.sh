kernprof -l prof.py
python -m line_profiler prof.py.lprof

ipython
# -n -> don't run the main
%run -n prof.py
cases = list(gen_cases(1000))
%load_ext line_profiler
%lprun -f login bench_login(cases)

%run -n login.py
passwd = 'duck season'
%run enc256.py
encrypt_passwd2(passwd)

%timeit encrypt_passwd(passwd)
%timeit encrypt_passwd2(passwd)
