<!DOCTYPE html>
<HTML LANG="en">
<HEAD>
<META http-equiv="content-type" content="text/html; charset=utf-8">
<META name="viewport" content="width=device-width, initial-scale=1.0">
<META name="robots" content="nofollow">
<LINK rel="stylesheet" type="text/css" href="/style/fresh.css" />
<link rel="stylesheet" type="text/css" href="/fresh/standard.css" />
<TITLE>IPython: IPython/core/magics/execution.py | Fossies</TITLE>
<META http-equiv="Content-Script-Type" content="text/javascript">
<script type="text/javascript" src="/scripts/highlight_styles.js"></script>
</HEAD>
<BODY>
<script type="text/javascript" src="/scripts/wz_tooltip.js"></script>
<script type="text/javascript" src="/scripts/tip_balloon.js"></script>
<H2><IMG SRC="/warix/forest1.gif" WIDTH="45" HEIGHT="29" ALT=""> "<A HREF="/">Fossies</A>" - the Fresh Open Source Software Archive <IMG SRC="/warix/forest2.gif" WIDTH="48" HEIGHT="30" ALT=""></H2>
<H3>Member "ipython-8.17.2/IPython/core/magics/execution.py" (27 Oct 2023, 60894 Bytes) of package <A HREF="/" TITLE="Fossies homepage">/</A><A HREF="/linux/" TITLE="Listing of all main folders within the Fossies basic folder /linux/">linux</A>/<A HREF="/linux/misc/" TITLE="Listing of all packages within the Fossies folder /linux/misc/">misc</A>/<A HREF="/linux/misc/ipython-8.17.2.tar.gz/" TITLE="Contents listing, member browsing, download with different compression formats, Doxygen generated source code documentation &amp; more ...">ipython-8.17.2.tar.gz</A>:</H3>
<HR>
<DIV class="fresh_info">
As a special service "Fossies" has tried to format the requested source page into HTML format using (guessed) Python source code syntax highlighting (style: <A HREF="/select_hl_style_lang" style="text-decoration:underline;" onmouseover="Tip(hl_styles_lang, ABOVE, false, OFFSETX, 0, OFFSETY, 5, BALLOON, true, FOLLOWMOUSE, false, WIDTH, 730, DELAY, 0, FADEIN, 0, FADEOUT, 1000, DURATION, 20000, STICKY, 1, CLICKCLOSE, true)" onmouseout="UnTip()" TITLE="About highlight style types">standard</A>) with prefixed line numbers.
Alternatively you can here <A HREF="/linux/misc/ipython-8.17.2.tar.gz/ipython-8.17.2/IPython/core/magics/execution.py?m=t">view</A> or <A HREF="/linux/misc/ipython-8.17.2.tar.gz/ipython-8.17.2/IPython/core/magics/execution.py?m=b" onmouseover="Tip(hl_dl_tip, ABOVE, false, OFFSETX, 0, OFFSETY, -5, BALLOON, true, FOLLOWMOUSE, false, WIDTH, 400, DELAY, 0, FADEIN, 0, FADEOUT, 300, DURATION, 10000, STICKY, 1, CLICKCLOSE, true)" onmouseout="UnTip()" TITLE="By the way: A member file download can also be achieved by clicking within a package contents listing on the according byte size field">download</A> the uninterpreted source code file.
 For more information about "execution.py" see the <span class="fresh_info_amo"><A HREF="/dox/" TITLE="Fossies doxygen-generated source code documentation (main page)" REL="nofollow">Fossies "Dox"</A></span> <a href="/dox/ipython-8.17.2/execution_8py.html" TITLE="&quot;execution.py&quot;: Doxygen-generated file reference page with documentation of  classes, namespaces and functions.">file reference</a> documentation and the last <span class="fresh_info_amo"><A HREF="/diffs/" TITLE="Fossies source code differences reports (main page)" REL="nofollow">Fossies "Diffs"</A></span> side-by-side code changes report: <A HREF="/diffs/ipython/8.14.0_vs_8.15.0/IPython/core/magics/execution.py-diff.html" TITLE="&quot;execution.py&quot; file currently unchanged, last changes on Fossies in a previous release report." STYLE="white-space: nowrap;"><IMG SRC="/delta_answer_10.png" WIDTH="13" HEIGHT="13"> 8.14.0_vs_8.15.0</A>.
</DIV>
<HR>
<pre class="hl"><span id="l_1" class="hl fld"><span class="hl lin">    1 </span><span class="hl slc"># -*- coding: utf-8 -*-</span></span>
<span id="l_2" class="hl fld"><span class="hl lin">    2 </span><span class="hl sng">&quot;&quot;&quot;Implementation of execution-related magic functions.&quot;&quot;&quot;</span></span>
<span id="l_3" class="hl fld"><span class="hl lin">    3 </span></span>
<span id="l_4" class="hl fld"><span class="hl lin">    4 </span><span class="hl slc"># Copyright (c) IPython Development Team.</span></span>
<span id="l_5" class="hl fld"><span class="hl lin">    5 </span><span class="hl slc"># Distributed under the terms of the Modified BSD License.</span></span>
<span id="l_6" class="hl fld"><span class="hl lin">    6 </span></span>
<span id="l_7" class="hl fld"><span class="hl lin">    7 </span></span>
<span id="l_8" class="hl fld"><span class="hl lin">    8 </span><span class="hl kwa">import</span> ast</span>
<span id="l_9" class="hl fld"><span class="hl lin">    9 </span><span class="hl kwa">import</span> bdb</span>
<span id="l_10" class="hl fld"><span class="hl lin">   10 </span><span class="hl kwa">import</span> builtins <span class="hl kwa">as</span> builtin_mod</span>
<span id="l_11" class="hl fld"><span class="hl lin">   11 </span><span class="hl kwa">import</span> copy</span>
<span id="l_12" class="hl fld"><span class="hl lin">   12 </span><span class="hl kwa">import</span> cProfile <span class="hl kwa">as</span> profile</span>
<span id="l_13" class="hl fld"><span class="hl lin">   13 </span><span class="hl kwa">import</span> gc</span>
<span id="l_14" class="hl fld"><span class="hl lin">   14 </span><span class="hl kwa">import</span> itertools</span>
<span id="l_15" class="hl fld"><span class="hl lin">   15 </span><span class="hl kwa">import</span> math</span>
<span id="l_16" class="hl fld"><span class="hl lin">   16 </span><span class="hl kwa">import</span> os</span>
<span id="l_17" class="hl fld"><span class="hl lin">   17 </span><span class="hl kwa">import</span> pstats</span>
<span id="l_18" class="hl fld"><span class="hl lin">   18 </span><span class="hl kwa">import</span> re</span>
<span id="l_19" class="hl fld"><span class="hl lin">   19 </span><span class="hl kwa">import</span> shlex</span>
<span id="l_20" class="hl fld"><span class="hl lin">   20 </span><span class="hl kwa">import</span> sys</span>
<span id="l_21" class="hl fld"><span class="hl lin">   21 </span><span class="hl kwa">import</span> time</span>
<span id="l_22" class="hl fld"><span class="hl lin">   22 </span><span class="hl kwa">import</span> timeit</span>
<span id="l_23" class="hl fld"><span class="hl lin">   23 </span><span class="hl kwa">from</span> typing <span class="hl kwa">import</span> Dict<span class="hl opt">,</span> Any</span>
<span id="l_24" class="hl fld"><span class="hl lin">   24 </span><span class="hl kwa">from</span> ast <span class="hl kwa">import</span> <span class="hl opt">(</span></span>
<span id="l_25" class="hl fld"><span class="hl lin">   25 </span>    Assign<span class="hl opt">,</span></span>
<span id="l_26" class="hl fld"><span class="hl lin">   26 </span>    Call<span class="hl opt">,</span></span>
<span id="l_27" class="hl fld"><span class="hl lin">   27 </span>    Expr<span class="hl opt">,</span></span>
<span id="l_28" class="hl fld"><span class="hl lin">   28 </span>    Load<span class="hl opt">,</span></span>
<span id="l_29" class="hl fld"><span class="hl lin">   29 </span>    Module<span class="hl opt">,</span></span>
<span id="l_30" class="hl fld"><span class="hl lin">   30 </span>    Name<span class="hl opt">,</span></span>
<span id="l_31" class="hl fld"><span class="hl lin">   31 </span>    NodeTransformer<span class="hl opt">,</span></span>
<span id="l_32" class="hl fld"><span class="hl lin">   32 </span>    Store<span class="hl opt">,</span></span>
<span id="l_33" class="hl fld"><span class="hl lin">   33 </span>    parse<span class="hl opt">,</span></span>
<span id="l_34" class="hl fld"><span class="hl lin">   34 </span>    unparse<span class="hl opt">,</span></span>
<span id="l_35" class="hl fld"><span class="hl lin">   35 </span><span class="hl opt">)</span></span>
<span id="l_36" class="hl fld"><span class="hl lin">   36 </span><span class="hl kwa">from</span> io <span class="hl kwa">import</span> StringIO</span>
<span id="l_37" class="hl fld"><span class="hl lin">   37 </span><span class="hl kwa">from</span> logging <span class="hl kwa">import</span> error</span>
<span id="l_38" class="hl fld"><span class="hl lin">   38 </span><span class="hl kwa">from</span> pathlib <span class="hl kwa">import</span> Path</span>
<span id="l_39" class="hl fld"><span class="hl lin">   39 </span><span class="hl kwa">from</span> pdb <span class="hl kwa">import</span> Restart</span>
<span id="l_40" class="hl fld"><span class="hl lin">   40 </span><span class="hl kwa">from</span> textwrap <span class="hl kwa">import</span> dedent<span class="hl opt">,</span> indent</span>
<span id="l_41" class="hl fld"><span class="hl lin">   41 </span><span class="hl kwa">from</span> warnings <span class="hl kwa">import</span> warn</span>
<span id="l_42" class="hl fld"><span class="hl lin">   42 </span></span>
<span id="l_43" class="hl fld"><span class="hl lin">   43 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>core <span class="hl kwa">import</span> magic_arguments<span class="hl opt">,</span> oinspect<span class="hl opt">,</span> page</span>
<span id="l_44" class="hl fld"><span class="hl lin">   44 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>core<span class="hl opt">.</span>displayhook <span class="hl kwa">import</span> DisplayHook</span>
<span id="l_45" class="hl fld"><span class="hl lin">   45 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>core<span class="hl opt">.</span>error <span class="hl kwa">import</span> UsageError</span>
<span id="l_46" class="hl fld"><span class="hl lin">   46 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>core<span class="hl opt">.</span>macro <span class="hl kwa">import</span> Macro</span>
<span id="l_47" class="hl fld"><span class="hl lin">   47 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>core<span class="hl opt">.</span>magic <span class="hl kwa">import</span> <span class="hl opt">(</span></span>
<span id="l_48" class="hl fld"><span class="hl lin">   48 </span>    Magics<span class="hl opt">,</span></span>
<span id="l_49" class="hl fld"><span class="hl lin">   49 </span>    cell_magic<span class="hl opt">,</span></span>
<span id="l_50" class="hl fld"><span class="hl lin">   50 </span>    line_cell_magic<span class="hl opt">,</span></span>
<span id="l_51" class="hl fld"><span class="hl lin">   51 </span>    line_magic<span class="hl opt">,</span></span>
<span id="l_52" class="hl fld"><span class="hl lin">   52 </span>    magics_class<span class="hl opt">,</span></span>
<span id="l_53" class="hl fld"><span class="hl lin">   53 </span>    needs_local_scope<span class="hl opt">,</span></span>
<span id="l_54" class="hl fld"><span class="hl lin">   54 </span>    no_var_expand<span class="hl opt">,</span></span>
<span id="l_55" class="hl fld"><span class="hl lin">   55 </span>    on_off<span class="hl opt">,</span></span>
<span id="l_56" class="hl fld"><span class="hl lin">   56 </span>    output_can_be_silenced<span class="hl opt">,</span></span>
<span id="l_57" class="hl fld"><span class="hl lin">   57 </span><span class="hl opt">)</span></span>
<span id="l_58" class="hl fld"><span class="hl lin">   58 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>testing<span class="hl opt">.</span>skipdoctest <span class="hl kwa">import</span> skip_doctest</span>
<span id="l_59" class="hl fld"><span class="hl lin">   59 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>utils<span class="hl opt">.</span>capture <span class="hl kwa">import</span> capture_output</span>
<span id="l_60" class="hl fld"><span class="hl lin">   60 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>utils<span class="hl opt">.</span>contexts <span class="hl kwa">import</span> preserve_keys</span>
<span id="l_61" class="hl fld"><span class="hl lin">   61 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>utils<span class="hl opt">.</span>ipstruct <span class="hl kwa">import</span> Struct</span>
<span id="l_62" class="hl fld"><span class="hl lin">   62 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>utils<span class="hl opt">.</span>module_paths <span class="hl kwa">import</span> find_mod</span>
<span id="l_63" class="hl fld"><span class="hl lin">   63 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>utils<span class="hl opt">.</span>path <span class="hl kwa">import</span> get_py_filename<span class="hl opt">,</span> shellglob</span>
<span id="l_64" class="hl fld"><span class="hl lin">   64 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>utils<span class="hl opt">.</span>timing <span class="hl kwa">import</span> clock<span class="hl opt">,</span> clock2</span>
<span id="l_65" class="hl fld"><span class="hl lin">   65 </span><span class="hl kwa">from</span> IPython<span class="hl opt">.</span>core<span class="hl opt">.</span>magics<span class="hl opt">.</span>ast_mod <span class="hl kwa">import</span> ReplaceCodeTransformer</span>
<span id="l_66" class="hl fld"><span class="hl lin">   66 </span></span>
<span id="l_67" class="hl fld"><span class="hl lin">   67 </span><span class="hl slc">#-----------------------------------------------------------------------------</span></span>
<span id="l_68" class="hl fld"><span class="hl lin">   68 </span><span class="hl slc"># Magic implementation classes</span></span>
<span id="l_69" class="hl fld"><span class="hl lin">   69 </span><span class="hl slc">#-----------------------------------------------------------------------------</span></span>
<span id="l_70" class="hl fld"><span class="hl lin">   70 </span></span>
<span id="l_71" class="hl fld"><span class="hl lin">   71 </span></span>
<span id="l_72" class="hl fld"><span class="hl lin">   72 </span><span class="hl kwa">class</span> <span class="hl kwd">TimeitResult</span><span class="hl opt">(</span><span class="hl kwb">object</span><span class="hl opt">):</span></span>
<span id="l_73" class="hl fld"><span class="hl lin">   73 </span>    <span class="hl sng">&quot;&quot;&quot;</span></span>
<span id="l_74" class="hl fld"><span class="hl lin">   74 </span><span class="hl sng">    Object returned by the timeit magic with info about the run.</span></span>
<span id="l_75" class="hl fld"><span class="hl lin">   75 </span><span class="hl sng"></span></span>
<span id="l_76" class="hl fld"><span class="hl lin">   76 </span><span class="hl sng">    Contains the following attributes :</span></span>
<span id="l_77" class="hl fld"><span class="hl lin">   77 </span><span class="hl sng"></span></span>
<span id="l_78" class="hl fld"><span class="hl lin">   78 </span><span class="hl sng">    loops: (int) number of loops done per measurement</span></span>
<span id="l_79" class="hl fld"><span class="hl lin">   79 </span><span class="hl sng">    repeat: (int) number of times the measurement has been repeated</span></span>
<span id="l_80" class="hl fld"><span class="hl lin">   80 </span><span class="hl sng">    best: (float) best execution time / number</span></span>
<span id="l_81" class="hl fld"><span class="hl lin">   81 </span><span class="hl sng">    all_runs: (list of float) execution time of each run (in s)</span></span>
<span id="l_82" class="hl fld"><span class="hl lin">   82 </span><span class="hl sng">    compile_time: (float) time of statement compilation (s)</span></span>
<span id="l_83" class="hl fld"><span class="hl lin">   83 </span><span class="hl sng"></span></span>
<span id="l_84" class="hl fld"><span class="hl lin">   84 </span><span class="hl sng">    &quot;&quot;&quot;</span></span>
<span id="l_85" class="hl fld"><span class="hl lin">   85 </span>    <span class="hl kwa">def</span> <span class="hl kwd">__init__</span><span class="hl opt">(</span>self<span class="hl opt">,</span> loops<span class="hl opt">,</span> repeat<span class="hl opt">,</span> best<span class="hl opt">,</span> worst<span class="hl opt">,</span> all_runs<span class="hl opt">,</span> compile_time<span class="hl opt">,</span> precision<span class="hl opt">):</span></span>
<span id="l_86" class="hl fld"><span class="hl lin">   86 </span>        self<span class="hl opt">.</span>loops <span class="hl opt">=</span> loops</span>
<span id="l_87" class="hl fld"><span class="hl lin">   87 </span>        self<span class="hl opt">.</span>repeat <span class="hl opt">=</span> repeat</span>
<span id="l_88" class="hl fld"><span class="hl lin">   88 </span>        self<span class="hl opt">.</span>best <span class="hl opt">=</span> best</span>
<span id="l_89" class="hl fld"><span class="hl lin">   89 </span>        self<span class="hl opt">.</span>worst <span class="hl opt">=</span> worst</span>
<span id="l_90" class="hl fld"><span class="hl lin">   90 </span>        self<span class="hl opt">.</span>all_runs <span class="hl opt">=</span> all_runs</span>
<span id="l_91" class="hl fld"><span class="hl lin">   91 </span>        self<span class="hl opt">.</span>compile_time <span class="hl opt">=</span> compile_time</span>
<span id="l_92" class="hl fld"><span class="hl lin">   92 </span>        self<span class="hl num">._</span>precision <span class="hl opt">=</span> precision</span>
<span id="l_93" class="hl fld"><span class="hl lin">   93 </span>        self<span class="hl opt">.</span>timings <span class="hl opt">= [</span> dt <span class="hl opt">/</span> self<span class="hl opt">.</span>loops <span class="hl kwa">for</span> dt <span class="hl kwa">in</span> all_runs<span class="hl opt">]</span></span>
<span id="l_94" class="hl fld"><span class="hl lin">   94 </span></span>
<span id="l_95" class="hl fld"><span class="hl lin">   95 </span>    <span class="hl kwb">&#64;property</span></span>
<span id="l_96" class="hl fld"><span class="hl lin">   96 </span>    <span class="hl kwa">def</span> <span class="hl kwd">average</span><span class="hl opt">(</span>self<span class="hl opt">):</span></span>
<span id="l_97" class="hl fld"><span class="hl lin">   97 </span>        <span class="hl kwa">return</span> math<span class="hl opt">.</span><span class="hl kwd">fsum</span><span class="hl opt">(</span>self<span class="hl opt">.</span>timings<span class="hl opt">) /</span> <span class="hl kwb">len</span><span class="hl opt">(</span>self<span class="hl opt">.</span>timings<span class="hl opt">)</span></span>
<span id="l_98" class="hl fld"><span class="hl lin">   98 </span></span>
<span id="l_99" class="hl fld"><span class="hl lin">   99 </span>    <span class="hl kwb">&#64;property</span></span>
<span id="l_100" class="hl fld"><span class="hl lin">  100 </span>    <span class="hl kwa">def</span> <span class="hl kwd">stdev</span><span class="hl opt">(</span>self<span class="hl opt">):</span></span>
<span id="l_101" class="hl fld"><span class="hl lin">  101 </span>        mean <span class="hl opt">=</span> self<span class="hl opt">.</span>average</span>
<span id="l_102" class="hl fld"><span class="hl lin">  102 </span>        <span class="hl kwa">return</span> <span class="hl opt">(</span>math<span class="hl opt">.</span><span class="hl kwd">fsum</span><span class="hl opt">([(</span>x <span class="hl opt">-</span> mean<span class="hl opt">) **</span> <span class="hl num">2</span> <span class="hl kwa">for</span> x <span class="hl kwa">in</span> self<span class="hl opt">.</span>timings<span class="hl opt">]) /</span> <span class="hl kwb">len</span><span class="hl opt">(</span>self<span class="hl opt">.</span>timings<span class="hl opt">)) **</span> <span class="hl num">0.5</span></span>
<span id="l_103" class="hl fld"><span class="hl lin">  103 </span></span>
<span id="l_104" class="hl fld"><span class="hl lin">  104 </span>    <span class="hl kwa">def</span> <span class="hl kwd">__str__</span><span class="hl opt">(</span>self<span class="hl opt">):</span></span>
<span id="l_105" class="hl fld"><span class="hl lin">  105 </span>        pm <span class="hl opt">=</span> <span class="hl sng">&#39;+-&#39;</span></span>
<span id="l_106" class="hl fld"><span class="hl lin">  106 </span>        <span class="hl kwa">if</span> <span class="hl kwb">hasattr</span><span class="hl opt">(</span>sys<span class="hl opt">.</span>stdout<span class="hl opt">,</span> <span class="hl sng">&#39;encoding&#39;</span><span class="hl opt">)</span> <span class="hl kwa">and</span> sys<span class="hl opt">.</span>stdout<span class="hl opt">.</span>encoding<span class="hl opt">:</span></span>
<span id="l_107" class="hl fld"><span class="hl lin">  107 </span>            <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_108" class="hl fld"><span class="hl lin">  108 </span>                u<span class="hl sng">&#39;</span><span class="hl esc">\xb1</span><span class="hl sng">&#39;</span><span class="hl opt">.</span><span class="hl kwd">encode</span><span class="hl opt">(</span>sys<span class="hl opt">.</span>stdout<span class="hl opt">.</span>encoding<span class="hl opt">)</span></span>
<span id="l_109" class="hl fld"><span class="hl lin">  109 </span>                pm <span class="hl opt">=</span> u<span class="hl sng">&#39;</span><span class="hl esc">\xb1</span><span class="hl sng">&#39;</span></span>
<span id="l_110" class="hl fld"><span class="hl lin">  110 </span>            <span class="hl kwa">except</span><span class="hl opt">:</span></span>
<span id="l_111" class="hl fld"><span class="hl lin">  111 </span>                <span class="hl kwa">pass</span></span>
<span id="l_112" class="hl fld"><span class="hl lin">  112 </span>        <span class="hl kwa">return</span> <span class="hl sng">&quot;</span><span class="hl ipl">{mean} {pm} {std}</span> <span class="hl sng">per loop (mean</span> <span class="hl ipl">{pm}</span> <span class="hl sng">std. dev. of</span> <span class="hl ipl">{runs}</span> <span class="hl sng">run</span><span class="hl ipl">{run_plural}</span><span class="hl sng">,</span> <span class="hl ipl">{loops:,}</span> <span class="hl sng">loop</span><span class="hl ipl">{loop_plural}</span> <span class="hl sng">each)&quot;</span><span class="hl opt">.</span><span class="hl kwd">format</span><span class="hl opt">(</span></span>
<span id="l_113" class="hl fld"><span class="hl lin">  113 </span>            pm<span class="hl opt">=</span>pm<span class="hl opt">,</span></span>
<span id="l_114" class="hl fld"><span class="hl lin">  114 </span>            runs<span class="hl opt">=</span>self<span class="hl opt">.</span>repeat<span class="hl opt">,</span></span>
<span id="l_115" class="hl fld"><span class="hl lin">  115 </span>            loops<span class="hl opt">=</span>self<span class="hl opt">.</span>loops<span class="hl opt">,</span></span>
<span id="l_116" class="hl fld"><span class="hl lin">  116 </span>            loop_plural<span class="hl opt">=</span><span class="hl sng">&quot;&quot;</span> <span class="hl kwa">if</span> self<span class="hl opt">.</span>loops <span class="hl opt">==</span> <span class="hl num">1</span> <span class="hl kwa">else</span> <span class="hl sng">&quot;s&quot;</span><span class="hl opt">,</span></span>
<span id="l_117" class="hl fld"><span class="hl lin">  117 </span>            run_plural<span class="hl opt">=</span><span class="hl sng">&quot;&quot;</span> <span class="hl kwa">if</span> self<span class="hl opt">.</span>repeat <span class="hl opt">==</span> <span class="hl num">1</span> <span class="hl kwa">else</span> <span class="hl sng">&quot;s&quot;</span><span class="hl opt">,</span></span>
<span id="l_118" class="hl fld"><span class="hl lin">  118 </span>            mean<span class="hl opt">=</span><span class="hl kwd">_format_time</span><span class="hl opt">(</span>self<span class="hl opt">.</span>average<span class="hl opt">,</span> self<span class="hl num">._</span>precision<span class="hl opt">),</span></span>
<span id="l_119" class="hl fld"><span class="hl lin">  119 </span>            std<span class="hl opt">=</span><span class="hl kwd">_format_time</span><span class="hl opt">(</span>self<span class="hl opt">.</span>stdev<span class="hl opt">,</span> self<span class="hl num">._</span>precision<span class="hl opt">),</span></span>
<span id="l_120" class="hl fld"><span class="hl lin">  120 </span>        <span class="hl opt">)</span></span>
<span id="l_121" class="hl fld"><span class="hl lin">  121 </span></span>
<span id="l_122" class="hl fld"><span class="hl lin">  122 </span>    <span class="hl kwa">def</span> <span class="hl kwd">_repr_pretty_</span><span class="hl opt">(</span>self<span class="hl opt">,</span> p <span class="hl opt">,</span> cycle<span class="hl opt">):</span></span>
<span id="l_123" class="hl fld"><span class="hl lin">  123 </span>        unic <span class="hl opt">=</span> self<span class="hl num">.__</span>str<span class="hl num">__</span><span class="hl opt">()</span></span>
<span id="l_124" class="hl fld"><span class="hl lin">  124 </span>        p<span class="hl opt">.</span><span class="hl kwd">text</span><span class="hl opt">(</span>u<span class="hl sng">&#39;&lt;TimeitResult : &#39;</span><span class="hl opt">+</span>unic<span class="hl opt">+</span>u<span class="hl sng">&#39;&gt;&#39;</span><span class="hl opt">)</span></span>
<span id="l_125" class="hl fld"><span class="hl lin">  125 </span></span>
<span id="l_126" class="hl fld"><span class="hl lin">  126 </span></span>
<span id="l_127" class="hl fld"><span class="hl lin">  127 </span><span class="hl kwa">class</span> <span class="hl kwd">TimeitTemplateFiller</span><span class="hl opt">(</span>ast<span class="hl opt">.</span>NodeTransformer<span class="hl opt">):</span></span>
<span id="l_128" class="hl fld"><span class="hl lin">  128 </span>    <span class="hl sng">&quot;&quot;&quot;Fill in the AST template for timing execution.</span></span>
<span id="l_129" class="hl fld"><span class="hl lin">  129 </span><span class="hl sng"></span></span>
<span id="l_130" class="hl fld"><span class="hl lin">  130 </span><span class="hl sng">    This is quite closely tied to the template definition, which is in</span></span>
<span id="l_131" class="hl fld"><span class="hl lin">  131 </span><span class="hl sng">    :meth:`ExecutionMagics.timeit`.</span></span>
<span id="l_132" class="hl fld"><span class="hl lin">  132 </span><span class="hl sng">    &quot;&quot;&quot;</span></span>
<span id="l_133" class="hl fld"><span class="hl lin">  133 </span>    <span class="hl kwa">def</span> <span class="hl kwd">__init__</span><span class="hl opt">(</span>self<span class="hl opt">,</span> ast_setup<span class="hl opt">,</span> ast_stmt<span class="hl opt">):</span></span>
<span id="l_134" class="hl fld"><span class="hl lin">  134 </span>        self<span class="hl opt">.</span>ast_setup <span class="hl opt">=</span> ast_setup</span>
<span id="l_135" class="hl fld"><span class="hl lin">  135 </span>        self<span class="hl opt">.</span>ast_stmt <span class="hl opt">=</span> ast_stmt</span>
<span id="l_136" class="hl fld"><span class="hl lin">  136 </span></span>
<span id="l_137" class="hl fld"><span class="hl lin">  137 </span>    <span class="hl kwa">def</span> <span class="hl kwd">visit_FunctionDef</span><span class="hl opt">(</span>self<span class="hl opt">,</span> node<span class="hl opt">):</span></span>
<span id="l_138" class="hl fld"><span class="hl lin">  138 </span>        <span class="hl sng">&quot;Fill in the setup statement&quot;</span></span>
<span id="l_139" class="hl fld"><span class="hl lin">  139 </span>        self<span class="hl opt">.</span><span class="hl kwd">generic_visit</span><span class="hl opt">(</span>node<span class="hl opt">)</span></span>
<span id="l_140" class="hl fld"><span class="hl lin">  140 </span>        <span class="hl kwa">if</span> node<span class="hl opt">.</span>name <span class="hl opt">==</span> <span class="hl sng">&quot;inner&quot;</span><span class="hl opt">:</span></span>
<span id="l_141" class="hl fld"><span class="hl lin">  141 </span>            node<span class="hl opt">.</span>body<span class="hl opt">[:</span><span class="hl num">1</span><span class="hl opt">] =</span> self<span class="hl opt">.</span>ast_setup<span class="hl opt">.</span>body</span>
<span id="l_142" class="hl fld"><span class="hl lin">  142 </span></span>
<span id="l_143" class="hl fld"><span class="hl lin">  143 </span>        <span class="hl kwa">return</span> node</span>
<span id="l_144" class="hl fld"><span class="hl lin">  144 </span></span>
<span id="l_145" class="hl fld"><span class="hl lin">  145 </span>    <span class="hl kwa">def</span> <span class="hl kwd">visit_For</span><span class="hl opt">(</span>self<span class="hl opt">,</span> node<span class="hl opt">):</span></span>
<span id="l_146" class="hl fld"><span class="hl lin">  146 </span>        <span class="hl sng">&quot;Fill in the statement to be timed&quot;</span></span>
<span id="l_147" class="hl fld"><span class="hl lin">  147 </span>        <span class="hl kwa">if</span> <span class="hl kwb">getattr</span><span class="hl opt">(</span><span class="hl kwb">getattr</span><span class="hl opt">(</span>node<span class="hl opt">.</span>body<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">],</span> <span class="hl sng">&#39;value&#39;</span><span class="hl opt">,</span> <span class="hl kwa">None</span><span class="hl opt">),</span> <span class="hl sng">&#39;id&#39;</span><span class="hl opt">,</span> <span class="hl kwa">None</span><span class="hl opt">) ==</span> <span class="hl sng">&#39;stmt&#39;</span><span class="hl opt">:</span></span>
<span id="l_148" class="hl fld"><span class="hl lin">  148 </span>            node<span class="hl opt">.</span>body <span class="hl opt">=</span> self<span class="hl opt">.</span>ast_stmt<span class="hl opt">.</span>body</span>
<span id="l_149" class="hl fld"><span class="hl lin">  149 </span>        <span class="hl kwa">return</span> node</span>
<span id="l_150" class="hl fld"><span class="hl lin">  150 </span></span>
<span id="l_151" class="hl fld"><span class="hl lin">  151 </span></span>
<span id="l_152" class="hl fld"><span class="hl lin">  152 </span><span class="hl kwa">class</span> <span class="hl kwd">Timer</span><span class="hl opt">(</span>timeit<span class="hl opt">.</span>Timer<span class="hl opt">):</span></span>
<span id="l_153" class="hl fld"><span class="hl lin">  153 </span>    <span class="hl sng">&quot;&quot;&quot;Timer class that explicitly uses self.inner</span></span>
<span id="l_154" class="hl fld"><span class="hl lin">  154 </span><span class="hl sng">    </span></span>
<span id="l_155" class="hl fld"><span class="hl lin">  155 </span><span class="hl sng">    which is an undocumented implementation detail of CPython,</span></span>
<span id="l_156" class="hl fld"><span class="hl lin">  156 </span><span class="hl sng">    not shared by PyPy.</span></span>
<span id="l_157" class="hl fld"><span class="hl lin">  157 </span><span class="hl sng">    &quot;&quot;&quot;</span></span>
<span id="l_158" class="hl fld"><span class="hl lin">  158 </span>    <span class="hl slc"># Timer.timeit copied from CPython 3.4.2</span></span>
<span id="l_159" class="hl fld"><span class="hl lin">  159 </span>    <span class="hl kwa">def</span> <span class="hl kwd">timeit</span><span class="hl opt">(</span>self<span class="hl opt">,</span> number<span class="hl opt">=</span>timeit<span class="hl opt">.</span>default_number<span class="hl opt">):</span></span>
<span id="l_160" class="hl fld"><span class="hl lin">  160 </span>        <span class="hl sng">&quot;&quot;&quot;Time &#39;number&#39; executions of the main statement.</span></span>
<span id="l_161" class="hl fld"><span class="hl lin">  161 </span><span class="hl sng"></span></span>
<span id="l_162" class="hl fld"><span class="hl lin">  162 </span><span class="hl sng">        To be precise, this executes the setup statement once, and</span></span>
<span id="l_163" class="hl fld"><span class="hl lin">  163 </span><span class="hl sng">        then returns the time it takes to execute the main statement</span></span>
<span id="l_164" class="hl fld"><span class="hl lin">  164 </span><span class="hl sng">        a number of times, as a float measured in seconds.  The</span></span>
<span id="l_165" class="hl fld"><span class="hl lin">  165 </span><span class="hl sng">        argument is the number of times through the loop, defaulting</span></span>
<span id="l_166" class="hl fld"><span class="hl lin">  166 </span><span class="hl sng">        to one million.  The main statement, the setup statement and</span></span>
<span id="l_167" class="hl fld"><span class="hl lin">  167 </span><span class="hl sng">        the timer function to be used are passed to the constructor.</span></span>
<span id="l_168" class="hl fld"><span class="hl lin">  168 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_169" class="hl fld"><span class="hl lin">  169 </span>        it <span class="hl opt">=</span> itertools<span class="hl opt">.</span><span class="hl kwd">repeat</span><span class="hl opt">(</span><span class="hl kwa">None</span><span class="hl opt">,</span> number<span class="hl opt">)</span></span>
<span id="l_170" class="hl fld"><span class="hl lin">  170 </span>        gcold <span class="hl opt">=</span> gc<span class="hl opt">.</span><span class="hl kwd">isenabled</span><span class="hl opt">()</span></span>
<span id="l_171" class="hl fld"><span class="hl lin">  171 </span>        gc<span class="hl opt">.</span><span class="hl kwd">disable</span><span class="hl opt">()</span></span>
<span id="l_172" class="hl fld"><span class="hl lin">  172 </span>        <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_173" class="hl fld"><span class="hl lin">  173 </span>            timing <span class="hl opt">=</span> self<span class="hl opt">.</span><span class="hl kwd">inner</span><span class="hl opt">(</span>it<span class="hl opt">,</span> self<span class="hl opt">.</span>timer<span class="hl opt">)</span></span>
<span id="l_174" class="hl fld"><span class="hl lin">  174 </span>        <span class="hl kwa">finally</span><span class="hl opt">:</span></span>
<span id="l_175" class="hl fld"><span class="hl lin">  175 </span>            <span class="hl kwa">if</span> gcold<span class="hl opt">:</span></span>
<span id="l_176" class="hl fld"><span class="hl lin">  176 </span>                gc<span class="hl opt">.</span><span class="hl kwd">enable</span><span class="hl opt">()</span></span>
<span id="l_177" class="hl fld"><span class="hl lin">  177 </span>        <span class="hl kwa">return</span> timing</span>
<span id="l_178" class="hl fld"><span class="hl lin">  178 </span></span>
<span id="l_179" class="hl fld"><span class="hl lin">  179 </span></span>
<span id="l_180" class="hl fld"><span class="hl lin">  180 </span><span class="hl kwb">&#64;magics_class</span></span>
<span id="l_181" class="hl fld"><span class="hl lin">  181 </span><span class="hl kwa">class</span> <span class="hl kwd">ExecutionMagics</span><span class="hl opt">(</span>Magics<span class="hl opt">):</span></span>
<span id="l_182" class="hl fld"><span class="hl lin">  182 </span>    <span class="hl sng">&quot;&quot;&quot;Magics related to code execution, debugging, profiling, etc.&quot;&quot;&quot;</span></span>
<span id="l_183" class="hl fld"><span class="hl lin">  183 </span></span>
<span id="l_184" class="hl fld"><span class="hl lin">  184 </span>    _transformers<span class="hl opt">:</span> Dict<span class="hl opt">[</span><span class="hl kwb">str</span><span class="hl opt">,</span> Any<span class="hl opt">] = {}</span></span>
<span id="l_185" class="hl fld"><span class="hl lin">  185 </span></span>
<span id="l_186" class="hl fld"><span class="hl lin">  186 </span>    <span class="hl kwa">def</span> <span class="hl kwd">__init__</span><span class="hl opt">(</span>self<span class="hl opt">,</span> shell<span class="hl opt">):</span></span>
<span id="l_187" class="hl fld"><span class="hl lin">  187 </span>        <span class="hl kwb">super</span><span class="hl opt">(</span>ExecutionMagics<span class="hl opt">,</span> self<span class="hl opt">)</span><span class="hl num">.__</span>init<span class="hl num">__</span><span class="hl opt">(</span>shell<span class="hl opt">)</span></span>
<span id="l_188" class="hl fld"><span class="hl lin">  188 </span>        <span class="hl slc"># Default execution function used to actually run user code.</span></span>
<span id="l_189" class="hl fld"><span class="hl lin">  189 </span>        self<span class="hl opt">.</span>default_runner <span class="hl opt">=</span> <span class="hl kwa">None</span></span>
<span id="l_190" class="hl fld"><span class="hl lin">  190 </span></span>
<span id="l_191" class="hl fld"><span class="hl lin">  191 </span>    <span class="hl kwb">&#64;skip_doctest</span></span>
<span id="l_192" class="hl fld"><span class="hl lin">  192 </span>    <span class="hl kwb">&#64;no_var_expand</span></span>
<span id="l_193" class="hl fld"><span class="hl lin">  193 </span>    <span class="hl kwb">&#64;line_cell_magic</span></span>
<span id="l_194" class="hl fld"><span class="hl lin">  194 </span>    <span class="hl kwa">def</span> <span class="hl kwd">prun</span><span class="hl opt">(</span>self<span class="hl opt">,</span> parameter_s<span class="hl opt">=</span><span class="hl sng">&#39;&#39;</span><span class="hl opt">,</span> cell<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">):</span></span>
<span id="l_195" class="hl fld"><span class="hl lin">  195 </span></span>
<span id="l_196" class="hl fld"><span class="hl lin">  196 </span>        <span class="hl sng">&quot;&quot;&quot;Run a statement through the python code profiler.</span></span>
<span id="l_197" class="hl fld"><span class="hl lin">  197 </span><span class="hl sng"></span></span>
<span id="l_198" class="hl fld"><span class="hl lin">  198 </span><span class="hl sng">        Usage, in line mode:</span></span>
<span id="l_199" class="hl fld"><span class="hl lin">  199 </span><span class="hl sng">          %prun [options] statement</span></span>
<span id="l_200" class="hl fld"><span class="hl lin">  200 </span><span class="hl sng"></span></span>
<span id="l_201" class="hl fld"><span class="hl lin">  201 </span><span class="hl sng">        Usage, in cell mode:</span></span>
<span id="l_202" class="hl fld"><span class="hl lin">  202 </span><span class="hl sng"></span>          <span class="hl ipl">%%</span><span class="hl sng">prun [options] [statement]</span></span>
<span id="l_203" class="hl fld"><span class="hl lin">  203 </span><span class="hl sng">          code...</span></span>
<span id="l_204" class="hl fld"><span class="hl lin">  204 </span><span class="hl sng">          code...</span></span>
<span id="l_205" class="hl fld"><span class="hl lin">  205 </span><span class="hl sng"></span></span>
<span id="l_206" class="hl fld"><span class="hl lin">  206 </span><span class="hl sng">        In cell mode, the additional code lines are appended to the (possibly</span></span>
<span id="l_207" class="hl fld"><span class="hl lin">  207 </span><span class="hl sng">        empty) statement in the first line.  Cell mode allows you to easily</span></span>
<span id="l_208" class="hl fld"><span class="hl lin">  208 </span><span class="hl sng">        profile multiline blocks without having to put them in a separate</span></span>
<span id="l_209" class="hl fld"><span class="hl lin">  209 </span><span class="hl sng">        function.</span></span>
<span id="l_210" class="hl fld"><span class="hl lin">  210 </span><span class="hl sng"></span></span>
<span id="l_211" class="hl fld"><span class="hl lin">  211 </span><span class="hl sng">        The given statement (which doesn&#39;t require quote marks) is run via the</span></span>
<span id="l_212" class="hl fld"><span class="hl lin">  212 </span><span class="hl sng">        python profiler in a manner similar to the profile.run() function.</span></span>
<span id="l_213" class="hl fld"><span class="hl lin">  213 </span><span class="hl sng">        Namespaces are internally managed to work correctly; profile.run</span></span>
<span id="l_214" class="hl fld"><span class="hl lin">  214 </span><span class="hl sng">        cannot be used in IPython because it makes certain assumptions about</span></span>
<span id="l_215" class="hl fld"><span class="hl lin">  215 </span><span class="hl sng">        namespaces which do not hold under IPython.</span></span>
<span id="l_216" class="hl fld"><span class="hl lin">  216 </span><span class="hl sng"></span></span>
<span id="l_217" class="hl fld"><span class="hl lin">  217 </span><span class="hl sng">        Options:</span></span>
<span id="l_218" class="hl fld"><span class="hl lin">  218 </span><span class="hl sng"></span></span>
<span id="l_219" class="hl fld"><span class="hl lin">  219 </span><span class="hl sng">        -l &lt;limit&gt;</span></span>
<span id="l_220" class="hl fld"><span class="hl lin">  220 </span><span class="hl sng">          you can place restrictions on what or how much of the</span></span>
<span id="l_221" class="hl fld"><span class="hl lin">  221 </span><span class="hl sng">          profile gets printed. The limit value can be:</span></span>
<span id="l_222" class="hl fld"><span class="hl lin">  222 </span><span class="hl sng"></span></span>
<span id="l_223" class="hl fld"><span class="hl lin">  223 </span><span class="hl sng">             * A string: only information for function names containing this string</span></span>
<span id="l_224" class="hl fld"><span class="hl lin">  224 </span><span class="hl sng">               is printed.</span></span>
<span id="l_225" class="hl fld"><span class="hl lin">  225 </span><span class="hl sng"></span></span>
<span id="l_226" class="hl fld"><span class="hl lin">  226 </span><span class="hl sng">             * An integer: only these many lines are printed.</span></span>
<span id="l_227" class="hl fld"><span class="hl lin">  227 </span><span class="hl sng"></span></span>
<span id="l_228" class="hl fld"><span class="hl lin">  228 </span><span class="hl sng">             * A float (between 0 and 1): this fraction of the report is printed</span></span>
<span id="l_229" class="hl fld"><span class="hl lin">  229 </span><span class="hl sng">               (for example, use a limit of 0.4 to see the topmost 40% only).</span></span>
<span id="l_230" class="hl fld"><span class="hl lin">  230 </span><span class="hl sng"></span></span>
<span id="l_231" class="hl fld"><span class="hl lin">  231 </span><span class="hl sng">          You can combine several limits with repeated use of the option. For</span></span>
<span id="l_232" class="hl fld"><span class="hl lin">  232 </span><span class="hl sng">          example, ``-l __init__ -l 5`` will print only the topmost 5 lines of</span></span>
<span id="l_233" class="hl fld"><span class="hl lin">  233 </span><span class="hl sng">          information about class constructors.</span></span>
<span id="l_234" class="hl fld"><span class="hl lin">  234 </span><span class="hl sng"></span></span>
<span id="l_235" class="hl fld"><span class="hl lin">  235 </span><span class="hl sng">        -r</span></span>
<span id="l_236" class="hl fld"><span class="hl lin">  236 </span><span class="hl sng">          return the pstats.Stats object generated by the profiling. This</span></span>
<span id="l_237" class="hl fld"><span class="hl lin">  237 </span><span class="hl sng">          object has all the information about the profile in it, and you can</span></span>
<span id="l_238" class="hl fld"><span class="hl lin">  238 </span><span class="hl sng">          later use it for further analysis or in other functions.</span></span>
<span id="l_239" class="hl fld"><span class="hl lin">  239 </span><span class="hl sng"></span></span>
<span id="l_240" class="hl fld"><span class="hl lin">  240 </span><span class="hl sng">        -s &lt;key&gt;</span></span>
<span id="l_241" class="hl fld"><span class="hl lin">  241 </span><span class="hl sng">          sort profile by given key. You can provide more than one key</span></span>
<span id="l_242" class="hl fld"><span class="hl lin">  242 </span><span class="hl sng">          by using the option several times: &#39;-s key1 -s key2 -s key3...&#39;. The</span></span>
<span id="l_243" class="hl fld"><span class="hl lin">  243 </span><span class="hl sng">          default sorting key is &#39;time&#39;.</span></span>
<span id="l_244" class="hl fld"><span class="hl lin">  244 </span><span class="hl sng"></span></span>
<span id="l_245" class="hl fld"><span class="hl lin">  245 </span><span class="hl sng">          The following is copied verbatim from the profile documentation</span></span>
<span id="l_246" class="hl fld"><span class="hl lin">  246 </span><span class="hl sng">          referenced below:</span></span>
<span id="l_247" class="hl fld"><span class="hl lin">  247 </span><span class="hl sng"></span></span>
<span id="l_248" class="hl fld"><span class="hl lin">  248 </span><span class="hl sng">          When more than one key is provided, additional keys are used as</span></span>
<span id="l_249" class="hl fld"><span class="hl lin">  249 </span><span class="hl sng">          secondary criteria when the there is equality in all keys selected</span></span>
<span id="l_250" class="hl fld"><span class="hl lin">  250 </span><span class="hl sng">          before them.</span></span>
<span id="l_251" class="hl fld"><span class="hl lin">  251 </span><span class="hl sng"></span></span>
<span id="l_252" class="hl fld"><span class="hl lin">  252 </span><span class="hl sng">          Abbreviations can be used for any key names, as long as the</span></span>
<span id="l_253" class="hl fld"><span class="hl lin">  253 </span><span class="hl sng">          abbreviation is unambiguous.  The following are the keys currently</span></span>
<span id="l_254" class="hl fld"><span class="hl lin">  254 </span><span class="hl sng">          defined:</span></span>
<span id="l_255" class="hl fld"><span class="hl lin">  255 </span><span class="hl sng"></span></span>
<span id="l_256" class="hl fld"><span class="hl lin">  256 </span><span class="hl sng">          ============  =====================</span></span>
<span id="l_257" class="hl fld"><span class="hl lin">  257 </span><span class="hl sng">          Valid Arg     Meaning</span></span>
<span id="l_258" class="hl fld"><span class="hl lin">  258 </span><span class="hl sng">          ============  =====================</span></span>
<span id="l_259" class="hl fld"><span class="hl lin">  259 </span><span class="hl sng">          &quot;calls&quot;       call count</span></span>
<span id="l_260" class="hl fld"><span class="hl lin">  260 </span><span class="hl sng">          &quot;cumulative&quot;  cumulative time</span></span>
<span id="l_261" class="hl fld"><span class="hl lin">  261 </span><span class="hl sng">          &quot;file&quot;        file name</span></span>
<span id="l_262" class="hl fld"><span class="hl lin">  262 </span><span class="hl sng">          &quot;module&quot;      file name</span></span>
<span id="l_263" class="hl fld"><span class="hl lin">  263 </span><span class="hl sng">          &quot;pcalls&quot;      primitive call count</span></span>
<span id="l_264" class="hl fld"><span class="hl lin">  264 </span><span class="hl sng">          &quot;line&quot;        line number</span></span>
<span id="l_265" class="hl fld"><span class="hl lin">  265 </span><span class="hl sng">          &quot;name&quot;        function name</span></span>
<span id="l_266" class="hl fld"><span class="hl lin">  266 </span><span class="hl sng">          &quot;nfl&quot;         name/file/line</span></span>
<span id="l_267" class="hl fld"><span class="hl lin">  267 </span><span class="hl sng">          &quot;stdname&quot;     standard name</span></span>
<span id="l_268" class="hl fld"><span class="hl lin">  268 </span><span class="hl sng">          &quot;time&quot;        internal time</span></span>
<span id="l_269" class="hl fld"><span class="hl lin">  269 </span><span class="hl sng">          ============  =====================</span></span>
<span id="l_270" class="hl fld"><span class="hl lin">  270 </span><span class="hl sng"></span></span>
<span id="l_271" class="hl fld"><span class="hl lin">  271 </span><span class="hl sng">          Note that all sorts on statistics are in descending order (placing</span></span>
<span id="l_272" class="hl fld"><span class="hl lin">  272 </span><span class="hl sng">          most time consuming items first), where as name, file, and line number</span></span>
<span id="l_273" class="hl fld"><span class="hl lin">  273 </span><span class="hl sng">          searches are in ascending order (i.e., alphabetical). The subtle</span></span>
<span id="l_274" class="hl fld"><span class="hl lin">  274 </span><span class="hl sng">          distinction between &quot;nfl&quot; and &quot;stdname&quot; is that the standard name is a</span></span>
<span id="l_275" class="hl fld"><span class="hl lin">  275 </span><span class="hl sng">          sort of the name as printed, which means that the embedded line</span></span>
<span id="l_276" class="hl fld"><span class="hl lin">  276 </span><span class="hl sng">          numbers get compared in an odd way.  For example, lines 3, 20, and 40</span></span>
<span id="l_277" class="hl fld"><span class="hl lin">  277 </span><span class="hl sng">          would (if the file names were the same) appear in the string order</span></span>
<span id="l_278" class="hl fld"><span class="hl lin">  278 </span><span class="hl sng">          &quot;20&quot; &quot;3&quot; and &quot;40&quot;.  In contrast, &quot;nfl&quot; does a numeric compare of the</span></span>
<span id="l_279" class="hl fld"><span class="hl lin">  279 </span><span class="hl sng">          line numbers.  In fact, sort_stats(&quot;nfl&quot;) is the same as</span></span>
<span id="l_280" class="hl fld"><span class="hl lin">  280 </span><span class="hl sng">          sort_stats(&quot;name&quot;, &quot;file&quot;, &quot;line&quot;).</span></span>
<span id="l_281" class="hl fld"><span class="hl lin">  281 </span><span class="hl sng"></span></span>
<span id="l_282" class="hl fld"><span class="hl lin">  282 </span><span class="hl sng">        -T &lt;filename&gt;</span></span>
<span id="l_283" class="hl fld"><span class="hl lin">  283 </span><span class="hl sng">          save profile results as shown on screen to a text</span></span>
<span id="l_284" class="hl fld"><span class="hl lin">  284 </span><span class="hl sng">          file. The profile is still shown on screen.</span></span>
<span id="l_285" class="hl fld"><span class="hl lin">  285 </span><span class="hl sng"></span></span>
<span id="l_286" class="hl fld"><span class="hl lin">  286 </span><span class="hl sng">        -D &lt;filename&gt;</span></span>
<span id="l_287" class="hl fld"><span class="hl lin">  287 </span><span class="hl sng">          save (via dump_stats) profile statistics to given</span></span>
<span id="l_288" class="hl fld"><span class="hl lin">  288 </span><span class="hl sng">          filename. This data is in a format understood by the pstats module, and</span></span>
<span id="l_289" class="hl fld"><span class="hl lin">  289 </span><span class="hl sng">          is generated by a call to the dump_stats() method of profile</span></span>
<span id="l_290" class="hl fld"><span class="hl lin">  290 </span><span class="hl sng">          objects. The profile is still shown on screen.</span></span>
<span id="l_291" class="hl fld"><span class="hl lin">  291 </span><span class="hl sng"></span></span>
<span id="l_292" class="hl fld"><span class="hl lin">  292 </span><span class="hl sng">        -q</span></span>
<span id="l_293" class="hl fld"><span class="hl lin">  293 </span><span class="hl sng">          suppress output to the pager.  Best used with -T and/or -D above.</span></span>
<span id="l_294" class="hl fld"><span class="hl lin">  294 </span><span class="hl sng"></span></span>
<span id="l_295" class="hl fld"><span class="hl lin">  295 </span><span class="hl sng">        If you want to run complete programs under the profiler&#39;s control, use</span></span>
<span id="l_296" class="hl fld"><span class="hl lin">  296 </span><span class="hl sng">        ``</span><span class="hl ipl">%ru</span><span class="hl sng">n -p [prof_opts] filename.py [args to program]`` where prof_opts</span></span>
<span id="l_297" class="hl fld"><span class="hl lin">  297 </span><span class="hl sng">        contains profiler specific options as described here.</span></span>
<span id="l_298" class="hl fld"><span class="hl lin">  298 </span><span class="hl sng"></span></span>
<span id="l_299" class="hl fld"><span class="hl lin">  299 </span><span class="hl sng">        You can read the complete documentation for the profile module with::</span></span>
<span id="l_300" class="hl fld"><span class="hl lin">  300 </span><span class="hl sng"></span></span>
<span id="l_301" class="hl fld"><span class="hl lin">  301 </span><span class="hl sng">          In [1]: import profile; profile.help()</span></span>
<span id="l_302" class="hl fld"><span class="hl lin">  302 </span><span class="hl sng"></span></span>
<span id="l_303" class="hl fld"><span class="hl lin">  303 </span><span class="hl sng">        .. versionchanged:: 7.3</span></span>
<span id="l_304" class="hl fld"><span class="hl lin">  304 </span><span class="hl sng">            User variables are no longer expanded,</span></span>
<span id="l_305" class="hl fld"><span class="hl lin">  305 </span><span class="hl sng">            the magic line is always left unmodified.</span></span>
<span id="l_306" class="hl fld"><span class="hl lin">  306 </span><span class="hl sng"></span></span>
<span id="l_307" class="hl fld"><span class="hl lin">  307 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_308" class="hl fld"><span class="hl lin">  308 </span>        opts<span class="hl opt">,</span> arg_str <span class="hl opt">=</span> self<span class="hl opt">.</span><span class="hl kwd">parse_options</span><span class="hl opt">(</span>parameter_s<span class="hl opt">,</span> <span class="hl sng">&#39;D:l:rs:T:q&#39;</span><span class="hl opt">,</span></span>
<span id="l_309" class="hl fld"><span class="hl lin">  309 </span>                                           list_all<span class="hl opt">=</span><span class="hl kwa">True</span><span class="hl opt">,</span> posix<span class="hl opt">=</span><span class="hl kwa">False</span><span class="hl opt">)</span></span>
<span id="l_310" class="hl fld"><span class="hl lin">  310 </span>        <span class="hl kwa">if</span> cell <span class="hl kwa">is not None</span><span class="hl opt">:</span></span>
<span id="l_311" class="hl fld"><span class="hl lin">  311 </span>            arg_str <span class="hl opt">+=</span> <span class="hl sng">&#39;</span><span class="hl esc">\n</span><span class="hl sng">&#39;</span> <span class="hl opt">+</span> cell</span>
<span id="l_312" class="hl fld"><span class="hl lin">  312 </span>        arg_str <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">transform_cell</span><span class="hl opt">(</span>arg_str<span class="hl opt">)</span></span>
<span id="l_313" class="hl fld"><span class="hl lin">  313 </span>        <span class="hl kwa">return</span> self<span class="hl num">._</span>run<span class="hl num">_</span>with<span class="hl num">_</span>profiler<span class="hl opt">(</span>arg_str<span class="hl opt">,</span> opts<span class="hl opt">,</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">)</span></span>
<span id="l_314" class="hl fld"><span class="hl lin">  314 </span></span>
<span id="l_315" class="hl fld"><span class="hl lin">  315 </span>    <span class="hl kwa">def</span> <span class="hl kwd">_run_with_profiler</span><span class="hl opt">(</span>self<span class="hl opt">,</span> code<span class="hl opt">,</span> opts<span class="hl opt">,</span> namespace<span class="hl opt">):</span></span>
<span id="l_316" class="hl fld"><span class="hl lin">  316 </span>        <span class="hl sng">&quot;&quot;&quot;</span></span>
<span id="l_317" class="hl fld"><span class="hl lin">  317 </span><span class="hl sng">        Run `code` with profiler.  Used by ``%prun`` and ``</span><span class="hl ipl">%ru</span><span class="hl sng">n -p``.</span></span>
<span id="l_318" class="hl fld"><span class="hl lin">  318 </span><span class="hl sng"></span></span>
<span id="l_319" class="hl fld"><span class="hl lin">  319 </span><span class="hl sng">        Parameters</span></span>
<span id="l_320" class="hl fld"><span class="hl lin">  320 </span><span class="hl sng">        ----------</span></span>
<span id="l_321" class="hl fld"><span class="hl lin">  321 </span><span class="hl sng">        code : str</span></span>
<span id="l_322" class="hl fld"><span class="hl lin">  322 </span><span class="hl sng">            Code to be executed.</span></span>
<span id="l_323" class="hl fld"><span class="hl lin">  323 </span><span class="hl sng">        opts : Struct</span></span>
<span id="l_324" class="hl fld"><span class="hl lin">  324 </span><span class="hl sng">            Options parsed by `self.parse_options`.</span></span>
<span id="l_325" class="hl fld"><span class="hl lin">  325 </span><span class="hl sng">        namespace : dict</span></span>
<span id="l_326" class="hl fld"><span class="hl lin">  326 </span><span class="hl sng">            A dictionary for Python namespace (e.g., `self.shell.user_ns`).</span></span>
<span id="l_327" class="hl fld"><span class="hl lin">  327 </span><span class="hl sng"></span></span>
<span id="l_328" class="hl fld"><span class="hl lin">  328 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_329" class="hl fld"><span class="hl lin">  329 </span></span>
<span id="l_330" class="hl fld"><span class="hl lin">  330 </span>        <span class="hl slc"># Fill default values for unspecified options:</span></span>
<span id="l_331" class="hl fld"><span class="hl lin">  331 </span>        opts<span class="hl opt">.</span><span class="hl kwd">merge</span><span class="hl opt">(</span><span class="hl kwd">Struct</span><span class="hl opt">(</span>D<span class="hl opt">=[</span><span class="hl sng">&#39;&#39;</span><span class="hl opt">],</span> l<span class="hl opt">=[],</span> s<span class="hl opt">=[</span><span class="hl sng">&#39;time&#39;</span><span class="hl opt">],</span> T<span class="hl opt">=[</span><span class="hl sng">&#39;&#39;</span><span class="hl opt">]))</span></span>
<span id="l_332" class="hl fld"><span class="hl lin">  332 </span></span>
<span id="l_333" class="hl fld"><span class="hl lin">  333 </span>        prof <span class="hl opt">=</span> profile<span class="hl opt">.</span><span class="hl kwd">Profile</span><span class="hl opt">()</span></span>
<span id="l_334" class="hl fld"><span class="hl lin">  334 </span>        <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_335" class="hl fld"><span class="hl lin">  335 </span>            prof <span class="hl opt">=</span> prof<span class="hl opt">.</span><span class="hl kwd">runctx</span><span class="hl opt">(</span>code<span class="hl opt">,</span> namespace<span class="hl opt">,</span> namespace<span class="hl opt">)</span></span>
<span id="l_336" class="hl fld"><span class="hl lin">  336 </span>            sys_exit <span class="hl opt">=</span> <span class="hl sng">&#39;&#39;</span></span>
<span id="l_337" class="hl fld"><span class="hl lin">  337 </span>        <span class="hl kwa">except</span> <span class="hl kwc">SystemExit</span><span class="hl opt">:</span></span>
<span id="l_338" class="hl fld"><span class="hl lin">  338 </span>            sys_exit <span class="hl opt">=</span> <span class="hl sng">&quot;&quot;&quot;*** SystemExit exception caught in code being profiled.&quot;&quot;&quot;</span></span>
<span id="l_339" class="hl fld"><span class="hl lin">  339 </span></span>
<span id="l_340" class="hl fld"><span class="hl lin">  340 </span>        stats <span class="hl opt">=</span> pstats<span class="hl opt">.</span><span class="hl kwd">Stats</span><span class="hl opt">(</span>prof<span class="hl opt">).</span><span class="hl kwd">strip_dirs</span><span class="hl opt">().</span><span class="hl kwd">sort_stats</span><span class="hl opt">(*</span>opts<span class="hl opt">.</span>s<span class="hl opt">)</span></span>
<span id="l_341" class="hl fld"><span class="hl lin">  341 </span></span>
<span id="l_342" class="hl fld"><span class="hl lin">  342 </span>        lims <span class="hl opt">=</span> opts<span class="hl opt">.</span>l</span>
<span id="l_343" class="hl fld"><span class="hl lin">  343 </span>        <span class="hl kwa">if</span> lims<span class="hl opt">:</span></span>
<span id="l_344" class="hl fld"><span class="hl lin">  344 </span>            lims <span class="hl opt">= []</span>  <span class="hl slc"># rebuild lims with ints/floats/strings</span></span>
<span id="l_345" class="hl fld"><span class="hl lin">  345 </span>            <span class="hl kwa">for</span> lim <span class="hl kwa">in</span> opts<span class="hl opt">.</span>l<span class="hl opt">:</span></span>
<span id="l_346" class="hl fld"><span class="hl lin">  346 </span>                <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_347" class="hl fld"><span class="hl lin">  347 </span>                    lims<span class="hl opt">.</span><span class="hl kwd">append</span><span class="hl opt">(</span><span class="hl kwb">int</span><span class="hl opt">(</span>lim<span class="hl opt">))</span></span>
<span id="l_348" class="hl fld"><span class="hl lin">  348 </span>                <span class="hl kwa">except</span> <span class="hl kwc">ValueError</span><span class="hl opt">:</span></span>
<span id="l_349" class="hl fld"><span class="hl lin">  349 </span>                    <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_350" class="hl fld"><span class="hl lin">  350 </span>                        lims<span class="hl opt">.</span><span class="hl kwd">append</span><span class="hl opt">(</span><span class="hl kwb">float</span><span class="hl opt">(</span>lim<span class="hl opt">))</span></span>
<span id="l_351" class="hl fld"><span class="hl lin">  351 </span>                    <span class="hl kwa">except</span> <span class="hl kwc">ValueError</span><span class="hl opt">:</span></span>
<span id="l_352" class="hl fld"><span class="hl lin">  352 </span>                        lims<span class="hl opt">.</span><span class="hl kwd">append</span><span class="hl opt">(</span>lim<span class="hl opt">)</span></span>
<span id="l_353" class="hl fld"><span class="hl lin">  353 </span></span>
<span id="l_354" class="hl fld"><span class="hl lin">  354 </span>        <span class="hl slc"># Trap output.</span></span>
<span id="l_355" class="hl fld"><span class="hl lin">  355 </span>        stdout_trap <span class="hl opt">=</span> <span class="hl kwd">StringIO</span><span class="hl opt">()</span></span>
<span id="l_356" class="hl fld"><span class="hl lin">  356 </span>        stats_stream <span class="hl opt">=</span> stats<span class="hl opt">.</span>stream</span>
<span id="l_357" class="hl fld"><span class="hl lin">  357 </span>        <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_358" class="hl fld"><span class="hl lin">  358 </span>            stats<span class="hl opt">.</span>stream <span class="hl opt">=</span> stdout_trap</span>
<span id="l_359" class="hl fld"><span class="hl lin">  359 </span>            stats<span class="hl opt">.</span><span class="hl kwd">print_stats</span><span class="hl opt">(*</span>lims<span class="hl opt">)</span></span>
<span id="l_360" class="hl fld"><span class="hl lin">  360 </span>        <span class="hl kwa">finally</span><span class="hl opt">:</span></span>
<span id="l_361" class="hl fld"><span class="hl lin">  361 </span>            stats<span class="hl opt">.</span>stream <span class="hl opt">=</span> stats_stream</span>
<span id="l_362" class="hl fld"><span class="hl lin">  362 </span></span>
<span id="l_363" class="hl fld"><span class="hl lin">  363 </span>        output <span class="hl opt">=</span> stdout_trap<span class="hl opt">.</span><span class="hl kwd">getvalue</span><span class="hl opt">()</span></span>
<span id="l_364" class="hl fld"><span class="hl lin">  364 </span>        output <span class="hl opt">=</span> output<span class="hl opt">.</span><span class="hl kwd">rstrip</span><span class="hl opt">()</span></span>
<span id="l_365" class="hl fld"><span class="hl lin">  365 </span></span>
<span id="l_366" class="hl fld"><span class="hl lin">  366 </span>        <span class="hl kwa">if</span> <span class="hl sng">&#39;q&#39;</span> <span class="hl kwa">not in</span> opts<span class="hl opt">:</span></span>
<span id="l_367" class="hl fld"><span class="hl lin">  367 </span>            page<span class="hl opt">.</span><span class="hl kwd">page</span><span class="hl opt">(</span>output<span class="hl opt">)</span></span>
<span id="l_368" class="hl fld"><span class="hl lin">  368 </span>        <span class="hl kwa">print</span><span class="hl opt">(</span>sys_exit<span class="hl opt">,</span> end<span class="hl opt">=</span><span class="hl sng">&#39; &#39;</span><span class="hl opt">)</span></span>
<span id="l_369" class="hl fld"><span class="hl lin">  369 </span></span>
<span id="l_370" class="hl fld"><span class="hl lin">  370 </span>        dump_file <span class="hl opt">=</span> opts<span class="hl opt">.</span>D<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">]</span></span>
<span id="l_371" class="hl fld"><span class="hl lin">  371 </span>        text_file <span class="hl opt">=</span> opts<span class="hl opt">.</span>T<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">]</span></span>
<span id="l_372" class="hl fld"><span class="hl lin">  372 </span>        <span class="hl kwa">if</span> dump_file<span class="hl opt">:</span></span>
<span id="l_373" class="hl fld"><span class="hl lin">  373 </span>            prof<span class="hl opt">.</span><span class="hl kwd">dump_stats</span><span class="hl opt">(</span>dump_file<span class="hl opt">)</span></span>
<span id="l_374" class="hl fld"><span class="hl lin">  374 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span></span>
<span id="l_375" class="hl fld"><span class="hl lin">  375 </span>                f<span class="hl sng">&quot;</span><span class="hl esc">\n</span><span class="hl sng">*** Profile stats marshalled to file</span> <span class="hl ipl">{repr(dump_file)}</span><span class="hl sng">.</span><span class="hl ipl">{sys_exit}</span><span class="hl sng">&quot;</span></span>
<span id="l_376" class="hl fld"><span class="hl lin">  376 </span>            <span class="hl opt">)</span></span>
<span id="l_377" class="hl fld"><span class="hl lin">  377 </span>        <span class="hl kwa">if</span> text_file<span class="hl opt">:</span></span>
<span id="l_378" class="hl fld"><span class="hl lin">  378 </span>            pfile <span class="hl opt">=</span> <span class="hl kwd">Path</span><span class="hl opt">(</span>text_file<span class="hl opt">)</span></span>
<span id="l_379" class="hl fld"><span class="hl lin">  379 </span>            pfile<span class="hl opt">.</span><span class="hl kwd">touch</span><span class="hl opt">(</span>exist_ok<span class="hl opt">=</span><span class="hl kwa">True</span><span class="hl opt">)</span></span>
<span id="l_380" class="hl fld"><span class="hl lin">  380 </span>            pfile<span class="hl opt">.</span><span class="hl kwd">write_text</span><span class="hl opt">(</span>output<span class="hl opt">,</span> encoding<span class="hl opt">=</span><span class="hl sng">&quot;utf-8&quot;</span><span class="hl opt">)</span></span>
<span id="l_381" class="hl fld"><span class="hl lin">  381 </span></span>
<span id="l_382" class="hl fld"><span class="hl lin">  382 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span></span>
<span id="l_383" class="hl fld"><span class="hl lin">  383 </span>                f<span class="hl sng">&quot;</span><span class="hl esc">\n</span><span class="hl sng">*** Profile printout saved to text file</span> <span class="hl ipl">{repr(text_file)}</span><span class="hl sng">.</span><span class="hl ipl">{sys_exit}</span><span class="hl sng">&quot;</span></span>
<span id="l_384" class="hl fld"><span class="hl lin">  384 </span>            <span class="hl opt">)</span></span>
<span id="l_385" class="hl fld"><span class="hl lin">  385 </span></span>
<span id="l_386" class="hl fld"><span class="hl lin">  386 </span>        <span class="hl kwa">if</span> <span class="hl sng">&#39;r&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_387" class="hl fld"><span class="hl lin">  387 </span>            <span class="hl kwa">return</span> stats</span>
<span id="l_388" class="hl fld"><span class="hl lin">  388 </span></span>
<span id="l_389" class="hl fld"><span class="hl lin">  389 </span>        <span class="hl kwa">return None</span></span>
<span id="l_390" class="hl fld"><span class="hl lin">  390 </span></span>
<span id="l_391" class="hl fld"><span class="hl lin">  391 </span>    <span class="hl kwb">&#64;line_magic</span></span>
<span id="l_392" class="hl fld"><span class="hl lin">  392 </span>    <span class="hl kwa">def</span> <span class="hl kwd">pdb</span><span class="hl opt">(</span>self<span class="hl opt">,</span> parameter_s<span class="hl opt">=</span><span class="hl sng">&#39;&#39;</span><span class="hl opt">):</span></span>
<span id="l_393" class="hl fld"><span class="hl lin">  393 </span>        <span class="hl sng">&quot;&quot;&quot;Control the automatic calling of the pdb interactive debugger.</span></span>
<span id="l_394" class="hl fld"><span class="hl lin">  394 </span><span class="hl sng"></span></span>
<span id="l_395" class="hl fld"><span class="hl lin">  395 </span><span class="hl sng">        Call as &#39;%pdb on&#39;, &#39;%pdb 1&#39;, &#39;%pdb off&#39; or &#39;%pdb 0&#39;. If called without</span></span>
<span id="l_396" class="hl fld"><span class="hl lin">  396 </span><span class="hl sng">        argument it works as a toggle.</span></span>
<span id="l_397" class="hl fld"><span class="hl lin">  397 </span><span class="hl sng"></span></span>
<span id="l_398" class="hl fld"><span class="hl lin">  398 </span><span class="hl sng">        When an exception is triggered, IPython can optionally call the</span></span>
<span id="l_399" class="hl fld"><span class="hl lin">  399 </span><span class="hl sng">        interactive pdb debugger after the traceback printout. %pdb toggles</span></span>
<span id="l_400" class="hl fld"><span class="hl lin">  400 </span><span class="hl sng">        this feature on and off.</span></span>
<span id="l_401" class="hl fld"><span class="hl lin">  401 </span><span class="hl sng"></span></span>
<span id="l_402" class="hl fld"><span class="hl lin">  402 </span><span class="hl sng">        The initial state of this feature is set in your configuration</span></span>
<span id="l_403" class="hl fld"><span class="hl lin">  403 </span><span class="hl sng">        file (the option is ``InteractiveShell.pdb``).</span></span>
<span id="l_404" class="hl fld"><span class="hl lin">  404 </span><span class="hl sng"></span></span>
<span id="l_405" class="hl fld"><span class="hl lin">  405 </span><span class="hl sng">        If you want to just activate the debugger AFTER an exception has fired,</span></span>
<span id="l_406" class="hl fld"><span class="hl lin">  406 </span><span class="hl sng">        without having to type &#39;%pdb on&#39; and rerunning your code, you can use</span></span>
<span id="l_407" class="hl fld"><span class="hl lin">  407 </span><span class="hl sng">        the</span> <span class="hl ipl">%de</span><span class="hl sng">bug magic.&quot;&quot;&quot;</span></span>
<span id="l_408" class="hl fld"><span class="hl lin">  408 </span></span>
<span id="l_409" class="hl fld"><span class="hl lin">  409 </span>        par <span class="hl opt">=</span> parameter_s<span class="hl opt">.</span><span class="hl kwd">strip</span><span class="hl opt">().</span><span class="hl kwd">lower</span><span class="hl opt">()</span></span>
<span id="l_410" class="hl fld"><span class="hl lin">  410 </span></span>
<span id="l_411" class="hl fld"><span class="hl lin">  411 </span>        <span class="hl kwa">if</span> par<span class="hl opt">:</span></span>
<span id="l_412" class="hl fld"><span class="hl lin">  412 </span>            <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_413" class="hl fld"><span class="hl lin">  413 </span>                new_pdb <span class="hl opt">=</span> {&#39;off&#39;:0,&#39;0&#39;:0,&#39;on&#39;:1,&#39;1&#39;:1}<span class="hl opt">[</span>par<span class="hl opt">]</span></span>
<span id="l_414" class="hl fld"><span class="hl lin">  414 </span>            <span class="hl kwa">except</span> <span class="hl kwc">KeyError</span><span class="hl opt">:</span></span>
<span id="l_415" class="hl fld"><span class="hl lin">  415 </span>                <span class="hl kwa">print</span> <span class="hl opt">(</span><span class="hl sng">&#39;Incorrect argument. Use on/1, off/0, &#39;</span></span>
<span id="l_416" class="hl fld"><span class="hl lin">  416 </span>                       <span class="hl sng">&#39;or nothing for a toggle.&#39;</span><span class="hl opt">)</span></span>
<span id="l_417" class="hl fld"><span class="hl lin">  417 </span>                <span class="hl kwa">return</span></span>
<span id="l_418" class="hl fld"><span class="hl lin">  418 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_419" class="hl fld"><span class="hl lin">  419 </span>            <span class="hl slc"># toggle</span></span>
<span id="l_420" class="hl fld"><span class="hl lin">  420 </span>            new_pdb <span class="hl opt">=</span> <span class="hl kwa">not</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>call_pdb</span>
<span id="l_421" class="hl fld"><span class="hl lin">  421 </span></span>
<span id="l_422" class="hl fld"><span class="hl lin">  422 </span>        <span class="hl slc"># set on the shell</span></span>
<span id="l_423" class="hl fld"><span class="hl lin">  423 </span>        self<span class="hl opt">.</span>shell<span class="hl opt">.</span>call_pdb <span class="hl opt">=</span> new_pdb</span>
<span id="l_424" class="hl fld"><span class="hl lin">  424 </span>        <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&#39;Automatic pdb calling has been turned&#39;</span><span class="hl opt">,</span><span class="hl kwd">on_off</span><span class="hl opt">(</span>new_pdb<span class="hl opt">))</span></span>
<span id="l_425" class="hl fld"><span class="hl lin">  425 </span></span>
<span id="l_426" class="hl fld"><span class="hl lin">  426 </span>    <span class="hl kwb">&#64;magic_arguments.magic_arguments</span><span class="hl opt">()</span></span>
<span id="l_427" class="hl fld"><span class="hl lin">  427 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span><span class="hl sng">&#39;--breakpoint&#39;</span><span class="hl opt">,</span> <span class="hl sng">&#39;-b&#39;</span><span class="hl opt">,</span> metavar<span class="hl opt">=</span><span class="hl sng">&#39;FILE:LINE&#39;</span><span class="hl opt">,</span></span>
<span id="l_428" class="hl fld"><span class="hl lin">  428 </span>        <span class="hl kwb">help</span><span class="hl opt">=</span><span class="hl sng">&quot;&quot;&quot;</span></span>
<span id="l_429" class="hl fld"><span class="hl lin">  429 </span><span class="hl sng">        Set break point at LINE in FILE.</span></span>
<span id="l_430" class="hl fld"><span class="hl lin">  430 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_431" class="hl fld"><span class="hl lin">  431 </span>    <span class="hl opt">)</span></span>
<span id="l_432" class="hl fld"><span class="hl lin">  432 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span><span class="hl sng">&#39;statement&#39;</span><span class="hl opt">,</span> nargs<span class="hl opt">=</span><span class="hl sng">&#39;*&#39;</span><span class="hl opt">,</span></span>
<span id="l_433" class="hl fld"><span class="hl lin">  433 </span>        <span class="hl kwb">help</span><span class="hl opt">=</span><span class="hl sng">&quot;&quot;&quot;</span></span>
<span id="l_434" class="hl fld"><span class="hl lin">  434 </span><span class="hl sng">        Code to run in debugger.</span></span>
<span id="l_435" class="hl fld"><span class="hl lin">  435 </span><span class="hl sng">        You can omit this in cell magic mode.</span></span>
<span id="l_436" class="hl fld"><span class="hl lin">  436 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_437" class="hl fld"><span class="hl lin">  437 </span>    <span class="hl opt">)</span></span>
<span id="l_438" class="hl fld"><span class="hl lin">  438 </span>    <span class="hl kwb">&#64;no_var_expand</span></span>
<span id="l_439" class="hl fld"><span class="hl lin">  439 </span>    <span class="hl kwb">&#64;line_cell_magic</span></span>
<span id="l_440" class="hl fld"><span class="hl lin">  440 </span>    <span class="hl kwb">&#64;needs_local_scope</span></span>
<span id="l_441" class="hl fld"><span class="hl lin">  441 </span>    <span class="hl kwa">def</span> <span class="hl kwd">debug</span><span class="hl opt">(</span>self<span class="hl opt">,</span> line<span class="hl opt">=</span><span class="hl sng">&quot;&quot;</span><span class="hl opt">,</span> cell<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">,</span> local_ns<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">):</span></span>
<span id="l_442" class="hl fld"><span class="hl lin">  442 </span>        <span class="hl sng">&quot;&quot;&quot;Activate the interactive debugger.</span></span>
<span id="l_443" class="hl fld"><span class="hl lin">  443 </span><span class="hl sng"></span></span>
<span id="l_444" class="hl fld"><span class="hl lin">  444 </span><span class="hl sng">        This magic command support two ways of activating debugger.</span></span>
<span id="l_445" class="hl fld"><span class="hl lin">  445 </span><span class="hl sng">        One is to activate debugger before executing code.  This way, you</span></span>
<span id="l_446" class="hl fld"><span class="hl lin">  446 </span><span class="hl sng">        can set a break point, to step through the code from the point.</span></span>
<span id="l_447" class="hl fld"><span class="hl lin">  447 </span><span class="hl sng">        You can use this mode by giving statements to execute and optionally</span></span>
<span id="l_448" class="hl fld"><span class="hl lin">  448 </span><span class="hl sng">        a breakpoint.</span></span>
<span id="l_449" class="hl fld"><span class="hl lin">  449 </span><span class="hl sng"></span></span>
<span id="l_450" class="hl fld"><span class="hl lin">  450 </span><span class="hl sng">        The other one is to activate debugger in post-mortem mode.  You can</span></span>
<span id="l_451" class="hl fld"><span class="hl lin">  451 </span><span class="hl sng">        activate this mode simply running</span> <span class="hl ipl">%de</span><span class="hl sng">bug without any argument.</span></span>
<span id="l_452" class="hl fld"><span class="hl lin">  452 </span><span class="hl sng">        If an exception has just occurred, this lets you inspect its stack</span></span>
<span id="l_453" class="hl fld"><span class="hl lin">  453 </span><span class="hl sng">        frames interactively.  Note that this will always work only on the last</span></span>
<span id="l_454" class="hl fld"><span class="hl lin">  454 </span><span class="hl sng">        traceback that occurred, so you must call this quickly after an</span></span>
<span id="l_455" class="hl fld"><span class="hl lin">  455 </span><span class="hl sng">        exception that you wish to inspect has fired, because if another one</span></span>
<span id="l_456" class="hl fld"><span class="hl lin">  456 </span><span class="hl sng">        occurs, it clobbers the previous one.</span></span>
<span id="l_457" class="hl fld"><span class="hl lin">  457 </span><span class="hl sng"></span></span>
<span id="l_458" class="hl fld"><span class="hl lin">  458 </span><span class="hl sng">        If you want IPython to automatically do this on every exception, see</span></span>
<span id="l_459" class="hl fld"><span class="hl lin">  459 </span><span class="hl sng">        the %pdb magic for more details.</span></span>
<span id="l_460" class="hl fld"><span class="hl lin">  460 </span><span class="hl sng"></span></span>
<span id="l_461" class="hl fld"><span class="hl lin">  461 </span><span class="hl sng">        .. versionchanged:: 7.3</span></span>
<span id="l_462" class="hl fld"><span class="hl lin">  462 </span><span class="hl sng">            When running code, user variables are no longer expanded,</span></span>
<span id="l_463" class="hl fld"><span class="hl lin">  463 </span><span class="hl sng">            the magic line is always left unmodified.</span></span>
<span id="l_464" class="hl fld"><span class="hl lin">  464 </span><span class="hl sng"></span></span>
<span id="l_465" class="hl fld"><span class="hl lin">  465 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_466" class="hl fld"><span class="hl lin">  466 </span>        args <span class="hl opt">=</span> magic_arguments<span class="hl opt">.</span><span class="hl kwd">parse_argstring</span><span class="hl opt">(</span>self<span class="hl opt">.</span>debug<span class="hl opt">,</span> line<span class="hl opt">)</span></span>
<span id="l_467" class="hl fld"><span class="hl lin">  467 </span></span>
<span id="l_468" class="hl fld"><span class="hl lin">  468 </span>        <span class="hl kwa">if not</span> <span class="hl opt">(</span>args<span class="hl opt">.</span>breakpoint <span class="hl kwa">or</span> args<span class="hl opt">.</span>statement <span class="hl kwa">or</span> cell<span class="hl opt">):</span></span>
<span id="l_469" class="hl fld"><span class="hl lin">  469 </span>            self<span class="hl num">._</span>debug<span class="hl num">_</span>post<span class="hl num">_</span>mortem<span class="hl opt">()</span></span>
<span id="l_470" class="hl fld"><span class="hl lin">  470 </span>        <span class="hl kwa">elif not</span> <span class="hl opt">(</span>args<span class="hl opt">.</span>breakpoint <span class="hl kwa">or</span> cell<span class="hl opt">):</span></span>
<span id="l_471" class="hl fld"><span class="hl lin">  471 </span>            <span class="hl slc"># If there is no breakpoints, the line is just code to execute</span></span>
<span id="l_472" class="hl fld"><span class="hl lin">  472 </span>            self<span class="hl num">._</span>debug<span class="hl num">_</span>exec<span class="hl opt">(</span>line<span class="hl opt">,</span> <span class="hl kwa">None</span><span class="hl opt">,</span> local_ns<span class="hl opt">)</span></span>
<span id="l_473" class="hl fld"><span class="hl lin">  473 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_474" class="hl fld"><span class="hl lin">  474 </span>            <span class="hl slc"># Here we try to reconstruct the code from the output of</span></span>
<span id="l_475" class="hl fld"><span class="hl lin">  475 </span>            <span class="hl slc"># parse_argstring. This might not work if the code has spaces</span></span>
<span id="l_476" class="hl fld"><span class="hl lin">  476 </span>            <span class="hl slc"># For example this fails for `print(&quot;a b&quot;)`</span></span>
<span id="l_477" class="hl fld"><span class="hl lin">  477 </span>            code <span class="hl opt">=</span> <span class="hl sng">&quot;</span><span class="hl esc">\n</span><span class="hl sng">&quot;</span><span class="hl opt">.</span><span class="hl kwd">join</span><span class="hl opt">(</span>args<span class="hl opt">.</span>statement<span class="hl opt">)</span></span>
<span id="l_478" class="hl fld"><span class="hl lin">  478 </span>            <span class="hl kwa">if</span> cell<span class="hl opt">:</span></span>
<span id="l_479" class="hl fld"><span class="hl lin">  479 </span>                code <span class="hl opt">+=</span> <span class="hl sng">&quot;</span><span class="hl esc">\n</span><span class="hl sng">&quot;</span> <span class="hl opt">+</span> cell</span>
<span id="l_480" class="hl fld"><span class="hl lin">  480 </span>            self<span class="hl num">._</span>debug<span class="hl num">_</span>exec<span class="hl opt">(</span>code<span class="hl opt">,</span> args<span class="hl opt">.</span>breakpoint<span class="hl opt">,</span> local_ns<span class="hl opt">)</span></span>
<span id="l_481" class="hl fld"><span class="hl lin">  481 </span></span>
<span id="l_482" class="hl fld"><span class="hl lin">  482 </span>    <span class="hl kwa">def</span> <span class="hl kwd">_debug_post_mortem</span><span class="hl opt">(</span>self<span class="hl opt">):</span></span>
<span id="l_483" class="hl fld"><span class="hl lin">  483 </span>        self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">debugger</span><span class="hl opt">(</span>force<span class="hl opt">=</span><span class="hl kwa">True</span><span class="hl opt">)</span></span>
<span id="l_484" class="hl fld"><span class="hl lin">  484 </span></span>
<span id="l_485" class="hl fld"><span class="hl lin">  485 </span>    <span class="hl kwa">def</span> <span class="hl kwd">_debug_exec</span><span class="hl opt">(</span>self<span class="hl opt">,</span> code<span class="hl opt">,</span> breakpoint<span class="hl opt">,</span> local_ns<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">):</span></span>
<span id="l_486" class="hl fld"><span class="hl lin">  486 </span>        <span class="hl kwa">if</span> breakpoint<span class="hl opt">:</span></span>
<span id="l_487" class="hl fld"><span class="hl lin">  487 </span>            <span class="hl opt">(</span>filename<span class="hl opt">,</span> bp_line<span class="hl opt">) =</span> breakpoint<span class="hl opt">.</span><span class="hl kwd">rsplit</span><span class="hl opt">(</span><span class="hl sng">&#39;:&#39;</span><span class="hl opt">,</span> <span class="hl num">1</span><span class="hl opt">)</span></span>
<span id="l_488" class="hl fld"><span class="hl lin">  488 </span>            bp_line <span class="hl opt">=</span> <span class="hl kwb">int</span><span class="hl opt">(</span>bp_line<span class="hl opt">)</span></span>
<span id="l_489" class="hl fld"><span class="hl lin">  489 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_490" class="hl fld"><span class="hl lin">  490 </span>            <span class="hl opt">(</span>filename<span class="hl opt">,</span> bp_line<span class="hl opt">) = (</span><span class="hl kwa">None</span><span class="hl opt">,</span> <span class="hl kwa">None</span><span class="hl opt">)</span></span>
<span id="l_491" class="hl fld"><span class="hl lin">  491 </span>        self<span class="hl num">._</span>run<span class="hl num">_</span>with<span class="hl num">_</span>debugger<span class="hl opt">(</span></span>
<span id="l_492" class="hl fld"><span class="hl lin">  492 </span>            code<span class="hl opt">,</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">,</span> filename<span class="hl opt">,</span> bp_line<span class="hl opt">,</span> local_ns<span class="hl opt">=</span>local_ns</span>
<span id="l_493" class="hl fld"><span class="hl lin">  493 </span>        <span class="hl opt">)</span></span>
<span id="l_494" class="hl fld"><span class="hl lin">  494 </span></span>
<span id="l_495" class="hl fld"><span class="hl lin">  495 </span>    <span class="hl kwb">&#64;line_magic</span></span>
<span id="l_496" class="hl fld"><span class="hl lin">  496 </span>    <span class="hl kwa">def</span> <span class="hl kwd">tb</span><span class="hl opt">(</span>self<span class="hl opt">,</span> s<span class="hl opt">):</span></span>
<span id="l_497" class="hl fld"><span class="hl lin">  497 </span>        <span class="hl sng">&quot;&quot;&quot;Print the last traceback.</span></span>
<span id="l_498" class="hl fld"><span class="hl lin">  498 </span><span class="hl sng"></span></span>
<span id="l_499" class="hl fld"><span class="hl lin">  499 </span><span class="hl sng">        Optionally, specify an exception reporting mode, tuning the</span></span>
<span id="l_500" class="hl fld"><span class="hl lin">  500 </span><span class="hl sng">        verbosity of the traceback. By default the currently-active exception</span></span>
<span id="l_501" class="hl fld"><span class="hl lin">  501 </span><span class="hl sng">        mode is used. See</span> <span class="hl ipl">%x</span><span class="hl sng">mode for changing exception reporting modes.</span></span>
<span id="l_502" class="hl fld"><span class="hl lin">  502 </span><span class="hl sng"></span></span>
<span id="l_503" class="hl fld"><span class="hl lin">  503 </span><span class="hl sng">        Valid modes: Plain, Context, Verbose, and Minimal.</span></span>
<span id="l_504" class="hl fld"><span class="hl lin">  504 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_505" class="hl fld"><span class="hl lin">  505 </span>        interactive_tb <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>InteractiveTB</span>
<span id="l_506" class="hl fld"><span class="hl lin">  506 </span>        <span class="hl kwa">if</span> s<span class="hl opt">:</span></span>
<span id="l_507" class="hl fld"><span class="hl lin">  507 </span>            <span class="hl slc"># Switch exception reporting mode for this one call.</span></span>
<span id="l_508" class="hl fld"><span class="hl lin">  508 </span>            <span class="hl slc"># Ensure it is switched back.</span></span>
<span id="l_509" class="hl fld"><span class="hl lin">  509 </span>            <span class="hl kwa">def</span> <span class="hl kwd">xmode_switch_err</span><span class="hl opt">(</span>name<span class="hl opt">):</span></span>
<span id="l_510" class="hl fld"><span class="hl lin">  510 </span>                <span class="hl kwd">warn</span><span class="hl opt">(</span><span class="hl sng">&#39;Error changing</span> <span class="hl ipl">%s</span> <span class="hl sng">exception modes.</span><span class="hl esc">\n</span><span class="hl sng"></span><span class="hl ipl">%s</span><span class="hl sng">&#39;</span> <span class="hl opt">%</span></span>
<span id="l_511" class="hl fld"><span class="hl lin">  511 </span>                    <span class="hl opt">(</span>name<span class="hl opt">,</span>sys<span class="hl opt">.</span><span class="hl kwd">exc_info</span><span class="hl opt">()[</span><span class="hl num">1</span><span class="hl opt">]))</span></span>
<span id="l_512" class="hl fld"><span class="hl lin">  512 </span></span>
<span id="l_513" class="hl fld"><span class="hl lin">  513 </span>            new_mode <span class="hl opt">=</span> s<span class="hl opt">.</span><span class="hl kwd">strip</span><span class="hl opt">().</span><span class="hl kwd">capitalize</span><span class="hl opt">()</span></span>
<span id="l_514" class="hl fld"><span class="hl lin">  514 </span>            original_mode <span class="hl opt">=</span> interactive_tb<span class="hl opt">.</span>mode</span>
<span id="l_515" class="hl fld"><span class="hl lin">  515 </span>            <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_516" class="hl fld"><span class="hl lin">  516 </span>                <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_517" class="hl fld"><span class="hl lin">  517 </span>                    interactive_tb<span class="hl opt">.</span><span class="hl kwd">set_mode</span><span class="hl opt">(</span>mode<span class="hl opt">=</span>new_mode<span class="hl opt">)</span></span>
<span id="l_518" class="hl fld"><span class="hl lin">  518 </span>                <span class="hl kwa">except</span> <span class="hl kwc">Exception</span><span class="hl opt">:</span></span>
<span id="l_519" class="hl fld"><span class="hl lin">  519 </span>                    <span class="hl kwd">xmode_switch_err</span><span class="hl opt">(</span><span class="hl sng">&#39;user&#39;</span><span class="hl opt">)</span></span>
<span id="l_520" class="hl fld"><span class="hl lin">  520 </span>                <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_521" class="hl fld"><span class="hl lin">  521 </span>                    self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">showtraceback</span><span class="hl opt">()</span></span>
<span id="l_522" class="hl fld"><span class="hl lin">  522 </span>            <span class="hl kwa">finally</span><span class="hl opt">:</span></span>
<span id="l_523" class="hl fld"><span class="hl lin">  523 </span>                interactive_tb<span class="hl opt">.</span><span class="hl kwd">set_mode</span><span class="hl opt">(</span>mode<span class="hl opt">=</span>original_mode<span class="hl opt">)</span></span>
<span id="l_524" class="hl fld"><span class="hl lin">  524 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_525" class="hl fld"><span class="hl lin">  525 </span>            self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">showtraceback</span><span class="hl opt">()</span></span>
<span id="l_526" class="hl fld"><span class="hl lin">  526 </span></span>
<span id="l_527" class="hl fld"><span class="hl lin">  527 </span>    <span class="hl kwb">&#64;skip_doctest</span></span>
<span id="l_528" class="hl fld"><span class="hl lin">  528 </span>    <span class="hl kwb">&#64;line_magic</span></span>
<span id="l_529" class="hl fld"><span class="hl lin">  529 </span>    <span class="hl kwa">def</span> <span class="hl kwd">run</span><span class="hl opt">(</span>self<span class="hl opt">,</span> parameter_s<span class="hl opt">=</span><span class="hl sng">&#39;&#39;</span><span class="hl opt">,</span> runner<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">,</span></span>
<span id="l_530" class="hl fld"><span class="hl lin">  530 </span>                  file_finder<span class="hl opt">=</span>get_py_filename<span class="hl opt">):</span></span>
<span id="l_531" class="hl fld"><span class="hl lin">  531 </span>        <span class="hl sng">&quot;&quot;&quot;Run the named file inside IPython as a program.</span></span>
<span id="l_532" class="hl fld"><span class="hl lin">  532 </span><span class="hl sng"></span></span>
<span id="l_533" class="hl fld"><span class="hl lin">  533 </span><span class="hl sng">        Usage::</span></span>
<span id="l_534" class="hl fld"><span class="hl lin">  534 </span><span class="hl sng"></span></span>
<span id="l_535" class="hl fld"><span class="hl lin">  535 </span><span class="hl sng"></span>          <span class="hl ipl">%ru</span><span class="hl sng">n [-n -i -e -G]</span></span>
<span id="l_536" class="hl fld"><span class="hl lin">  536 </span><span class="hl sng">               [( -t [-N&lt;N&gt;] | -d [-b&lt;N&gt;] | -p [profile options] )]</span></span>
<span id="l_537" class="hl fld"><span class="hl lin">  537 </span><span class="hl sng">               ( -m mod | filename ) [args]</span></span>
<span id="l_538" class="hl fld"><span class="hl lin">  538 </span><span class="hl sng"></span></span>
<span id="l_539" class="hl fld"><span class="hl lin">  539 </span><span class="hl sng">        The filename argument should be either a pure Python script (with</span></span>
<span id="l_540" class="hl fld"><span class="hl lin">  540 </span><span class="hl sng">        extension ``.py``), or a file with custom IPython syntax (such as</span></span>
<span id="l_541" class="hl fld"><span class="hl lin">  541 </span><span class="hl sng">        magics). If the latter, the file can be either a script with ``.ipy``</span></span>
<span id="l_542" class="hl fld"><span class="hl lin">  542 </span><span class="hl sng">        extension, or a Jupyter notebook with ``.ipynb`` extension. When running</span></span>
<span id="l_543" class="hl fld"><span class="hl lin">  543 </span><span class="hl sng">        a Jupyter notebook, the output from print statements and other</span></span>
<span id="l_544" class="hl fld"><span class="hl lin">  544 </span><span class="hl sng">        displayed objects will appear in the terminal (even matplotlib figures</span></span>
<span id="l_545" class="hl fld"><span class="hl lin">  545 </span><span class="hl sng">        will open, if a terminal-compliant backend is being used). Note that,</span></span>
<span id="l_546" class="hl fld"><span class="hl lin">  546 </span><span class="hl sng">        at the system command line, the ``jupyter run`` command offers similar</span></span>
<span id="l_547" class="hl fld"><span class="hl lin">  547 </span><span class="hl sng">        functionality for executing notebooks (albeit currently with some</span></span>
<span id="l_548" class="hl fld"><span class="hl lin">  548 </span><span class="hl sng">        differences in supported options).</span></span>
<span id="l_549" class="hl fld"><span class="hl lin">  549 </span><span class="hl sng"></span></span>
<span id="l_550" class="hl fld"><span class="hl lin">  550 </span><span class="hl sng">        Parameters after the filename are passed as command-line arguments to</span></span>
<span id="l_551" class="hl fld"><span class="hl lin">  551 </span><span class="hl sng">        the program (put in sys.argv). Then, control returns to IPython&#39;s</span></span>
<span id="l_552" class="hl fld"><span class="hl lin">  552 </span><span class="hl sng">        prompt.</span></span>
<span id="l_553" class="hl fld"><span class="hl lin">  553 </span><span class="hl sng"></span></span>
<span id="l_554" class="hl fld"><span class="hl lin">  554 </span><span class="hl sng">        This is similar to running at a system prompt ``python file args``,</span></span>
<span id="l_555" class="hl fld"><span class="hl lin">  555 </span><span class="hl sng">        but with the advantage of giving you IPython&#39;s tracebacks, and of</span></span>
<span id="l_556" class="hl fld"><span class="hl lin">  556 </span><span class="hl sng">        loading all variables into your interactive namespace for further use</span></span>
<span id="l_557" class="hl fld"><span class="hl lin">  557 </span><span class="hl sng">        (unless -p is used, see below).</span></span>
<span id="l_558" class="hl fld"><span class="hl lin">  558 </span><span class="hl sng"></span></span>
<span id="l_559" class="hl fld"><span class="hl lin">  559 </span><span class="hl sng">        The file is executed in a namespace initially consisting only of</span></span>
<span id="l_560" class="hl fld"><span class="hl lin">  560 </span><span class="hl sng">        ``__name__==&#39;__main__&#39;`` and sys.argv constructed as indicated. It thus</span></span>
<span id="l_561" class="hl fld"><span class="hl lin">  561 </span><span class="hl sng">        sees its environment as if it were being run as a stand-alone program</span></span>
<span id="l_562" class="hl fld"><span class="hl lin">  562 </span><span class="hl sng">        (except for sharing global objects such as previously imported</span></span>
<span id="l_563" class="hl fld"><span class="hl lin">  563 </span><span class="hl sng">        modules). But after execution, the IPython interactive namespace gets</span></span>
<span id="l_564" class="hl fld"><span class="hl lin">  564 </span><span class="hl sng">        updated with all variables defined in the program (except for __name__</span></span>
<span id="l_565" class="hl fld"><span class="hl lin">  565 </span><span class="hl sng">        and sys.argv). This allows for very convenient loading of code for</span></span>
<span id="l_566" class="hl fld"><span class="hl lin">  566 </span><span class="hl sng">        interactive work, while giving each program a &#39;clean sheet&#39; to run in.</span></span>
<span id="l_567" class="hl fld"><span class="hl lin">  567 </span><span class="hl sng"></span></span>
<span id="l_568" class="hl fld"><span class="hl lin">  568 </span><span class="hl sng">        Arguments are expanded using shell-like glob match.  Patterns</span></span>
<span id="l_569" class="hl fld"><span class="hl lin">  569 </span><span class="hl sng">        &#39;*&#39;, &#39;?&#39;, &#39;[seq]&#39; and &#39;[!seq]&#39; can be used.  Additionally,</span></span>
<span id="l_570" class="hl fld"><span class="hl lin">  570 </span><span class="hl sng">        tilde &#39;~&#39; will be expanded into user&#39;s home directory.  Unlike</span></span>
<span id="l_571" class="hl fld"><span class="hl lin">  571 </span><span class="hl sng">        real shells, quotation does not suppress expansions.  Use</span></span>
<span id="l_572" class="hl fld"><span class="hl lin">  572 </span><span class="hl sng">        *two* back slashes (e.g. ``</span><span class="hl esc">\\\\</span><span class="hl sng">*``) to suppress expansions.</span></span>
<span id="l_573" class="hl fld"><span class="hl lin">  573 </span><span class="hl sng">        To completely disable these expansions, you can use -G flag.</span></span>
<span id="l_574" class="hl fld"><span class="hl lin">  574 </span><span class="hl sng"></span></span>
<span id="l_575" class="hl fld"><span class="hl lin">  575 </span><span class="hl sng">        On Windows systems, the use of single quotes `&#39;` when specifying</span></span>
<span id="l_576" class="hl fld"><span class="hl lin">  576 </span><span class="hl sng">        a file is not supported. Use double quotes `&quot;`.</span></span>
<span id="l_577" class="hl fld"><span class="hl lin">  577 </span><span class="hl sng"></span></span>
<span id="l_578" class="hl fld"><span class="hl lin">  578 </span><span class="hl sng">        Options:</span></span>
<span id="l_579" class="hl fld"><span class="hl lin">  579 </span><span class="hl sng"></span></span>
<span id="l_580" class="hl fld"><span class="hl lin">  580 </span><span class="hl sng">        -n</span></span>
<span id="l_581" class="hl fld"><span class="hl lin">  581 </span><span class="hl sng">          __name__ is NOT set to &#39;__main__&#39;, but to the running file&#39;s name</span></span>
<span id="l_582" class="hl fld"><span class="hl lin">  582 </span><span class="hl sng">          without extension (as python does under import).  This allows running</span></span>
<span id="l_583" class="hl fld"><span class="hl lin">  583 </span><span class="hl sng">          scripts and reloading the definitions in them without calling code</span></span>
<span id="l_584" class="hl fld"><span class="hl lin">  584 </span><span class="hl sng">          protected by an ``if __name__ == &quot;__main__&quot;`` clause.</span></span>
<span id="l_585" class="hl fld"><span class="hl lin">  585 </span><span class="hl sng"></span></span>
<span id="l_586" class="hl fld"><span class="hl lin">  586 </span><span class="hl sng">        -i</span></span>
<span id="l_587" class="hl fld"><span class="hl lin">  587 </span><span class="hl sng">          run the file in IPython&#39;s namespace instead of an empty one. This</span></span>
<span id="l_588" class="hl fld"><span class="hl lin">  588 </span><span class="hl sng">          is useful if you are experimenting with code written in a text editor</span></span>
<span id="l_589" class="hl fld"><span class="hl lin">  589 </span><span class="hl sng">          which depends on variables defined interactively.</span></span>
<span id="l_590" class="hl fld"><span class="hl lin">  590 </span><span class="hl sng"></span></span>
<span id="l_591" class="hl fld"><span class="hl lin">  591 </span><span class="hl sng">        -e</span></span>
<span id="l_592" class="hl fld"><span class="hl lin">  592 </span><span class="hl sng">          ignore sys.exit() calls or SystemExit exceptions in the script</span></span>
<span id="l_593" class="hl fld"><span class="hl lin">  593 </span><span class="hl sng">          being run.  This is particularly useful if IPython is being used to</span></span>
<span id="l_594" class="hl fld"><span class="hl lin">  594 </span><span class="hl sng">          run unittests, which always exit with a sys.exit() call.  In such</span></span>
<span id="l_595" class="hl fld"><span class="hl lin">  595 </span><span class="hl sng">          cases you are interested in the output of the test results, not in</span></span>
<span id="l_596" class="hl fld"><span class="hl lin">  596 </span><span class="hl sng">          seeing a traceback of the unittest module.</span></span>
<span id="l_597" class="hl fld"><span class="hl lin">  597 </span><span class="hl sng"></span></span>
<span id="l_598" class="hl fld"><span class="hl lin">  598 </span><span class="hl sng">        -t</span></span>
<span id="l_599" class="hl fld"><span class="hl lin">  599 </span><span class="hl sng">          print timing information at the end of the run.  IPython will give</span></span>
<span id="l_600" class="hl fld"><span class="hl lin">  600 </span><span class="hl sng">          you an estimated CPU time consumption for your script, which under</span></span>
<span id="l_601" class="hl fld"><span class="hl lin">  601 </span><span class="hl sng">          Unix uses the resource module to avoid the wraparound problems of</span></span>
<span id="l_602" class="hl fld"><span class="hl lin">  602 </span><span class="hl sng">          time.clock().  Under Unix, an estimate of time spent on system tasks</span></span>
<span id="l_603" class="hl fld"><span class="hl lin">  603 </span><span class="hl sng">          is also given (for Windows platforms this is reported as 0.0).</span></span>
<span id="l_604" class="hl fld"><span class="hl lin">  604 </span><span class="hl sng"></span></span>
<span id="l_605" class="hl fld"><span class="hl lin">  605 </span><span class="hl sng">        If -t is given, an additional ``-N&lt;N&gt;`` option can be given, where &lt;N&gt;</span></span>
<span id="l_606" class="hl fld"><span class="hl lin">  606 </span><span class="hl sng">        must be an integer indicating how many times you want the script to</span></span>
<span id="l_607" class="hl fld"><span class="hl lin">  607 </span><span class="hl sng">        run.  The final timing report will include total and per run results.</span></span>
<span id="l_608" class="hl fld"><span class="hl lin">  608 </span><span class="hl sng"></span></span>
<span id="l_609" class="hl fld"><span class="hl lin">  609 </span><span class="hl sng">        For example (testing the script uniq_stable.py)::</span></span>
<span id="l_610" class="hl fld"><span class="hl lin">  610 </span><span class="hl sng"></span></span>
<span id="l_611" class="hl fld"><span class="hl lin">  611 </span><span class="hl sng">            In [1]: run -t uniq_stable</span></span>
<span id="l_612" class="hl fld"><span class="hl lin">  612 </span><span class="hl sng"></span></span>
<span id="l_613" class="hl fld"><span class="hl lin">  613 </span><span class="hl sng">            IPython CPU timings (estimated):</span></span>
<span id="l_614" class="hl fld"><span class="hl lin">  614 </span><span class="hl sng">              User  :    0.19597 s.</span></span>
<span id="l_615" class="hl fld"><span class="hl lin">  615 </span><span class="hl sng">              System:        0.0 s.</span></span>
<span id="l_616" class="hl fld"><span class="hl lin">  616 </span><span class="hl sng"></span></span>
<span id="l_617" class="hl fld"><span class="hl lin">  617 </span><span class="hl sng">            In [2]: run -t -N5 uniq_stable</span></span>
<span id="l_618" class="hl fld"><span class="hl lin">  618 </span><span class="hl sng"></span></span>
<span id="l_619" class="hl fld"><span class="hl lin">  619 </span><span class="hl sng">            IPython CPU timings (estimated):</span></span>
<span id="l_620" class="hl fld"><span class="hl lin">  620 </span><span class="hl sng">            Total runs performed: 5</span></span>
<span id="l_621" class="hl fld"><span class="hl lin">  621 </span><span class="hl sng">              Times :      Total       Per run</span></span>
<span id="l_622" class="hl fld"><span class="hl lin">  622 </span><span class="hl sng">              User  :   0.910862 s,  0.1821724 s.</span></span>
<span id="l_623" class="hl fld"><span class="hl lin">  623 </span><span class="hl sng">              System:        0.0 s,        0.0 s.</span></span>
<span id="l_624" class="hl fld"><span class="hl lin">  624 </span><span class="hl sng"></span></span>
<span id="l_625" class="hl fld"><span class="hl lin">  625 </span><span class="hl sng">        -d</span></span>
<span id="l_626" class="hl fld"><span class="hl lin">  626 </span><span class="hl sng">          run your program under the control of pdb, the Python debugger.</span></span>
<span id="l_627" class="hl fld"><span class="hl lin">  627 </span><span class="hl sng">          This allows you to execute your program step by step, watch variables,</span></span>
<span id="l_628" class="hl fld"><span class="hl lin">  628 </span><span class="hl sng">          etc.  Internally, what IPython does is similar to calling::</span></span>
<span id="l_629" class="hl fld"><span class="hl lin">  629 </span><span class="hl sng"></span></span>
<span id="l_630" class="hl fld"><span class="hl lin">  630 </span><span class="hl sng">              pdb.run(&#39;execfile(&quot;YOURFILENAME&quot;)&#39;)</span></span>
<span id="l_631" class="hl fld"><span class="hl lin">  631 </span><span class="hl sng"></span></span>
<span id="l_632" class="hl fld"><span class="hl lin">  632 </span><span class="hl sng">          with a breakpoint set on line 1 of your file.  You can change the line</span></span>
<span id="l_633" class="hl fld"><span class="hl lin">  633 </span><span class="hl sng">          number for this automatic breakpoint to be &lt;N&gt; by using the -bN option</span></span>
<span id="l_634" class="hl fld"><span class="hl lin">  634 </span><span class="hl sng">          (where N must be an integer). For example::</span></span>
<span id="l_635" class="hl fld"><span class="hl lin">  635 </span><span class="hl sng"></span></span>
<span id="l_636" class="hl fld"><span class="hl lin">  636 </span><span class="hl sng"></span>              <span class="hl ipl">%ru</span><span class="hl sng">n -d -b40 myscript</span></span>
<span id="l_637" class="hl fld"><span class="hl lin">  637 </span><span class="hl sng"></span></span>
<span id="l_638" class="hl fld"><span class="hl lin">  638 </span><span class="hl sng">          will set the first breakpoint at line 40 in myscript.py.  Note that</span></span>
<span id="l_639" class="hl fld"><span class="hl lin">  639 </span><span class="hl sng">          the first breakpoint must be set on a line which actually does</span></span>
<span id="l_640" class="hl fld"><span class="hl lin">  640 </span><span class="hl sng">          something (not a comment or docstring) for it to stop execution.</span></span>
<span id="l_641" class="hl fld"><span class="hl lin">  641 </span><span class="hl sng"></span></span>
<span id="l_642" class="hl fld"><span class="hl lin">  642 </span><span class="hl sng">          Or you can specify a breakpoint in a different file::</span></span>
<span id="l_643" class="hl fld"><span class="hl lin">  643 </span><span class="hl sng"></span></span>
<span id="l_644" class="hl fld"><span class="hl lin">  644 </span><span class="hl sng"></span>              <span class="hl ipl">%ru</span><span class="hl sng">n -d -b myotherfile.py:20 myscript</span></span>
<span id="l_645" class="hl fld"><span class="hl lin">  645 </span><span class="hl sng"></span></span>
<span id="l_646" class="hl fld"><span class="hl lin">  646 </span><span class="hl sng">          When the pdb debugger starts, you will see a (Pdb) prompt.  You must</span></span>
<span id="l_647" class="hl fld"><span class="hl lin">  647 </span><span class="hl sng">          first enter &#39;c&#39; (without quotes) to start execution up to the first</span></span>
<span id="l_648" class="hl fld"><span class="hl lin">  648 </span><span class="hl sng">          breakpoint.</span></span>
<span id="l_649" class="hl fld"><span class="hl lin">  649 </span><span class="hl sng"></span></span>
<span id="l_650" class="hl fld"><span class="hl lin">  650 </span><span class="hl sng">          Entering &#39;help&#39; gives information about the use of the debugger.  You</span></span>
<span id="l_651" class="hl fld"><span class="hl lin">  651 </span><span class="hl sng">          can easily see pdb&#39;s full documentation with &quot;import pdb;pdb.help()&quot;</span></span>
<span id="l_652" class="hl fld"><span class="hl lin">  652 </span><span class="hl sng">          at a prompt.</span></span>
<span id="l_653" class="hl fld"><span class="hl lin">  653 </span><span class="hl sng"></span></span>
<span id="l_654" class="hl fld"><span class="hl lin">  654 </span><span class="hl sng">        -p</span></span>
<span id="l_655" class="hl fld"><span class="hl lin">  655 </span><span class="hl sng">          run program under the control of the Python profiler module (which</span></span>
<span id="l_656" class="hl fld"><span class="hl lin">  656 </span><span class="hl sng">          prints a detailed report of execution times, function calls, etc).</span></span>
<span id="l_657" class="hl fld"><span class="hl lin">  657 </span><span class="hl sng"></span></span>
<span id="l_658" class="hl fld"><span class="hl lin">  658 </span><span class="hl sng">          You can pass other options after -p which affect the behavior of the</span></span>
<span id="l_659" class="hl fld"><span class="hl lin">  659 </span><span class="hl sng">          profiler itself. See the docs for %prun for details.</span></span>
<span id="l_660" class="hl fld"><span class="hl lin">  660 </span><span class="hl sng"></span></span>
<span id="l_661" class="hl fld"><span class="hl lin">  661 </span><span class="hl sng">          In this mode, the program&#39;s variables do NOT propagate back to the</span></span>
<span id="l_662" class="hl fld"><span class="hl lin">  662 </span><span class="hl sng">          IPython interactive namespace (because they remain in the namespace</span></span>
<span id="l_663" class="hl fld"><span class="hl lin">  663 </span><span class="hl sng">          where the profiler executes them).</span></span>
<span id="l_664" class="hl fld"><span class="hl lin">  664 </span><span class="hl sng"></span></span>
<span id="l_665" class="hl fld"><span class="hl lin">  665 </span><span class="hl sng">          Internally this triggers a call to %prun, see its documentation for</span></span>
<span id="l_666" class="hl fld"><span class="hl lin">  666 </span><span class="hl sng">          details on the options available specifically for profiling.</span></span>
<span id="l_667" class="hl fld"><span class="hl lin">  667 </span><span class="hl sng"></span></span>
<span id="l_668" class="hl fld"><span class="hl lin">  668 </span><span class="hl sng">        There is one special usage for which the text above doesn&#39;t apply:</span></span>
<span id="l_669" class="hl fld"><span class="hl lin">  669 </span><span class="hl sng">        if the filename ends with .ipy[nb], the file is run as ipython script,</span></span>
<span id="l_670" class="hl fld"><span class="hl lin">  670 </span><span class="hl sng">        just as if the commands were written on IPython prompt.</span></span>
<span id="l_671" class="hl fld"><span class="hl lin">  671 </span><span class="hl sng"></span></span>
<span id="l_672" class="hl fld"><span class="hl lin">  672 </span><span class="hl sng">        -m</span></span>
<span id="l_673" class="hl fld"><span class="hl lin">  673 </span><span class="hl sng">          specify module name to load instead of script path. Similar to</span></span>
<span id="l_674" class="hl fld"><span class="hl lin">  674 </span><span class="hl sng">          the -m option for the python interpreter. Use this option last if you</span></span>
<span id="l_675" class="hl fld"><span class="hl lin">  675 </span><span class="hl sng">          want to combine with other</span> <span class="hl ipl">%ru</span><span class="hl sng">n options. Unlike the python interpreter</span></span>
<span id="l_676" class="hl fld"><span class="hl lin">  676 </span><span class="hl sng">          only source modules are allowed no .pyc or .pyo files.</span></span>
<span id="l_677" class="hl fld"><span class="hl lin">  677 </span><span class="hl sng">          For example::</span></span>
<span id="l_678" class="hl fld"><span class="hl lin">  678 </span><span class="hl sng"></span></span>
<span id="l_679" class="hl fld"><span class="hl lin">  679 </span><span class="hl sng"></span>              <span class="hl ipl">%ru</span><span class="hl sng">n -m example</span></span>
<span id="l_680" class="hl fld"><span class="hl lin">  680 </span><span class="hl sng"></span></span>
<span id="l_681" class="hl fld"><span class="hl lin">  681 </span><span class="hl sng">          will run the example module.</span></span>
<span id="l_682" class="hl fld"><span class="hl lin">  682 </span><span class="hl sng"></span></span>
<span id="l_683" class="hl fld"><span class="hl lin">  683 </span><span class="hl sng">        -G</span></span>
<span id="l_684" class="hl fld"><span class="hl lin">  684 </span><span class="hl sng">          disable shell-like glob expansion of arguments.</span></span>
<span id="l_685" class="hl fld"><span class="hl lin">  685 </span><span class="hl sng"></span></span>
<span id="l_686" class="hl fld"><span class="hl lin">  686 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_687" class="hl fld"><span class="hl lin">  687 </span></span>
<span id="l_688" class="hl fld"><span class="hl lin">  688 </span>        <span class="hl slc"># Logic to handle issue #3664</span></span>
<span id="l_689" class="hl fld"><span class="hl lin">  689 </span>        <span class="hl slc"># Add &#39;--&#39; after &#39;-m &lt;module_name&gt;&#39; to ignore additional args passed to a module.</span></span>
<span id="l_690" class="hl fld"><span class="hl lin">  690 </span>        <span class="hl kwa">if</span> <span class="hl sng">&#39;-m&#39;</span> <span class="hl kwa">in</span> parameter_s <span class="hl kwa">and</span> <span class="hl sng">&#39;--&#39;</span> <span class="hl kwa">not in</span> parameter_s<span class="hl opt">:</span></span>
<span id="l_691" class="hl fld"><span class="hl lin">  691 </span>            argv <span class="hl opt">=</span> shlex<span class="hl opt">.</span><span class="hl kwd">split</span><span class="hl opt">(</span>parameter_s<span class="hl opt">,</span> posix<span class="hl opt">=(</span>os<span class="hl opt">.</span>name <span class="hl opt">==</span> <span class="hl sng">&#39;posix&#39;</span><span class="hl opt">))</span></span>
<span id="l_692" class="hl fld"><span class="hl lin">  692 </span>            <span class="hl kwa">for</span> idx<span class="hl opt">,</span> arg <span class="hl kwa">in</span> <span class="hl kwb">enumerate</span><span class="hl opt">(</span>argv<span class="hl opt">):</span></span>
<span id="l_693" class="hl fld"><span class="hl lin">  693 </span>                <span class="hl kwa">if</span> arg <span class="hl kwa">and</span> arg<span class="hl opt">.</span><span class="hl kwd">startswith</span><span class="hl opt">(</span><span class="hl sng">&#39;-&#39;</span><span class="hl opt">)</span> <span class="hl kwa">and</span> arg <span class="hl opt">!=</span> <span class="hl sng">&#39;-&#39;</span><span class="hl opt">:</span></span>
<span id="l_694" class="hl fld"><span class="hl lin">  694 </span>                    <span class="hl kwa">if</span> arg <span class="hl opt">==</span> <span class="hl sng">&#39;-m&#39;</span><span class="hl opt">:</span></span>
<span id="l_695" class="hl fld"><span class="hl lin">  695 </span>                        argv<span class="hl opt">.</span><span class="hl kwd">insert</span><span class="hl opt">(</span>idx <span class="hl opt">+</span> <span class="hl num">2</span><span class="hl opt">,</span> <span class="hl sng">&#39;--&#39;</span><span class="hl opt">)</span></span>
<span id="l_696" class="hl fld"><span class="hl lin">  696 </span>                        <span class="hl kwa">break</span></span>
<span id="l_697" class="hl fld"><span class="hl lin">  697 </span>                <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_698" class="hl fld"><span class="hl lin">  698 </span>                    <span class="hl slc"># Positional arg, break</span></span>
<span id="l_699" class="hl fld"><span class="hl lin">  699 </span>                    <span class="hl kwa">break</span></span>
<span id="l_700" class="hl fld"><span class="hl lin">  700 </span>            parameter_s <span class="hl opt">=</span> <span class="hl sng">&#39; &#39;</span><span class="hl opt">.</span><span class="hl kwd">join</span><span class="hl opt">(</span>shlex<span class="hl opt">.</span><span class="hl kwd">quote</span><span class="hl opt">(</span>arg<span class="hl opt">)</span> <span class="hl kwa">for</span> arg <span class="hl kwa">in</span> argv<span class="hl opt">)</span></span>
<span id="l_701" class="hl fld"><span class="hl lin">  701 </span></span>
<span id="l_702" class="hl fld"><span class="hl lin">  702 </span>        <span class="hl slc"># get arguments and set sys.argv for program to be run.</span></span>
<span id="l_703" class="hl fld"><span class="hl lin">  703 </span>        opts<span class="hl opt">,</span> arg_lst <span class="hl opt">=</span> self<span class="hl opt">.</span><span class="hl kwd">parse_options</span><span class="hl opt">(</span>parameter_s<span class="hl opt">,</span></span>
<span id="l_704" class="hl fld"><span class="hl lin">  704 </span>                                           <span class="hl sng">&#39;nidtN:b:pD:l:rs:T:em:G&#39;</span><span class="hl opt">,</span></span>
<span id="l_705" class="hl fld"><span class="hl lin">  705 </span>                                           mode<span class="hl opt">=</span><span class="hl sng">&#39;list&#39;</span><span class="hl opt">,</span> list_all<span class="hl opt">=</span><span class="hl num">1</span><span class="hl opt">)</span></span>
<span id="l_706" class="hl fld"><span class="hl lin">  706 </span>        <span class="hl kwa">if</span> <span class="hl sng">&quot;m&quot;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_707" class="hl fld"><span class="hl lin">  707 </span>            modulename <span class="hl opt">=</span> opts<span class="hl opt">[</span><span class="hl sng">&quot;m&quot;</span><span class="hl opt">][</span><span class="hl num">0</span><span class="hl opt">]</span></span>
<span id="l_708" class="hl fld"><span class="hl lin">  708 </span>            modpath <span class="hl opt">=</span> <span class="hl kwd">find_mod</span><span class="hl opt">(</span>modulename<span class="hl opt">)</span></span>
<span id="l_709" class="hl fld"><span class="hl lin">  709 </span>            <span class="hl kwa">if</span> modpath <span class="hl kwa">is None</span><span class="hl opt">:</span></span>
<span id="l_710" class="hl fld"><span class="hl lin">  710 </span>                msg <span class="hl opt">=</span> <span class="hl sng">&#39;</span><span class="hl ipl">%r</span> <span class="hl sng">is not a valid modulename on sys.path&#39;</span><span class="hl opt">%</span>modulename</span>
<span id="l_711" class="hl fld"><span class="hl lin">  711 </span>                <span class="hl kwa">raise</span> <span class="hl kwc">Exception</span><span class="hl opt">(</span>msg<span class="hl opt">)</span></span>
<span id="l_712" class="hl fld"><span class="hl lin">  712 </span>            arg_lst <span class="hl opt">= [</span>modpath<span class="hl opt">] +</span> arg_lst</span>
<span id="l_713" class="hl fld"><span class="hl lin">  713 </span>        <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_714" class="hl fld"><span class="hl lin">  714 </span>            fpath <span class="hl opt">=</span> <span class="hl kwa">None</span> <span class="hl slc"># initialize to make sure fpath is in scope later</span></span>
<span id="l_715" class="hl fld"><span class="hl lin">  715 </span>            fpath <span class="hl opt">=</span> arg_lst<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">]</span></span>
<span id="l_716" class="hl fld"><span class="hl lin">  716 </span>            filename <span class="hl opt">=</span> <span class="hl kwd">file_finder</span><span class="hl opt">(</span>fpath<span class="hl opt">)</span></span>
<span id="l_717" class="hl fld"><span class="hl lin">  717 </span>        <span class="hl kwa">except</span> <span class="hl kwc">IndexError</span> <span class="hl kwa">as</span> e<span class="hl opt">:</span></span>
<span id="l_718" class="hl fld"><span class="hl lin">  718 </span>            msg <span class="hl opt">=</span> <span class="hl sng">&#39;you must provide at least a filename.&#39;</span></span>
<span id="l_719" class="hl fld"><span class="hl lin">  719 </span>            <span class="hl kwa">raise</span> <span class="hl kwc">Exception</span><span class="hl opt">(</span>msg<span class="hl opt">)</span> <span class="hl kwa">from</span> e</span>
<span id="l_720" class="hl fld"><span class="hl lin">  720 </span>        <span class="hl kwa">except</span> <span class="hl kwc">IOError</span> <span class="hl kwa">as</span> e<span class="hl opt">:</span></span>
<span id="l_721" class="hl fld"><span class="hl lin">  721 </span>            <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_722" class="hl fld"><span class="hl lin">  722 </span>                msg <span class="hl opt">=</span> <span class="hl kwb">str</span><span class="hl opt">(</span>e<span class="hl opt">)</span></span>
<span id="l_723" class="hl fld"><span class="hl lin">  723 </span>            <span class="hl kwa">except</span> <span class="hl kwc">UnicodeError</span><span class="hl opt">:</span></span>
<span id="l_724" class="hl fld"><span class="hl lin">  724 </span>                msg <span class="hl opt">=</span> e<span class="hl opt">.</span>message</span>
<span id="l_725" class="hl fld"><span class="hl lin">  725 </span>            <span class="hl kwa">if</span> os<span class="hl opt">.</span>name <span class="hl opt">==</span> <span class="hl sng">&#39;nt&#39;</span> <span class="hl kwa">and</span> re<span class="hl opt">.</span><span class="hl kwd">match</span><span class="hl opt">(</span>r<span class="hl sng">&quot;^&#39;.*&#39;$&quot;</span><span class="hl opt">,</span>fpath<span class="hl opt">):</span></span>
<span id="l_726" class="hl fld"><span class="hl lin">  726 </span>                <span class="hl kwd">warn</span><span class="hl opt">(</span><span class="hl sng">&#39;For Windows, use double quotes to wrap a filename:</span> <span class="hl ipl">%ru</span><span class="hl sng">n &quot;mypath</span><span class="hl esc">\\</span><span class="hl sng">myfile.py&quot;&#39;</span><span class="hl opt">)</span></span>
<span id="l_727" class="hl fld"><span class="hl lin">  727 </span>            <span class="hl kwa">raise</span> <span class="hl kwc">Exception</span><span class="hl opt">(</span>msg<span class="hl opt">)</span> <span class="hl kwa">from</span> e</span>
<span id="l_728" class="hl fld"><span class="hl lin">  728 </span>        <span class="hl kwa">except</span> <span class="hl kwc">TypeError</span><span class="hl opt">:</span></span>
<span id="l_729" class="hl fld"><span class="hl lin">  729 </span>            <span class="hl kwa">if</span> fpath <span class="hl kwa">in</span> sys<span class="hl opt">.</span>meta_path<span class="hl opt">:</span></span>
<span id="l_730" class="hl fld"><span class="hl lin">  730 </span>                filename <span class="hl opt">=</span> <span class="hl sng">&quot;&quot;</span></span>
<span id="l_731" class="hl fld"><span class="hl lin">  731 </span>            <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_732" class="hl fld"><span class="hl lin">  732 </span>                <span class="hl kwa">raise</span></span>
<span id="l_733" class="hl fld"><span class="hl lin">  733 </span></span>
<span id="l_734" class="hl fld"><span class="hl lin">  734 </span>        <span class="hl kwa">if</span> filename<span class="hl opt">.</span><span class="hl kwd">lower</span><span class="hl opt">().</span><span class="hl kwd">endswith</span><span class="hl opt">((</span><span class="hl sng">&#39;.ipy&#39;</span><span class="hl opt">,</span> <span class="hl sng">&#39;.ipynb&#39;</span><span class="hl opt">)):</span></span>
<span id="l_735" class="hl fld"><span class="hl lin">  735 </span>            <span class="hl kwa">with</span> <span class="hl kwd">preserve_keys</span><span class="hl opt">(</span>self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">,</span> <span class="hl sng">&#39;__file__&#39;</span><span class="hl opt">):</span></span>
<span id="l_736" class="hl fld"><span class="hl lin">  736 </span>                self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">[</span><span class="hl sng">&#39;__file__&#39;</span><span class="hl opt">] =</span> filename</span>
<span id="l_737" class="hl fld"><span class="hl lin">  737 </span>                self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">safe_execfile_ipy</span><span class="hl opt">(</span>filename<span class="hl opt">,</span> raise_exceptions<span class="hl opt">=</span><span class="hl kwa">True</span><span class="hl opt">)</span></span>
<span id="l_738" class="hl fld"><span class="hl lin">  738 </span>            <span class="hl kwa">return</span></span>
<span id="l_739" class="hl fld"><span class="hl lin">  739 </span></span>
<span id="l_740" class="hl fld"><span class="hl lin">  740 </span>        <span class="hl slc"># Control the response to exit() calls made by the script being run</span></span>
<span id="l_741" class="hl fld"><span class="hl lin">  741 </span>        exit_ignore <span class="hl opt">=</span> <span class="hl sng">&#39;e&#39;</span> <span class="hl kwa">in</span> opts</span>
<span id="l_742" class="hl fld"><span class="hl lin">  742 </span></span>
<span id="l_743" class="hl fld"><span class="hl lin">  743 </span>        <span class="hl slc"># Make sure that the running script gets a proper sys.argv as if it</span></span>
<span id="l_744" class="hl fld"><span class="hl lin">  744 </span>        <span class="hl slc"># were run from a system shell.</span></span>
<span id="l_745" class="hl fld"><span class="hl lin">  745 </span>        save_argv <span class="hl opt">=</span> sys<span class="hl opt">.</span>argv <span class="hl slc"># save it for later restoring</span></span>
<span id="l_746" class="hl fld"><span class="hl lin">  746 </span></span>
<span id="l_747" class="hl fld"><span class="hl lin">  747 </span>        <span class="hl kwa">if</span> <span class="hl sng">&#39;G&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_748" class="hl fld"><span class="hl lin">  748 </span>            args <span class="hl opt">=</span> arg_lst<span class="hl opt">[</span><span class="hl num">1</span><span class="hl opt">:]</span></span>
<span id="l_749" class="hl fld"><span class="hl lin">  749 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_750" class="hl fld"><span class="hl lin">  750 </span>            <span class="hl slc"># tilde and glob expansion</span></span>
<span id="l_751" class="hl fld"><span class="hl lin">  751 </span>            args <span class="hl opt">=</span> <span class="hl kwd">shellglob</span><span class="hl opt">(</span><span class="hl kwb">map</span><span class="hl opt">(</span>os<span class="hl opt">.</span>path<span class="hl opt">.</span>expanduser<span class="hl opt">,</span>  arg_lst<span class="hl opt">[</span><span class="hl num">1</span><span class="hl opt">:]))</span></span>
<span id="l_752" class="hl fld"><span class="hl lin">  752 </span></span>
<span id="l_753" class="hl fld"><span class="hl lin">  753 </span>        sys<span class="hl opt">.</span>argv <span class="hl opt">= [</span>filename<span class="hl opt">] +</span> args  <span class="hl slc"># put in the proper filename</span></span>
<span id="l_754" class="hl fld"><span class="hl lin">  754 </span></span>
<span id="l_755" class="hl fld"><span class="hl lin">  755 </span>        <span class="hl kwa">if</span> <span class="hl sng">&#39;n&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_756" class="hl fld"><span class="hl lin">  756 </span>            name <span class="hl opt">=</span> <span class="hl kwd">Path</span><span class="hl opt">(</span>filename<span class="hl opt">).</span>stem</span>
<span id="l_757" class="hl fld"><span class="hl lin">  757 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_758" class="hl fld"><span class="hl lin">  758 </span>            name <span class="hl opt">=</span> <span class="hl sng">&#39;__main__&#39;</span></span>
<span id="l_759" class="hl fld"><span class="hl lin">  759 </span></span>
<span id="l_760" class="hl fld"><span class="hl lin">  760 </span>        <span class="hl kwa">if</span> <span class="hl sng">&#39;i&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_761" class="hl fld"><span class="hl lin">  761 </span>            <span class="hl slc"># Run in user&#39;s interactive namespace</span></span>
<span id="l_762" class="hl fld"><span class="hl lin">  762 </span>            prog_ns <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns</span>
<span id="l_763" class="hl fld"><span class="hl lin">  763 </span>            __name__save <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">[</span><span class="hl sng">&#39;__name__&#39;</span><span class="hl opt">]</span></span>
<span id="l_764" class="hl fld"><span class="hl lin">  764 </span>            prog_ns<span class="hl opt">[</span><span class="hl sng">&#39;__name__&#39;</span><span class="hl opt">] =</span> name</span>
<span id="l_765" class="hl fld"><span class="hl lin">  765 </span>            main_mod <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_module</span>
<span id="l_766" class="hl fld"><span class="hl lin">  766 </span></span>
<span id="l_767" class="hl fld"><span class="hl lin">  767 </span>            <span class="hl slc"># Since &#39;%run foo&#39; emulates &#39;python foo.py&#39; at the cmd line, we must</span></span>
<span id="l_768" class="hl fld"><span class="hl lin">  768 </span>            <span class="hl slc"># set the __file__ global in the script&#39;s namespace</span></span>
<span id="l_769" class="hl fld"><span class="hl lin">  769 </span>            <span class="hl slc"># TK: Is this necessary in interactive mode?</span></span>
<span id="l_770" class="hl fld"><span class="hl lin">  770 </span>            prog_ns<span class="hl opt">[</span><span class="hl sng">&#39;__file__&#39;</span><span class="hl opt">] =</span> filename</span>
<span id="l_771" class="hl fld"><span class="hl lin">  771 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_772" class="hl fld"><span class="hl lin">  772 </span>            <span class="hl slc"># Run in a fresh, empty namespace</span></span>
<span id="l_773" class="hl fld"><span class="hl lin">  773 </span></span>
<span id="l_774" class="hl fld"><span class="hl lin">  774 </span>            <span class="hl slc"># The shell MUST hold a reference to prog_ns so after %run</span></span>
<span id="l_775" class="hl fld"><span class="hl lin">  775 </span>            <span class="hl slc"># exits, the python deletion mechanism doesn&#39;t zero it out</span></span>
<span id="l_776" class="hl fld"><span class="hl lin">  776 </span>            <span class="hl slc"># (leaving dangling references). See interactiveshell for details</span></span>
<span id="l_777" class="hl fld"><span class="hl lin">  777 </span>            main_mod <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">new_main_mod</span><span class="hl opt">(</span>filename<span class="hl opt">,</span> name<span class="hl opt">)</span></span>
<span id="l_778" class="hl fld"><span class="hl lin">  778 </span>            prog_ns <span class="hl opt">=</span> main_mod<span class="hl num">.__</span>dict<span class="hl num">__</span></span>
<span id="l_779" class="hl fld"><span class="hl lin">  779 </span></span>
<span id="l_780" class="hl fld"><span class="hl lin">  780 </span>        <span class="hl slc"># pickle fix.  See interactiveshell for an explanation.  But we need to</span></span>
<span id="l_781" class="hl fld"><span class="hl lin">  781 </span>        <span class="hl slc"># make sure that, if we overwrite __main__, we replace it at the end</span></span>
<span id="l_782" class="hl fld"><span class="hl lin">  782 </span>        main_mod_name <span class="hl opt">=</span> prog_ns<span class="hl opt">[</span><span class="hl sng">&#39;__name__&#39;</span><span class="hl opt">]</span></span>
<span id="l_783" class="hl fld"><span class="hl lin">  783 </span></span>
<span id="l_784" class="hl fld"><span class="hl lin">  784 </span>        <span class="hl kwa">if</span> main_mod_name <span class="hl opt">==</span> <span class="hl sng">&#39;__main__&#39;</span><span class="hl opt">:</span></span>
<span id="l_785" class="hl fld"><span class="hl lin">  785 </span>            restore_main <span class="hl opt">=</span> sys<span class="hl opt">.</span>modules<span class="hl opt">[</span><span class="hl sng">&#39;__main__&#39;</span><span class="hl opt">]</span></span>
<span id="l_786" class="hl fld"><span class="hl lin">  786 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_787" class="hl fld"><span class="hl lin">  787 </span>            restore_main <span class="hl opt">=</span> <span class="hl kwa">False</span></span>
<span id="l_788" class="hl fld"><span class="hl lin">  788 </span></span>
<span id="l_789" class="hl fld"><span class="hl lin">  789 </span>        <span class="hl slc"># This needs to be undone at the end to prevent holding references to</span></span>
<span id="l_790" class="hl fld"><span class="hl lin">  790 </span>        <span class="hl slc"># every single object ever created.</span></span>
<span id="l_791" class="hl fld"><span class="hl lin">  791 </span>        sys<span class="hl opt">.</span>modules<span class="hl opt">[</span>main_mod_name<span class="hl opt">] =</span> main_mod</span>
<span id="l_792" class="hl fld"><span class="hl lin">  792 </span></span>
<span id="l_793" class="hl fld"><span class="hl lin">  793 </span>        <span class="hl kwa">if</span> <span class="hl sng">&#39;p&#39;</span> <span class="hl kwa">in</span> opts <span class="hl kwa">or</span> <span class="hl sng">&#39;d&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_794" class="hl fld"><span class="hl lin">  794 </span>            <span class="hl kwa">if</span> <span class="hl sng">&#39;m&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_795" class="hl fld"><span class="hl lin">  795 </span>                code <span class="hl opt">=</span> <span class="hl sng">&#39;run_module(modulename, prog_ns)&#39;</span></span>
<span id="l_796" class="hl fld"><span class="hl lin">  796 </span>                code_ns <span class="hl opt">= {</span></span>
<span id="l_797" class="hl fld"><span class="hl lin">  797 </span>                    <span class="hl sng">&#39;run_module&#39;</span><span class="hl opt">:</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>safe_run_module<span class="hl opt">,</span></span>
<span id="l_798" class="hl fld"><span class="hl lin">  798 </span>                    <span class="hl sng">&#39;prog_ns&#39;</span><span class="hl opt">:</span> prog_ns<span class="hl opt">,</span></span>
<span id="l_799" class="hl fld"><span class="hl lin">  799 </span>                    <span class="hl sng">&#39;modulename&#39;</span><span class="hl opt">:</span> modulename<span class="hl opt">,</span></span>
<span id="l_800" class="hl fld"><span class="hl lin">  800 </span>                <span class="hl opt">}</span></span>
<span id="l_801" class="hl fld"><span class="hl lin">  801 </span>            <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_802" class="hl fld"><span class="hl lin">  802 </span>                <span class="hl kwa">if</span> <span class="hl sng">&#39;d&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_803" class="hl fld"><span class="hl lin">  803 </span>                    <span class="hl slc"># allow exceptions to raise in debug mode</span></span>
<span id="l_804" class="hl fld"><span class="hl lin">  804 </span>                    code <span class="hl opt">=</span> <span class="hl sng">&#39;execfile(filename, prog_ns, raise_exceptions=True)&#39;</span></span>
<span id="l_805" class="hl fld"><span class="hl lin">  805 </span>                <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_806" class="hl fld"><span class="hl lin">  806 </span>                    code <span class="hl opt">=</span> <span class="hl sng">&#39;execfile(filename, prog_ns)&#39;</span></span>
<span id="l_807" class="hl fld"><span class="hl lin">  807 </span>                code_ns <span class="hl opt">= {</span></span>
<span id="l_808" class="hl fld"><span class="hl lin">  808 </span>                    <span class="hl sng">&#39;execfile&#39;</span><span class="hl opt">:</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>safe_execfile<span class="hl opt">,</span></span>
<span id="l_809" class="hl fld"><span class="hl lin">  809 </span>                    <span class="hl sng">&#39;prog_ns&#39;</span><span class="hl opt">:</span> prog_ns<span class="hl opt">,</span></span>
<span id="l_810" class="hl fld"><span class="hl lin">  810 </span>                    <span class="hl sng">&#39;filename&#39;</span><span class="hl opt">:</span> <span class="hl kwd">get_py_filename</span><span class="hl opt">(</span>filename<span class="hl opt">),</span></span>
<span id="l_811" class="hl fld"><span class="hl lin">  811 </span>                <span class="hl opt">}</span></span>
<span id="l_812" class="hl fld"><span class="hl lin">  812 </span></span>
<span id="l_813" class="hl fld"><span class="hl lin">  813 </span>        <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_814" class="hl fld"><span class="hl lin">  814 </span>            stats <span class="hl opt">=</span> <span class="hl kwa">None</span></span>
<span id="l_815" class="hl fld"><span class="hl lin">  815 </span>            <span class="hl kwa">if</span> <span class="hl sng">&#39;p&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_816" class="hl fld"><span class="hl lin">  816 </span>                stats <span class="hl opt">=</span> self<span class="hl num">._</span>run<span class="hl num">_</span>with<span class="hl num">_</span>profiler<span class="hl opt">(</span>code<span class="hl opt">,</span> opts<span class="hl opt">,</span> code_ns<span class="hl opt">)</span></span>
<span id="l_817" class="hl fld"><span class="hl lin">  817 </span>            <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_818" class="hl fld"><span class="hl lin">  818 </span>                <span class="hl kwa">if</span> <span class="hl sng">&#39;d&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_819" class="hl fld"><span class="hl lin">  819 </span>                    bp_file<span class="hl opt">,</span> bp_line <span class="hl opt">=</span> <span class="hl kwd">parse_breakpoint</span><span class="hl opt">(</span></span>
<span id="l_820" class="hl fld"><span class="hl lin">  820 </span>                        opts<span class="hl opt">.</span><span class="hl kwd">get</span><span class="hl opt">(</span><span class="hl sng">&#39;b&#39;</span><span class="hl opt">, [</span><span class="hl sng">&#39;1&#39;</span><span class="hl opt">])[</span><span class="hl num">0</span><span class="hl opt">],</span> filename<span class="hl opt">)</span></span>
<span id="l_821" class="hl fld"><span class="hl lin">  821 </span>                    self<span class="hl num">._</span>run<span class="hl num">_</span>with<span class="hl num">_</span>debugger<span class="hl opt">(</span></span>
<span id="l_822" class="hl fld"><span class="hl lin">  822 </span>                        code<span class="hl opt">,</span> code_ns<span class="hl opt">,</span> filename<span class="hl opt">,</span> bp_line<span class="hl opt">,</span> bp_file<span class="hl opt">)</span></span>
<span id="l_823" class="hl fld"><span class="hl lin">  823 </span>                <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_824" class="hl fld"><span class="hl lin">  824 </span>                    <span class="hl kwa">if</span> <span class="hl sng">&#39;m&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_825" class="hl fld"><span class="hl lin">  825 </span>                        <span class="hl kwa">def</span> <span class="hl kwd">run</span><span class="hl opt">():</span></span>
<span id="l_826" class="hl fld"><span class="hl lin">  826 </span>                            self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">safe_run_module</span><span class="hl opt">(</span>modulename<span class="hl opt">,</span> prog_ns<span class="hl opt">)</span></span>
<span id="l_827" class="hl fld"><span class="hl lin">  827 </span>                    <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_828" class="hl fld"><span class="hl lin">  828 </span>                        <span class="hl kwa">if</span> runner <span class="hl kwa">is None</span><span class="hl opt">:</span></span>
<span id="l_829" class="hl fld"><span class="hl lin">  829 </span>                            runner <span class="hl opt">=</span> self<span class="hl opt">.</span>default_runner</span>
<span id="l_830" class="hl fld"><span class="hl lin">  830 </span>                        <span class="hl kwa">if</span> runner <span class="hl kwa">is None</span><span class="hl opt">:</span></span>
<span id="l_831" class="hl fld"><span class="hl lin">  831 </span>                            runner <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>safe_execfile</span>
<span id="l_832" class="hl fld"><span class="hl lin">  832 </span></span>
<span id="l_833" class="hl fld"><span class="hl lin">  833 </span>                        <span class="hl kwa">def</span> <span class="hl kwd">run</span><span class="hl opt">():</span></span>
<span id="l_834" class="hl fld"><span class="hl lin">  834 </span>                            <span class="hl kwd">runner</span><span class="hl opt">(</span>filename<span class="hl opt">,</span> prog_ns<span class="hl opt">,</span> prog_ns<span class="hl opt">,</span></span>
<span id="l_835" class="hl fld"><span class="hl lin">  835 </span>                                    exit_ignore<span class="hl opt">=</span>exit_ignore<span class="hl opt">)</span></span>
<span id="l_836" class="hl fld"><span class="hl lin">  836 </span></span>
<span id="l_837" class="hl fld"><span class="hl lin">  837 </span>                    <span class="hl kwa">if</span> <span class="hl sng">&#39;t&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_838" class="hl fld"><span class="hl lin">  838 </span>                        <span class="hl slc"># timed execution</span></span>
<span id="l_839" class="hl fld"><span class="hl lin">  839 </span>                        <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_840" class="hl fld"><span class="hl lin">  840 </span>                            nruns <span class="hl opt">=</span> <span class="hl kwb">int</span><span class="hl opt">(</span>opts<span class="hl opt">[</span><span class="hl sng">&#39;N&#39;</span><span class="hl opt">][</span><span class="hl num">0</span><span class="hl opt">])</span></span>
<span id="l_841" class="hl fld"><span class="hl lin">  841 </span>                            <span class="hl kwa">if</span> nruns <span class="hl opt">&lt;</span> <span class="hl num">1</span><span class="hl opt">:</span></span>
<span id="l_842" class="hl fld"><span class="hl lin">  842 </span>                                <span class="hl kwd">error</span><span class="hl opt">(</span><span class="hl sng">&#39;Number of runs must be &gt;=1&#39;</span><span class="hl opt">)</span></span>
<span id="l_843" class="hl fld"><span class="hl lin">  843 </span>                                <span class="hl kwa">return</span></span>
<span id="l_844" class="hl fld"><span class="hl lin">  844 </span>                        <span class="hl kwa">except</span> <span class="hl opt">(</span><span class="hl kwc">KeyError</span><span class="hl opt">):</span></span>
<span id="l_845" class="hl fld"><span class="hl lin">  845 </span>                            nruns <span class="hl opt">=</span> <span class="hl num">1</span></span>
<span id="l_846" class="hl fld"><span class="hl lin">  846 </span>                        self<span class="hl num">._</span>run<span class="hl num">_</span>with<span class="hl num">_</span>timing<span class="hl opt">(</span>run<span class="hl opt">,</span> nruns<span class="hl opt">)</span></span>
<span id="l_847" class="hl fld"><span class="hl lin">  847 </span>                    <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_848" class="hl fld"><span class="hl lin">  848 </span>                        <span class="hl slc"># regular execution</span></span>
<span id="l_849" class="hl fld"><span class="hl lin">  849 </span>                        <span class="hl kwd">run</span><span class="hl opt">()</span></span>
<span id="l_850" class="hl fld"><span class="hl lin">  850 </span></span>
<span id="l_851" class="hl fld"><span class="hl lin">  851 </span>            <span class="hl kwa">if</span> <span class="hl sng">&#39;i&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">:</span></span>
<span id="l_852" class="hl fld"><span class="hl lin">  852 </span>                self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">[</span><span class="hl sng">&#39;__name__&#39;</span><span class="hl opt">] =</span> __name__save</span>
<span id="l_853" class="hl fld"><span class="hl lin">  853 </span>            <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_854" class="hl fld"><span class="hl lin">  854 </span>                <span class="hl slc"># update IPython interactive namespace</span></span>
<span id="l_855" class="hl fld"><span class="hl lin">  855 </span></span>
<span id="l_856" class="hl fld"><span class="hl lin">  856 </span>                <span class="hl slc"># Some forms of read errors on the file may mean the</span></span>
<span id="l_857" class="hl fld"><span class="hl lin">  857 </span>                <span class="hl slc"># __name__ key was never set; using pop we don&#39;t have to</span></span>
<span id="l_858" class="hl fld"><span class="hl lin">  858 </span>                <span class="hl slc"># worry about a possible KeyError.</span></span>
<span id="l_859" class="hl fld"><span class="hl lin">  859 </span>                prog_ns<span class="hl opt">.</span><span class="hl kwd">pop</span><span class="hl opt">(</span><span class="hl sng">&#39;__name__&#39;</span><span class="hl opt">,</span> <span class="hl kwa">None</span><span class="hl opt">)</span></span>
<span id="l_860" class="hl fld"><span class="hl lin">  860 </span></span>
<span id="l_861" class="hl fld"><span class="hl lin">  861 </span>                <span class="hl kwa">with</span> <span class="hl kwd">preserve_keys</span><span class="hl opt">(</span>self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">,</span> <span class="hl sng">&#39;__file__&#39;</span><span class="hl opt">):</span></span>
<span id="l_862" class="hl fld"><span class="hl lin">  862 </span>                    self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">.</span><span class="hl kwd">update</span><span class="hl opt">(</span>prog_ns<span class="hl opt">)</span></span>
<span id="l_863" class="hl fld"><span class="hl lin">  863 </span>        <span class="hl kwa">finally</span><span class="hl opt">:</span></span>
<span id="l_864" class="hl fld"><span class="hl lin">  864 </span>            <span class="hl slc"># It&#39;s a bit of a mystery why, but __builtins__ can change from</span></span>
<span id="l_865" class="hl fld"><span class="hl lin">  865 </span>            <span class="hl slc"># being a module to becoming a dict missing some key data after</span></span>
<span id="l_866" class="hl fld"><span class="hl lin">  866 </span>            <span class="hl slc"># %run.  As best I can see, this is NOT something IPython is doing</span></span>
<span id="l_867" class="hl fld"><span class="hl lin">  867 </span>            <span class="hl slc"># at all, and similar problems have been reported before:</span></span>
<span id="l_868" class="hl fld"><span class="hl lin">  868 </span>            <span class="hl slc"># http://coding.derkeiler.com/Archive/Python/comp.lang.python/2004-10/0188.html</span></span>
<span id="l_869" class="hl fld"><span class="hl lin">  869 </span>            <span class="hl slc"># Since this seems to be done by the interpreter itself, the best</span></span>
<span id="l_870" class="hl fld"><span class="hl lin">  870 </span>            <span class="hl slc"># we can do is to at least restore __builtins__ for the user on</span></span>
<span id="l_871" class="hl fld"><span class="hl lin">  871 </span>            <span class="hl slc"># exit.</span></span>
<span id="l_872" class="hl fld"><span class="hl lin">  872 </span>            self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">[</span><span class="hl sng">&#39;__builtins__&#39;</span><span class="hl opt">] =</span> builtin_mod</span>
<span id="l_873" class="hl fld"><span class="hl lin">  873 </span></span>
<span id="l_874" class="hl fld"><span class="hl lin">  874 </span>            <span class="hl slc"># Ensure key global structures are restored</span></span>
<span id="l_875" class="hl fld"><span class="hl lin">  875 </span>            sys<span class="hl opt">.</span>argv <span class="hl opt">=</span> save_argv</span>
<span id="l_876" class="hl fld"><span class="hl lin">  876 </span>            <span class="hl kwa">if</span> restore_main<span class="hl opt">:</span></span>
<span id="l_877" class="hl fld"><span class="hl lin">  877 </span>                sys<span class="hl opt">.</span>modules<span class="hl opt">[</span><span class="hl sng">&#39;__main__&#39;</span><span class="hl opt">] =</span> restore_main</span>
<span id="l_878" class="hl fld"><span class="hl lin">  878 </span>                <span class="hl kwa">if</span> <span class="hl sng">&#39;__mp_main__&#39;</span> <span class="hl kwa">in</span> sys<span class="hl opt">.</span>modules<span class="hl opt">:</span></span>
<span id="l_879" class="hl fld"><span class="hl lin">  879 </span>                    sys<span class="hl opt">.</span>modules<span class="hl opt">[</span><span class="hl sng">&#39;__mp_main__&#39;</span><span class="hl opt">] =</span> restore_main</span>
<span id="l_880" class="hl fld"><span class="hl lin">  880 </span>            <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_881" class="hl fld"><span class="hl lin">  881 </span>                <span class="hl slc"># Remove from sys.modules the reference to main_mod we&#39;d</span></span>
<span id="l_882" class="hl fld"><span class="hl lin">  882 </span>                <span class="hl slc"># added.  Otherwise it will trap references to objects</span></span>
<span id="l_883" class="hl fld"><span class="hl lin">  883 </span>                <span class="hl slc"># contained therein.</span></span>
<span id="l_884" class="hl fld"><span class="hl lin">  884 </span>                <span class="hl kwa">del</span> sys<span class="hl opt">.</span>modules<span class="hl opt">[</span>main_mod_name<span class="hl opt">]</span></span>
<span id="l_885" class="hl fld"><span class="hl lin">  885 </span></span>
<span id="l_886" class="hl fld"><span class="hl lin">  886 </span>        <span class="hl kwa">return</span> stats</span>
<span id="l_887" class="hl fld"><span class="hl lin">  887 </span></span>
<span id="l_888" class="hl fld"><span class="hl lin">  888 </span>    <span class="hl kwa">def</span> <span class="hl kwd">_run_with_debugger</span><span class="hl opt">(</span></span>
<span id="l_889" class="hl fld"><span class="hl lin">  889 </span>        self<span class="hl opt">,</span> code<span class="hl opt">,</span> code_ns<span class="hl opt">,</span> filename<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">,</span> bp_line<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">,</span> bp_file<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">,</span> local_ns<span class="hl opt">=</span><span class="hl kwa">None</span></span>
<span id="l_890" class="hl fld"><span class="hl lin">  890 </span>    <span class="hl opt">):</span></span>
<span id="l_891" class="hl fld"><span class="hl lin">  891 </span>        <span class="hl sng">&quot;&quot;&quot;</span></span>
<span id="l_892" class="hl fld"><span class="hl lin">  892 </span><span class="hl sng">        Run `code` in debugger with a break point.</span></span>
<span id="l_893" class="hl fld"><span class="hl lin">  893 </span><span class="hl sng"></span></span>
<span id="l_894" class="hl fld"><span class="hl lin">  894 </span><span class="hl sng">        Parameters</span></span>
<span id="l_895" class="hl fld"><span class="hl lin">  895 </span><span class="hl sng">        ----------</span></span>
<span id="l_896" class="hl fld"><span class="hl lin">  896 </span><span class="hl sng">        code : str</span></span>
<span id="l_897" class="hl fld"><span class="hl lin">  897 </span><span class="hl sng">            Code to execute.</span></span>
<span id="l_898" class="hl fld"><span class="hl lin">  898 </span><span class="hl sng">        code_ns : dict</span></span>
<span id="l_899" class="hl fld"><span class="hl lin">  899 </span><span class="hl sng">            A namespace in which `code` is executed.</span></span>
<span id="l_900" class="hl fld"><span class="hl lin">  900 </span><span class="hl sng">        filename : str</span></span>
<span id="l_901" class="hl fld"><span class="hl lin">  901 </span><span class="hl sng">            `code` is ran as if it is in `filename`.</span></span>
<span id="l_902" class="hl fld"><span class="hl lin">  902 </span><span class="hl sng">        bp_line : int, optional</span></span>
<span id="l_903" class="hl fld"><span class="hl lin">  903 </span><span class="hl sng">            Line number of the break point.</span></span>
<span id="l_904" class="hl fld"><span class="hl lin">  904 </span><span class="hl sng">        bp_file : str, optional</span></span>
<span id="l_905" class="hl fld"><span class="hl lin">  905 </span><span class="hl sng">            Path to the file in which break point is specified.</span></span>
<span id="l_906" class="hl fld"><span class="hl lin">  906 </span><span class="hl sng">            `filename` is used if not given.</span></span>
<span id="l_907" class="hl fld"><span class="hl lin">  907 </span><span class="hl sng">        local_ns : dict, optional</span></span>
<span id="l_908" class="hl fld"><span class="hl lin">  908 </span><span class="hl sng">            A local namespace in which `code` is executed.</span></span>
<span id="l_909" class="hl fld"><span class="hl lin">  909 </span><span class="hl sng"></span></span>
<span id="l_910" class="hl fld"><span class="hl lin">  910 </span><span class="hl sng">        Raises</span></span>
<span id="l_911" class="hl fld"><span class="hl lin">  911 </span><span class="hl sng">        ------</span></span>
<span id="l_912" class="hl fld"><span class="hl lin">  912 </span><span class="hl sng">        UsageError</span></span>
<span id="l_913" class="hl fld"><span class="hl lin">  913 </span><span class="hl sng">            If the break point given by `bp_line` is not valid.</span></span>
<span id="l_914" class="hl fld"><span class="hl lin">  914 </span><span class="hl sng"></span></span>
<span id="l_915" class="hl fld"><span class="hl lin">  915 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_916" class="hl fld"><span class="hl lin">  916 </span>        deb <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>InteractiveTB<span class="hl opt">.</span>pdb</span>
<span id="l_917" class="hl fld"><span class="hl lin">  917 </span>        <span class="hl kwa">if not</span> deb<span class="hl opt">:</span></span>
<span id="l_918" class="hl fld"><span class="hl lin">  918 </span>            self<span class="hl opt">.</span>shell<span class="hl opt">.</span>InteractiveTB<span class="hl opt">.</span>pdb <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>InteractiveTB<span class="hl opt">.</span><span class="hl kwd">debugger_cls</span><span class="hl opt">()</span></span>
<span id="l_919" class="hl fld"><span class="hl lin">  919 </span>            deb <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>InteractiveTB<span class="hl opt">.</span>pdb</span>
<span id="l_920" class="hl fld"><span class="hl lin">  920 </span></span>
<span id="l_921" class="hl fld"><span class="hl lin">  921 </span>        <span class="hl slc"># deb.checkline() fails if deb.curframe exists but is None; it can</span></span>
<span id="l_922" class="hl fld"><span class="hl lin">  922 </span>        <span class="hl slc"># handle it not existing. https://github.com/ipython/ipython/issues/10028</span></span>
<span id="l_923" class="hl fld"><span class="hl lin">  923 </span>        <span class="hl kwa">if</span> <span class="hl kwb">hasattr</span><span class="hl opt">(</span>deb<span class="hl opt">,</span> <span class="hl sng">&#39;curframe&#39;</span><span class="hl opt">):</span></span>
<span id="l_924" class="hl fld"><span class="hl lin">  924 </span>            <span class="hl kwa">del</span> deb<span class="hl opt">.</span>curframe</span>
<span id="l_925" class="hl fld"><span class="hl lin">  925 </span></span>
<span id="l_926" class="hl fld"><span class="hl lin">  926 </span>        <span class="hl slc"># reset Breakpoint state, which is moronically kept</span></span>
<span id="l_927" class="hl fld"><span class="hl lin">  927 </span>        <span class="hl slc"># in a class</span></span>
<span id="l_928" class="hl fld"><span class="hl lin">  928 </span>        bdb<span class="hl opt">.</span>Breakpoint<span class="hl opt">.</span>next <span class="hl opt">=</span> <span class="hl num">1</span></span>
<span id="l_929" class="hl fld"><span class="hl lin">  929 </span>        bdb<span class="hl opt">.</span>Breakpoint<span class="hl opt">.</span>bplist <span class="hl opt">= {}</span></span>
<span id="l_930" class="hl fld"><span class="hl lin">  930 </span>        bdb<span class="hl opt">.</span>Breakpoint<span class="hl opt">.</span>bpbynumber <span class="hl opt">= [</span><span class="hl kwa">None</span><span class="hl opt">]</span></span>
<span id="l_931" class="hl fld"><span class="hl lin">  931 </span>        deb<span class="hl opt">.</span><span class="hl kwd">clear_all_breaks</span><span class="hl opt">()</span></span>
<span id="l_932" class="hl fld"><span class="hl lin">  932 </span>        <span class="hl kwa">if</span> bp_line <span class="hl kwa">is not None</span><span class="hl opt">:</span></span>
<span id="l_933" class="hl fld"><span class="hl lin">  933 </span>            <span class="hl slc"># Set an initial breakpoint to stop execution</span></span>
<span id="l_934" class="hl fld"><span class="hl lin">  934 </span>            maxtries <span class="hl opt">=</span> <span class="hl num">10</span></span>
<span id="l_935" class="hl fld"><span class="hl lin">  935 </span>            bp_file <span class="hl opt">=</span> bp_file <span class="hl kwa">or</span> filename</span>
<span id="l_936" class="hl fld"><span class="hl lin">  936 </span>            checkline <span class="hl opt">=</span> deb<span class="hl opt">.</span><span class="hl kwd">checkline</span><span class="hl opt">(</span>bp_file<span class="hl opt">,</span> bp_line<span class="hl opt">)</span></span>
<span id="l_937" class="hl fld"><span class="hl lin">  937 </span>            <span class="hl kwa">if not</span> checkline<span class="hl opt">:</span></span>
<span id="l_938" class="hl fld"><span class="hl lin">  938 </span>                <span class="hl kwa">for</span> bp <span class="hl kwa">in</span> <span class="hl kwb">range</span><span class="hl opt">(</span>bp_line <span class="hl opt">+</span> <span class="hl num">1</span><span class="hl opt">,</span> bp_line <span class="hl opt">+</span> maxtries <span class="hl opt">+</span> <span class="hl num">1</span><span class="hl opt">):</span></span>
<span id="l_939" class="hl fld"><span class="hl lin">  939 </span>                    <span class="hl kwa">if</span> deb<span class="hl opt">.</span><span class="hl kwd">checkline</span><span class="hl opt">(</span>bp_file<span class="hl opt">,</span> bp<span class="hl opt">):</span></span>
<span id="l_940" class="hl fld"><span class="hl lin">  940 </span>                        <span class="hl kwa">break</span></span>
<span id="l_941" class="hl fld"><span class="hl lin">  941 </span>                <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_942" class="hl fld"><span class="hl lin">  942 </span>                    msg <span class="hl opt">= (</span><span class="hl sng">&quot;</span><span class="hl esc">\n</span><span class="hl sng">I failed to find a valid line to set &quot;</span></span>
<span id="l_943" class="hl fld"><span class="hl lin">  943 </span>                           <span class="hl sng">&quot;a breakpoint</span><span class="hl esc">\n</span><span class="hl sng">&quot;</span></span>
<span id="l_944" class="hl fld"><span class="hl lin">  944 </span>                           <span class="hl sng">&quot;after trying up to line:</span> <span class="hl ipl">%s</span><span class="hl sng">.</span><span class="hl esc">\n</span><span class="hl sng">&quot;</span></span>
<span id="l_945" class="hl fld"><span class="hl lin">  945 </span>                           <span class="hl sng">&quot;Please set a valid breakpoint manually &quot;</span></span>
<span id="l_946" class="hl fld"><span class="hl lin">  946 </span>                           <span class="hl sng">&quot;with the -b option.&quot;</span> <span class="hl opt">%</span> bp<span class="hl opt">)</span></span>
<span id="l_947" class="hl fld"><span class="hl lin">  947 </span>                    <span class="hl kwa">raise</span> <span class="hl kwd">UsageError</span><span class="hl opt">(</span>msg<span class="hl opt">)</span></span>
<span id="l_948" class="hl fld"><span class="hl lin">  948 </span>            <span class="hl slc"># if we find a good linenumber, set the breakpoint</span></span>
<span id="l_949" class="hl fld"><span class="hl lin">  949 </span>            deb<span class="hl opt">.</span><span class="hl kwd">do_break</span><span class="hl opt">(</span><span class="hl sng">&#39;</span><span class="hl ipl">%s</span><span class="hl sng">:</span><span class="hl ipl">%s</span><span class="hl sng">&#39;</span> <span class="hl opt">% (</span>bp_file<span class="hl opt">,</span> bp_line<span class="hl opt">))</span></span>
<span id="l_950" class="hl fld"><span class="hl lin">  950 </span></span>
<span id="l_951" class="hl fld"><span class="hl lin">  951 </span>        <span class="hl kwa">if</span> filename<span class="hl opt">:</span></span>
<span id="l_952" class="hl fld"><span class="hl lin">  952 </span>            <span class="hl slc"># Mimic Pdb._runscript(...)</span></span>
<span id="l_953" class="hl fld"><span class="hl lin">  953 </span>            deb<span class="hl num">._</span>wait<span class="hl num">_</span>for<span class="hl num">_</span>mainpyfile <span class="hl opt">=</span> <span class="hl kwa">True</span></span>
<span id="l_954" class="hl fld"><span class="hl lin">  954 </span>            deb<span class="hl opt">.</span>mainpyfile <span class="hl opt">=</span> deb<span class="hl opt">.</span><span class="hl kwd">canonic</span><span class="hl opt">(</span>filename<span class="hl opt">)</span></span>
<span id="l_955" class="hl fld"><span class="hl lin">  955 </span></span>
<span id="l_956" class="hl fld"><span class="hl lin">  956 </span>        <span class="hl slc"># Start file run</span></span>
<span id="l_957" class="hl fld"><span class="hl lin">  957 </span>        <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;NOTE: Enter &#39;c&#39; at the</span> <span class="hl ipl">%s</span> <span class="hl sng">prompt to continue execution.&quot;</span> <span class="hl opt">%</span> deb<span class="hl opt">.</span>prompt<span class="hl opt">)</span></span>
<span id="l_958" class="hl fld"><span class="hl lin">  958 </span>        <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_959" class="hl fld"><span class="hl lin">  959 </span>            <span class="hl kwa">if</span> filename<span class="hl opt">:</span></span>
<span id="l_960" class="hl fld"><span class="hl lin">  960 </span>                <span class="hl slc"># save filename so it can be used by methods on the deb object</span></span>
<span id="l_961" class="hl fld"><span class="hl lin">  961 </span>                deb<span class="hl num">._</span>exec<span class="hl num">_</span>filename <span class="hl opt">=</span> filename</span>
<span id="l_962" class="hl fld"><span class="hl lin">  962 </span>            <span class="hl kwa">while True</span><span class="hl opt">:</span></span>
<span id="l_963" class="hl fld"><span class="hl lin">  963 </span>                <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_964" class="hl fld"><span class="hl lin">  964 </span>                    trace <span class="hl opt">=</span> sys<span class="hl opt">.</span><span class="hl kwd">gettrace</span><span class="hl opt">()</span></span>
<span id="l_965" class="hl fld"><span class="hl lin">  965 </span>                    deb<span class="hl opt">.</span><span class="hl kwd">run</span><span class="hl opt">(</span>code<span class="hl opt">,</span> code_ns<span class="hl opt">,</span> local_ns<span class="hl opt">)</span></span>
<span id="l_966" class="hl fld"><span class="hl lin">  966 </span>                <span class="hl kwa">except</span> Restart<span class="hl opt">:</span></span>
<span id="l_967" class="hl fld"><span class="hl lin">  967 </span>                    <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;Restarting&quot;</span><span class="hl opt">)</span></span>
<span id="l_968" class="hl fld"><span class="hl lin">  968 </span>                    <span class="hl kwa">if</span> filename<span class="hl opt">:</span></span>
<span id="l_969" class="hl fld"><span class="hl lin">  969 </span>                        deb<span class="hl num">._</span>wait<span class="hl num">_</span>for<span class="hl num">_</span>mainpyfile <span class="hl opt">=</span> <span class="hl kwa">True</span></span>
<span id="l_970" class="hl fld"><span class="hl lin">  970 </span>                        deb<span class="hl opt">.</span>mainpyfile <span class="hl opt">=</span> deb<span class="hl opt">.</span><span class="hl kwd">canonic</span><span class="hl opt">(</span>filename<span class="hl opt">)</span></span>
<span id="l_971" class="hl fld"><span class="hl lin">  971 </span>                    <span class="hl kwa">continue</span></span>
<span id="l_972" class="hl fld"><span class="hl lin">  972 </span>                <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_973" class="hl fld"><span class="hl lin">  973 </span>                    <span class="hl kwa">break</span></span>
<span id="l_974" class="hl fld"><span class="hl lin">  974 </span>                <span class="hl kwa">finally</span><span class="hl opt">:</span></span>
<span id="l_975" class="hl fld"><span class="hl lin">  975 </span>                    sys<span class="hl opt">.</span><span class="hl kwd">settrace</span><span class="hl opt">(</span>trace<span class="hl opt">)</span></span>
<span id="l_976" class="hl fld"><span class="hl lin">  976 </span>            </span>
<span id="l_977" class="hl fld"><span class="hl lin">  977 </span></span>
<span id="l_978" class="hl fld"><span class="hl lin">  978 </span>        <span class="hl kwa">except</span><span class="hl opt">:</span></span>
<span id="l_979" class="hl fld"><span class="hl lin">  979 </span>            etype<span class="hl opt">,</span> value<span class="hl opt">,</span> tb <span class="hl opt">=</span> sys<span class="hl opt">.</span><span class="hl kwd">exc_info</span><span class="hl opt">()</span></span>
<span id="l_980" class="hl fld"><span class="hl lin">  980 </span>            <span class="hl slc"># Skip three frames in the traceback: the %run one,</span></span>
<span id="l_981" class="hl fld"><span class="hl lin">  981 </span>            <span class="hl slc"># one inside bdb.py, and the command-line typed by the</span></span>
<span id="l_982" class="hl fld"><span class="hl lin">  982 </span>            <span class="hl slc"># user (run by exec in pdb itself).</span></span>
<span id="l_983" class="hl fld"><span class="hl lin">  983 </span>            self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">InteractiveTB</span><span class="hl opt">(</span>etype<span class="hl opt">,</span> value<span class="hl opt">,</span> tb<span class="hl opt">,</span> tb_offset<span class="hl opt">=</span><span class="hl num">3</span><span class="hl opt">)</span></span>
<span id="l_984" class="hl fld"><span class="hl lin">  984 </span></span>
<span id="l_985" class="hl fld"><span class="hl lin">  985 </span>    <span class="hl kwb">&#64;staticmethod</span></span>
<span id="l_986" class="hl fld"><span class="hl lin">  986 </span>    <span class="hl kwa">def</span> <span class="hl kwd">_run_with_timing</span><span class="hl opt">(</span>run<span class="hl opt">,</span> nruns<span class="hl opt">):</span></span>
<span id="l_987" class="hl fld"><span class="hl lin">  987 </span>        <span class="hl sng">&quot;&quot;&quot;</span></span>
<span id="l_988" class="hl fld"><span class="hl lin">  988 </span><span class="hl sng">        Run function `run` and print timing information.</span></span>
<span id="l_989" class="hl fld"><span class="hl lin">  989 </span><span class="hl sng"></span></span>
<span id="l_990" class="hl fld"><span class="hl lin">  990 </span><span class="hl sng">        Parameters</span></span>
<span id="l_991" class="hl fld"><span class="hl lin">  991 </span><span class="hl sng">        ----------</span></span>
<span id="l_992" class="hl fld"><span class="hl lin">  992 </span><span class="hl sng">        run : callable</span></span>
<span id="l_993" class="hl fld"><span class="hl lin">  993 </span><span class="hl sng">            Any callable object which takes no argument.</span></span>
<span id="l_994" class="hl fld"><span class="hl lin">  994 </span><span class="hl sng">        nruns : int</span></span>
<span id="l_995" class="hl fld"><span class="hl lin">  995 </span><span class="hl sng">            Number of times to execute `run`.</span></span>
<span id="l_996" class="hl fld"><span class="hl lin">  996 </span><span class="hl sng"></span></span>
<span id="l_997" class="hl fld"><span class="hl lin">  997 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_998" class="hl fld"><span class="hl lin">  998 </span>        twall0 <span class="hl opt">=</span> time<span class="hl opt">.</span><span class="hl kwd">perf_counter</span><span class="hl opt">()</span></span>
<span id="l_999" class="hl fld"><span class="hl lin">  999 </span>        <span class="hl kwa">if</span> nruns <span class="hl opt">==</span> <span class="hl num">1</span><span class="hl opt">:</span></span>
<span id="l_1000" class="hl fld"><span class="hl lin"> 1000 </span>            t0 <span class="hl opt">=</span> <span class="hl kwd">clock2</span><span class="hl opt">()</span></span>
<span id="l_1001" class="hl fld"><span class="hl lin"> 1001 </span>            <span class="hl kwd">run</span><span class="hl opt">()</span></span>
<span id="l_1002" class="hl fld"><span class="hl lin"> 1002 </span>            t1 <span class="hl opt">=</span> <span class="hl kwd">clock2</span><span class="hl opt">()</span></span>
<span id="l_1003" class="hl fld"><span class="hl lin"> 1003 </span>            t_usr <span class="hl opt">=</span> t1<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">] -</span> t0<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">]</span></span>
<span id="l_1004" class="hl fld"><span class="hl lin"> 1004 </span>            t_sys <span class="hl opt">=</span> t1<span class="hl opt">[</span><span class="hl num">1</span><span class="hl opt">] -</span> t0<span class="hl opt">[</span><span class="hl num">1</span><span class="hl opt">]</span></span>
<span id="l_1005" class="hl fld"><span class="hl lin"> 1005 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;</span><span class="hl esc">\n</span><span class="hl sng">IPython CPU timings (estimated):&quot;</span><span class="hl opt">)</span></span>
<span id="l_1006" class="hl fld"><span class="hl lin"> 1006 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;  User   : %10.2f s.&quot;</span> <span class="hl opt">%</span> t_usr<span class="hl opt">)</span></span>
<span id="l_1007" class="hl fld"><span class="hl lin"> 1007 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;  System : %10.2f s.&quot;</span> <span class="hl opt">%</span> t_sys<span class="hl opt">)</span></span>
<span id="l_1008" class="hl fld"><span class="hl lin"> 1008 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_1009" class="hl fld"><span class="hl lin"> 1009 </span>            runs <span class="hl opt">=</span> <span class="hl kwb">range</span><span class="hl opt">(</span>nruns<span class="hl opt">)</span></span>
<span id="l_1010" class="hl fld"><span class="hl lin"> 1010 </span>            t0 <span class="hl opt">=</span> <span class="hl kwd">clock2</span><span class="hl opt">()</span></span>
<span id="l_1011" class="hl fld"><span class="hl lin"> 1011 </span>            <span class="hl kwa">for</span> nr <span class="hl kwa">in</span> runs<span class="hl opt">:</span></span>
<span id="l_1012" class="hl fld"><span class="hl lin"> 1012 </span>                <span class="hl kwd">run</span><span class="hl opt">()</span></span>
<span id="l_1013" class="hl fld"><span class="hl lin"> 1013 </span>            t1 <span class="hl opt">=</span> <span class="hl kwd">clock2</span><span class="hl opt">()</span></span>
<span id="l_1014" class="hl fld"><span class="hl lin"> 1014 </span>            t_usr <span class="hl opt">=</span> t1<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">] -</span> t0<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">]</span></span>
<span id="l_1015" class="hl fld"><span class="hl lin"> 1015 </span>            t_sys <span class="hl opt">=</span> t1<span class="hl opt">[</span><span class="hl num">1</span><span class="hl opt">] -</span> t0<span class="hl opt">[</span><span class="hl num">1</span><span class="hl opt">]</span></span>
<span id="l_1016" class="hl fld"><span class="hl lin"> 1016 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;</span><span class="hl esc">\n</span><span class="hl sng">IPython CPU timings (estimated):&quot;</span><span class="hl opt">)</span></span>
<span id="l_1017" class="hl fld"><span class="hl lin"> 1017 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;Total runs performed:&quot;</span><span class="hl opt">,</span> nruns<span class="hl opt">)</span></span>
<span id="l_1018" class="hl fld"><span class="hl lin"> 1018 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;  Times  : %10s   %10s&quot;</span> <span class="hl opt">% (</span><span class="hl sng">&#39;Total&#39;</span><span class="hl opt">,</span> <span class="hl sng">&#39;Per run&#39;</span><span class="hl opt">))</span></span>
<span id="l_1019" class="hl fld"><span class="hl lin"> 1019 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;  User   : %10.2f s, %10.2f s.&quot;</span> <span class="hl opt">% (</span>t_usr<span class="hl opt">,</span> t_usr <span class="hl opt">/</span> nruns<span class="hl opt">))</span></span>
<span id="l_1020" class="hl fld"><span class="hl lin"> 1020 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;  System : %10.2f s, %10.2f s.&quot;</span> <span class="hl opt">% (</span>t_sys<span class="hl opt">,</span> t_sys <span class="hl opt">/</span> nruns<span class="hl opt">))</span></span>
<span id="l_1021" class="hl fld"><span class="hl lin"> 1021 </span>        twall1 <span class="hl opt">=</span> time<span class="hl opt">.</span><span class="hl kwd">perf_counter</span><span class="hl opt">()</span></span>
<span id="l_1022" class="hl fld"><span class="hl lin"> 1022 </span>        <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;Wall time: %10.2f s.&quot;</span> <span class="hl opt">% (</span>twall1 <span class="hl opt">-</span> twall0<span class="hl opt">))</span></span>
<span id="l_1023" class="hl fld"><span class="hl lin"> 1023 </span></span>
<span id="l_1024" class="hl fld"><span class="hl lin"> 1024 </span>    <span class="hl kwb">&#64;skip_doctest</span></span>
<span id="l_1025" class="hl fld"><span class="hl lin"> 1025 </span>    <span class="hl kwb">&#64;no_var_expand</span></span>
<span id="l_1026" class="hl fld"><span class="hl lin"> 1026 </span>    <span class="hl kwb">&#64;line_cell_magic</span></span>
<span id="l_1027" class="hl fld"><span class="hl lin"> 1027 </span>    <span class="hl kwb">&#64;needs_local_scope</span></span>
<span id="l_1028" class="hl fld"><span class="hl lin"> 1028 </span>    <span class="hl kwa">def</span> <span class="hl kwd">timeit</span><span class="hl opt">(</span>self<span class="hl opt">,</span> line<span class="hl opt">=</span><span class="hl sng">&#39;&#39;</span><span class="hl opt">,</span> cell<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">,</span> local_ns<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">):</span></span>
<span id="l_1029" class="hl fld"><span class="hl lin"> 1029 </span>        <span class="hl sng">&quot;&quot;&quot;Time execution of a Python statement or expression</span></span>
<span id="l_1030" class="hl fld"><span class="hl lin"> 1030 </span><span class="hl sng"></span></span>
<span id="l_1031" class="hl fld"><span class="hl lin"> 1031 </span><span class="hl sng">        Usage, in line mode:</span></span>
<span id="l_1032" class="hl fld"><span class="hl lin"> 1032 </span><span class="hl sng">          %timeit [-n&lt;N&gt; -r&lt;R&gt; [-t|-c] -q -p&lt;P&gt; -o] statement</span></span>
<span id="l_1033" class="hl fld"><span class="hl lin"> 1033 </span><span class="hl sng">        or in cell mode:</span></span>
<span id="l_1034" class="hl fld"><span class="hl lin"> 1034 </span><span class="hl sng"></span>          <span class="hl ipl">%%</span><span class="hl sng">timeit [-n&lt;N&gt; -r&lt;R&gt; [-t|-c] -q -p&lt;P&gt; -o] setup_code</span></span>
<span id="l_1035" class="hl fld"><span class="hl lin"> 1035 </span><span class="hl sng">          code</span></span>
<span id="l_1036" class="hl fld"><span class="hl lin"> 1036 </span><span class="hl sng">          code...</span></span>
<span id="l_1037" class="hl fld"><span class="hl lin"> 1037 </span><span class="hl sng"></span></span>
<span id="l_1038" class="hl fld"><span class="hl lin"> 1038 </span><span class="hl sng">        Time execution of a Python statement or expression using the timeit</span></span>
<span id="l_1039" class="hl fld"><span class="hl lin"> 1039 </span><span class="hl sng">        module.  This function can be used both as a line and cell magic:</span></span>
<span id="l_1040" class="hl fld"><span class="hl lin"> 1040 </span><span class="hl sng"></span></span>
<span id="l_1041" class="hl fld"><span class="hl lin"> 1041 </span><span class="hl sng">        - In line mode you can time a single-line statement (though multiple</span></span>
<span id="l_1042" class="hl fld"><span class="hl lin"> 1042 </span><span class="hl sng">          ones can be chained with using semicolons).</span></span>
<span id="l_1043" class="hl fld"><span class="hl lin"> 1043 </span><span class="hl sng"></span></span>
<span id="l_1044" class="hl fld"><span class="hl lin"> 1044 </span><span class="hl sng">        - In cell mode, the statement in the first line is used as setup code</span></span>
<span id="l_1045" class="hl fld"><span class="hl lin"> 1045 </span><span class="hl sng">          (executed but not timed) and the body of the cell is timed.  The cell</span></span>
<span id="l_1046" class="hl fld"><span class="hl lin"> 1046 </span><span class="hl sng">          body has access to any variables created in the setup code.</span></span>
<span id="l_1047" class="hl fld"><span class="hl lin"> 1047 </span><span class="hl sng"></span></span>
<span id="l_1048" class="hl fld"><span class="hl lin"> 1048 </span><span class="hl sng">        Options:</span></span>
<span id="l_1049" class="hl fld"><span class="hl lin"> 1049 </span><span class="hl sng">        -n&lt;N&gt;: execute the given statement &lt;N&gt; times in a loop. If &lt;N&gt; is not</span></span>
<span id="l_1050" class="hl fld"><span class="hl lin"> 1050 </span><span class="hl sng">        provided, &lt;N&gt; is determined so as to get sufficient accuracy.</span></span>
<span id="l_1051" class="hl fld"><span class="hl lin"> 1051 </span><span class="hl sng"></span></span>
<span id="l_1052" class="hl fld"><span class="hl lin"> 1052 </span><span class="hl sng">        -r&lt;R&gt;: number of repeats &lt;R&gt;, each consisting of &lt;N&gt; loops, and take the</span></span>
<span id="l_1053" class="hl fld"><span class="hl lin"> 1053 </span><span class="hl sng">        average result.</span></span>
<span id="l_1054" class="hl fld"><span class="hl lin"> 1054 </span><span class="hl sng">        Default: 7</span></span>
<span id="l_1055" class="hl fld"><span class="hl lin"> 1055 </span><span class="hl sng"></span></span>
<span id="l_1056" class="hl fld"><span class="hl lin"> 1056 </span><span class="hl sng">        -t: use time.time to measure the time, which is the default on Unix.</span></span>
<span id="l_1057" class="hl fld"><span class="hl lin"> 1057 </span><span class="hl sng">        This function measures wall time.</span></span>
<span id="l_1058" class="hl fld"><span class="hl lin"> 1058 </span><span class="hl sng"></span></span>
<span id="l_1059" class="hl fld"><span class="hl lin"> 1059 </span><span class="hl sng">        -c: use time.clock to measure the time, which is the default on</span></span>
<span id="l_1060" class="hl fld"><span class="hl lin"> 1060 </span><span class="hl sng">        Windows and measures wall time. On Unix, resource.getrusage is used</span></span>
<span id="l_1061" class="hl fld"><span class="hl lin"> 1061 </span><span class="hl sng">        instead and returns the CPU user time.</span></span>
<span id="l_1062" class="hl fld"><span class="hl lin"> 1062 </span><span class="hl sng"></span></span>
<span id="l_1063" class="hl fld"><span class="hl lin"> 1063 </span><span class="hl sng">        -p&lt;P&gt;: use a precision of &lt;P&gt; digits to display the timing result.</span></span>
<span id="l_1064" class="hl fld"><span class="hl lin"> 1064 </span><span class="hl sng">        Default: 3</span></span>
<span id="l_1065" class="hl fld"><span class="hl lin"> 1065 </span><span class="hl sng"></span></span>
<span id="l_1066" class="hl fld"><span class="hl lin"> 1066 </span><span class="hl sng">        -q: Quiet, do not print result.</span></span>
<span id="l_1067" class="hl fld"><span class="hl lin"> 1067 </span><span class="hl sng"></span></span>
<span id="l_1068" class="hl fld"><span class="hl lin"> 1068 </span><span class="hl sng">        -o: return a TimeitResult that can be stored in a variable to inspect</span></span>
<span id="l_1069" class="hl fld"><span class="hl lin"> 1069 </span><span class="hl sng">            the result in more details.</span></span>
<span id="l_1070" class="hl fld"><span class="hl lin"> 1070 </span><span class="hl sng"></span></span>
<span id="l_1071" class="hl fld"><span class="hl lin"> 1071 </span><span class="hl sng">        .. versionchanged:: 7.3</span></span>
<span id="l_1072" class="hl fld"><span class="hl lin"> 1072 </span><span class="hl sng">            User variables are no longer expanded,</span></span>
<span id="l_1073" class="hl fld"><span class="hl lin"> 1073 </span><span class="hl sng">            the magic line is always left unmodified.</span></span>
<span id="l_1074" class="hl fld"><span class="hl lin"> 1074 </span><span class="hl sng"></span></span>
<span id="l_1075" class="hl fld"><span class="hl lin"> 1075 </span><span class="hl sng">        Examples</span></span>
<span id="l_1076" class="hl fld"><span class="hl lin"> 1076 </span><span class="hl sng">        --------</span></span>
<span id="l_1077" class="hl fld"><span class="hl lin"> 1077 </span><span class="hl sng">        ::</span></span>
<span id="l_1078" class="hl fld"><span class="hl lin"> 1078 </span><span class="hl sng"></span></span>
<span id="l_1079" class="hl fld"><span class="hl lin"> 1079 </span><span class="hl sng">          In [1]: %timeit pass</span></span>
<span id="l_1080" class="hl fld"><span class="hl lin"> 1080 </span><span class="hl sng">          8.26 ns ± 0.12 ns per loop (mean ± std. dev. of 7 runs, 100000000 loops each)</span></span>
<span id="l_1081" class="hl fld"><span class="hl lin"> 1081 </span><span class="hl sng"></span></span>
<span id="l_1082" class="hl fld"><span class="hl lin"> 1082 </span><span class="hl sng">          In [2]: u = None</span></span>
<span id="l_1083" class="hl fld"><span class="hl lin"> 1083 </span><span class="hl sng"></span></span>
<span id="l_1084" class="hl fld"><span class="hl lin"> 1084 </span><span class="hl sng">          In [3]: %timeit u is None</span></span>
<span id="l_1085" class="hl fld"><span class="hl lin"> 1085 </span><span class="hl sng">          29.9 ns ± 0.643 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)</span></span>
<span id="l_1086" class="hl fld"><span class="hl lin"> 1086 </span><span class="hl sng"></span></span>
<span id="l_1087" class="hl fld"><span class="hl lin"> 1087 </span><span class="hl sng">          In [4]: %timeit -r 4 u == None</span></span>
<span id="l_1088" class="hl fld"><span class="hl lin"> 1088 </span><span class="hl sng"></span></span>
<span id="l_1089" class="hl fld"><span class="hl lin"> 1089 </span><span class="hl sng">          In [5]: import time</span></span>
<span id="l_1090" class="hl fld"><span class="hl lin"> 1090 </span><span class="hl sng"></span></span>
<span id="l_1091" class="hl fld"><span class="hl lin"> 1091 </span><span class="hl sng">          In [6]: %timeit -n1 time.sleep(2)</span></span>
<span id="l_1092" class="hl fld"><span class="hl lin"> 1092 </span><span class="hl sng"></span></span>
<span id="l_1093" class="hl fld"><span class="hl lin"> 1093 </span><span class="hl sng">        The times reported by %timeit will be slightly higher than those</span></span>
<span id="l_1094" class="hl fld"><span class="hl lin"> 1094 </span><span class="hl sng">        reported by the timeit.py script when variables are accessed. This is</span></span>
<span id="l_1095" class="hl fld"><span class="hl lin"> 1095 </span><span class="hl sng">        due to the fact that %timeit executes the statement in the namespace</span></span>
<span id="l_1096" class="hl fld"><span class="hl lin"> 1096 </span><span class="hl sng">        of the shell, compared with timeit.py, which uses a single setup</span></span>
<span id="l_1097" class="hl fld"><span class="hl lin"> 1097 </span><span class="hl sng">        statement to import function or create variables. Generally, the bias</span></span>
<span id="l_1098" class="hl fld"><span class="hl lin"> 1098 </span><span class="hl sng">        does not matter as long as results from timeit.py are not mixed with</span></span>
<span id="l_1099" class="hl fld"><span class="hl lin"> 1099 </span><span class="hl sng">        those from %timeit.&quot;&quot;&quot;</span></span>
<span id="l_1100" class="hl fld"><span class="hl lin"> 1100 </span></span>
<span id="l_1101" class="hl fld"><span class="hl lin"> 1101 </span>        opts<span class="hl opt">,</span> stmt <span class="hl opt">=</span> self<span class="hl opt">.</span><span class="hl kwd">parse_options</span><span class="hl opt">(</span></span>
<span id="l_1102" class="hl fld"><span class="hl lin"> 1102 </span>            line<span class="hl opt">,</span> <span class="hl sng">&quot;n:r:tcp:qo&quot;</span><span class="hl opt">,</span> posix<span class="hl opt">=</span><span class="hl kwa">False</span><span class="hl opt">,</span> strict<span class="hl opt">=</span><span class="hl kwa">False</span><span class="hl opt">,</span> preserve_non_opts<span class="hl opt">=</span><span class="hl kwa">True</span></span>
<span id="l_1103" class="hl fld"><span class="hl lin"> 1103 </span>        <span class="hl opt">)</span></span>
<span id="l_1104" class="hl fld"><span class="hl lin"> 1104 </span>        <span class="hl kwa">if</span> stmt <span class="hl opt">==</span> <span class="hl sng">&quot;&quot;</span> <span class="hl kwa">and</span> cell <span class="hl kwa">is None</span><span class="hl opt">:</span></span>
<span id="l_1105" class="hl fld"><span class="hl lin"> 1105 </span>            <span class="hl kwa">return</span></span>
<span id="l_1106" class="hl fld"><span class="hl lin"> 1106 </span>        </span>
<span id="l_1107" class="hl fld"><span class="hl lin"> 1107 </span>        timefunc <span class="hl opt">=</span> timeit<span class="hl opt">.</span>default_timer</span>
<span id="l_1108" class="hl fld"><span class="hl lin"> 1108 </span>        number <span class="hl opt">=</span> <span class="hl kwb">int</span><span class="hl opt">(</span><span class="hl kwb">getattr</span><span class="hl opt">(</span>opts<span class="hl opt">,</span> <span class="hl sng">&quot;n&quot;</span><span class="hl opt">,</span> <span class="hl num">0</span><span class="hl opt">))</span></span>
<span id="l_1109" class="hl fld"><span class="hl lin"> 1109 </span>        default_repeat <span class="hl opt">=</span> <span class="hl num">7</span> <span class="hl kwa">if</span> timeit<span class="hl opt">.</span>default_repeat <span class="hl opt">&lt;</span> <span class="hl num">7</span> <span class="hl kwa">else</span> timeit<span class="hl opt">.</span>default_repeat</span>
<span id="l_1110" class="hl fld"><span class="hl lin"> 1110 </span>        repeat <span class="hl opt">=</span> <span class="hl kwb">int</span><span class="hl opt">(</span><span class="hl kwb">getattr</span><span class="hl opt">(</span>opts<span class="hl opt">,</span> <span class="hl sng">&quot;r&quot;</span><span class="hl opt">,</span> default_repeat<span class="hl opt">))</span></span>
<span id="l_1111" class="hl fld"><span class="hl lin"> 1111 </span>        precision <span class="hl opt">=</span> <span class="hl kwb">int</span><span class="hl opt">(</span><span class="hl kwb">getattr</span><span class="hl opt">(</span>opts<span class="hl opt">,</span> <span class="hl sng">&quot;p&quot;</span><span class="hl opt">,</span> <span class="hl num">3</span><span class="hl opt">))</span></span>
<span id="l_1112" class="hl fld"><span class="hl lin"> 1112 </span>        quiet <span class="hl opt">=</span> <span class="hl sng">&#39;q&#39;</span> <span class="hl kwa">in</span> opts</span>
<span id="l_1113" class="hl fld"><span class="hl lin"> 1113 </span>        return_result <span class="hl opt">=</span> <span class="hl sng">&#39;o&#39;</span> <span class="hl kwa">in</span> opts</span>
<span id="l_1114" class="hl fld"><span class="hl lin"> 1114 </span>        <span class="hl kwa">if</span> <span class="hl kwb">hasattr</span><span class="hl opt">(</span>opts<span class="hl opt">,</span> <span class="hl sng">&quot;t&quot;</span><span class="hl opt">):</span></span>
<span id="l_1115" class="hl fld"><span class="hl lin"> 1115 </span>            timefunc <span class="hl opt">=</span> time<span class="hl opt">.</span>time</span>
<span id="l_1116" class="hl fld"><span class="hl lin"> 1116 </span>        <span class="hl kwa">if</span> <span class="hl kwb">hasattr</span><span class="hl opt">(</span>opts<span class="hl opt">,</span> <span class="hl sng">&quot;c&quot;</span><span class="hl opt">):</span></span>
<span id="l_1117" class="hl fld"><span class="hl lin"> 1117 </span>            timefunc <span class="hl opt">=</span> clock</span>
<span id="l_1118" class="hl fld"><span class="hl lin"> 1118 </span></span>
<span id="l_1119" class="hl fld"><span class="hl lin"> 1119 </span>        timer <span class="hl opt">=</span> <span class="hl kwd">Timer</span><span class="hl opt">(</span>timer<span class="hl opt">=</span>timefunc<span class="hl opt">)</span></span>
<span id="l_1120" class="hl fld"><span class="hl lin"> 1120 </span>        <span class="hl slc"># this code has tight coupling to the inner workings of timeit.Timer,</span></span>
<span id="l_1121" class="hl fld"><span class="hl lin"> 1121 </span>        <span class="hl slc"># but is there a better way to achieve that the code stmt has access</span></span>
<span id="l_1122" class="hl fld"><span class="hl lin"> 1122 </span>        <span class="hl slc"># to the shell namespace?</span></span>
<span id="l_1123" class="hl fld"><span class="hl lin"> 1123 </span>        transform  <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>transform_cell</span>
<span id="l_1124" class="hl fld"><span class="hl lin"> 1124 </span></span>
<span id="l_1125" class="hl fld"><span class="hl lin"> 1125 </span>        <span class="hl kwa">if</span> cell <span class="hl kwa">is None</span><span class="hl opt">:</span></span>
<span id="l_1126" class="hl fld"><span class="hl lin"> 1126 </span>            <span class="hl slc"># called as line magic</span></span>
<span id="l_1127" class="hl fld"><span class="hl lin"> 1127 </span>            ast_setup <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">.</span><span class="hl kwd">ast_parse</span><span class="hl opt">(</span><span class="hl sng">&quot;pass&quot;</span><span class="hl opt">)</span></span>
<span id="l_1128" class="hl fld"><span class="hl lin"> 1128 </span>            ast_stmt <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">.</span><span class="hl kwd">ast_parse</span><span class="hl opt">(</span><span class="hl kwd">transform</span><span class="hl opt">(</span>stmt<span class="hl opt">))</span></span>
<span id="l_1129" class="hl fld"><span class="hl lin"> 1129 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_1130" class="hl fld"><span class="hl lin"> 1130 </span>            ast_setup <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">.</span><span class="hl kwd">ast_parse</span><span class="hl opt">(</span><span class="hl kwd">transform</span><span class="hl opt">(</span>stmt<span class="hl opt">))</span></span>
<span id="l_1131" class="hl fld"><span class="hl lin"> 1131 </span>            ast_stmt <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">.</span><span class="hl kwd">ast_parse</span><span class="hl opt">(</span><span class="hl kwd">transform</span><span class="hl opt">(</span>cell<span class="hl opt">))</span></span>
<span id="l_1132" class="hl fld"><span class="hl lin"> 1132 </span></span>
<span id="l_1133" class="hl fld"><span class="hl lin"> 1133 </span>        ast_setup <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">transform_ast</span><span class="hl opt">(</span>ast_setup<span class="hl opt">)</span></span>
<span id="l_1134" class="hl fld"><span class="hl lin"> 1134 </span>        ast_stmt <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">transform_ast</span><span class="hl opt">(</span>ast_stmt<span class="hl opt">)</span></span>
<span id="l_1135" class="hl fld"><span class="hl lin"> 1135 </span></span>
<span id="l_1136" class="hl fld"><span class="hl lin"> 1136 </span>        <span class="hl slc"># Check that these compile to valid Python code *outside* the timer func</span></span>
<span id="l_1137" class="hl fld"><span class="hl lin"> 1137 </span>        <span class="hl slc"># Invalid code may become valid when put inside the function &amp; loop,</span></span>
<span id="l_1138" class="hl fld"><span class="hl lin"> 1138 </span>        <span class="hl slc"># which messes up error messages.</span></span>
<span id="l_1139" class="hl fld"><span class="hl lin"> 1139 </span>        <span class="hl slc"># https://github.com/ipython/ipython/issues/10636</span></span>
<span id="l_1140" class="hl fld"><span class="hl lin"> 1140 </span>        self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">(</span>ast_setup<span class="hl opt">,</span> <span class="hl sng">&quot;&lt;magic-timeit-setup&gt;&quot;</span><span class="hl opt">,</span> <span class="hl sng">&quot;exec&quot;</span><span class="hl opt">)</span></span>
<span id="l_1141" class="hl fld"><span class="hl lin"> 1141 </span>        self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">(</span>ast_stmt<span class="hl opt">,</span> <span class="hl sng">&quot;&lt;magic-timeit-stmt&gt;&quot;</span><span class="hl opt">,</span> <span class="hl sng">&quot;exec&quot;</span><span class="hl opt">)</span></span>
<span id="l_1142" class="hl fld"><span class="hl lin"> 1142 </span></span>
<span id="l_1143" class="hl fld"><span class="hl lin"> 1143 </span>        <span class="hl slc"># This codestring is taken from timeit.template - we fill it in as an</span></span>
<span id="l_1144" class="hl fld"><span class="hl lin"> 1144 </span>        <span class="hl slc"># AST, so that we can apply our AST transformations to the user code</span></span>
<span id="l_1145" class="hl fld"><span class="hl lin"> 1145 </span>        <span class="hl slc"># without affecting the timing code.</span></span>
<span id="l_1146" class="hl fld"><span class="hl lin"> 1146 </span>        timeit_ast_template <span class="hl opt">=</span> ast<span class="hl opt">.</span><span class="hl kwd">parse</span><span class="hl opt">(</span><span class="hl sng">&#39;def inner(_it, _timer):</span><span class="hl esc">\n</span><span class="hl sng">&#39;</span></span>
<span id="l_1147" class="hl fld"><span class="hl lin"> 1147 </span>                                        <span class="hl sng">&#39;    setup</span><span class="hl esc">\n</span><span class="hl sng">&#39;</span></span>
<span id="l_1148" class="hl fld"><span class="hl lin"> 1148 </span>                                        <span class="hl sng">&#39;    _t0 = _timer()</span><span class="hl esc">\n</span><span class="hl sng">&#39;</span></span>
<span id="l_1149" class="hl fld"><span class="hl lin"> 1149 </span>                                        <span class="hl sng">&#39;    for _i in _it:</span><span class="hl esc">\n</span><span class="hl sng">&#39;</span></span>
<span id="l_1150" class="hl fld"><span class="hl lin"> 1150 </span>                                        <span class="hl sng">&#39;        stmt</span><span class="hl esc">\n</span><span class="hl sng">&#39;</span></span>
<span id="l_1151" class="hl fld"><span class="hl lin"> 1151 </span>                                        <span class="hl sng">&#39;    _t1 = _timer()</span><span class="hl esc">\n</span><span class="hl sng">&#39;</span></span>
<span id="l_1152" class="hl fld"><span class="hl lin"> 1152 </span>                                        <span class="hl sng">&#39;    return _t1 - _t0</span><span class="hl esc">\n</span><span class="hl sng">&#39;</span><span class="hl opt">)</span></span>
<span id="l_1153" class="hl fld"><span class="hl lin"> 1153 </span></span>
<span id="l_1154" class="hl fld"><span class="hl lin"> 1154 </span>        timeit_ast <span class="hl opt">=</span> <span class="hl kwd">TimeitTemplateFiller</span><span class="hl opt">(</span>ast_setup<span class="hl opt">,</span> ast_stmt<span class="hl opt">).</span><span class="hl kwd">visit</span><span class="hl opt">(</span>timeit_ast_template<span class="hl opt">)</span></span>
<span id="l_1155" class="hl fld"><span class="hl lin"> 1155 </span>        timeit_ast <span class="hl opt">=</span> ast<span class="hl opt">.</span><span class="hl kwd">fix_missing_locations</span><span class="hl opt">(</span>timeit_ast<span class="hl opt">)</span></span>
<span id="l_1156" class="hl fld"><span class="hl lin"> 1156 </span></span>
<span id="l_1157" class="hl fld"><span class="hl lin"> 1157 </span>        <span class="hl slc"># Track compilation time so it can be reported if too long</span></span>
<span id="l_1158" class="hl fld"><span class="hl lin"> 1158 </span>        <span class="hl slc"># Minimum time above which compilation time will be reported</span></span>
<span id="l_1159" class="hl fld"><span class="hl lin"> 1159 </span>        tc_min <span class="hl opt">=</span> <span class="hl num">0.1</span></span>
<span id="l_1160" class="hl fld"><span class="hl lin"> 1160 </span></span>
<span id="l_1161" class="hl fld"><span class="hl lin"> 1161 </span>        t0 <span class="hl opt">=</span> <span class="hl kwd">clock</span><span class="hl opt">()</span></span>
<span id="l_1162" class="hl fld"><span class="hl lin"> 1162 </span>        code <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">(</span>timeit_ast<span class="hl opt">,</span> <span class="hl sng">&quot;&lt;magic-timeit&gt;&quot;</span><span class="hl opt">,</span> <span class="hl sng">&quot;exec&quot;</span><span class="hl opt">)</span></span>
<span id="l_1163" class="hl fld"><span class="hl lin"> 1163 </span>        tc <span class="hl opt">=</span> <span class="hl kwd">clock</span><span class="hl opt">()-</span>t0</span>
<span id="l_1164" class="hl fld"><span class="hl lin"> 1164 </span></span>
<span id="l_1165" class="hl fld"><span class="hl lin"> 1165 </span>        ns <span class="hl opt">= {}</span></span>
<span id="l_1166" class="hl fld"><span class="hl lin"> 1166 </span>        glob <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns</span>
<span id="l_1167" class="hl fld"><span class="hl lin"> 1167 </span>        <span class="hl slc"># handles global vars with same name as local vars. We store them in conflict_globs.</span></span>
<span id="l_1168" class="hl fld"><span class="hl lin"> 1168 </span>        conflict_globs <span class="hl opt">= {}</span></span>
<span id="l_1169" class="hl fld"><span class="hl lin"> 1169 </span>        <span class="hl kwa">if</span> local_ns <span class="hl kwa">and</span> cell <span class="hl kwa">is None</span><span class="hl opt">:</span></span>
<span id="l_1170" class="hl fld"><span class="hl lin"> 1170 </span>            <span class="hl kwa">for</span> var_name<span class="hl opt">,</span> var_val <span class="hl kwa">in</span> glob<span class="hl opt">.</span><span class="hl kwd">items</span><span class="hl opt">():</span></span>
<span id="l_1171" class="hl fld"><span class="hl lin"> 1171 </span>                <span class="hl kwa">if</span> var_name <span class="hl kwa">in</span> local_ns<span class="hl opt">:</span></span>
<span id="l_1172" class="hl fld"><span class="hl lin"> 1172 </span>                    conflict_globs<span class="hl opt">[</span>var_name<span class="hl opt">] =</span> var_val</span>
<span id="l_1173" class="hl fld"><span class="hl lin"> 1173 </span>            glob<span class="hl opt">.</span><span class="hl kwd">update</span><span class="hl opt">(</span>local_ns<span class="hl opt">)</span></span>
<span id="l_1174" class="hl fld"><span class="hl lin"> 1174 </span>            </span>
<span id="l_1175" class="hl fld"><span class="hl lin"> 1175 </span>        <span class="hl kwa">exec</span><span class="hl opt">(</span>code<span class="hl opt">,</span> glob<span class="hl opt">,</span> ns<span class="hl opt">)</span></span>
<span id="l_1176" class="hl fld"><span class="hl lin"> 1176 </span>        timer<span class="hl opt">.</span>inner <span class="hl opt">=</span> ns<span class="hl opt">[</span><span class="hl sng">&quot;inner&quot;</span><span class="hl opt">]</span></span>
<span id="l_1177" class="hl fld"><span class="hl lin"> 1177 </span></span>
<span id="l_1178" class="hl fld"><span class="hl lin"> 1178 </span>        <span class="hl slc"># This is used to check if there is a huge difference between the</span></span>
<span id="l_1179" class="hl fld"><span class="hl lin"> 1179 </span>        <span class="hl slc"># best and worst timings.</span></span>
<span id="l_1180" class="hl fld"><span class="hl lin"> 1180 </span>        <span class="hl slc"># Issue: https://github.com/ipython/ipython/issues/6471</span></span>
<span id="l_1181" class="hl fld"><span class="hl lin"> 1181 </span>        <span class="hl kwa">if</span> number <span class="hl opt">==</span> <span class="hl num">0</span><span class="hl opt">:</span></span>
<span id="l_1182" class="hl fld"><span class="hl lin"> 1182 </span>            <span class="hl slc"># determine number so that 0.2 &lt;= total time &lt; 2.0</span></span>
<span id="l_1183" class="hl fld"><span class="hl lin"> 1183 </span>            <span class="hl kwa">for</span> index <span class="hl kwa">in</span> <span class="hl kwb">range</span><span class="hl opt">(</span><span class="hl num">0</span><span class="hl opt">,</span> <span class="hl num">10</span><span class="hl opt">):</span></span>
<span id="l_1184" class="hl fld"><span class="hl lin"> 1184 </span>                number <span class="hl opt">=</span> <span class="hl num">10</span> <span class="hl opt">**</span> index</span>
<span id="l_1185" class="hl fld"><span class="hl lin"> 1185 </span>                time_number <span class="hl opt">=</span> timer<span class="hl opt">.</span><span class="hl kwd">timeit</span><span class="hl opt">(</span>number<span class="hl opt">)</span></span>
<span id="l_1186" class="hl fld"><span class="hl lin"> 1186 </span>                <span class="hl kwa">if</span> time_number <span class="hl opt">&gt;=</span> <span class="hl num">0.2</span><span class="hl opt">:</span></span>
<span id="l_1187" class="hl fld"><span class="hl lin"> 1187 </span>                    <span class="hl kwa">break</span></span>
<span id="l_1188" class="hl fld"><span class="hl lin"> 1188 </span></span>
<span id="l_1189" class="hl fld"><span class="hl lin"> 1189 </span>        all_runs <span class="hl opt">=</span> timer<span class="hl opt">.</span><span class="hl kwd">repeat</span><span class="hl opt">(</span>repeat<span class="hl opt">,</span> number<span class="hl opt">)</span></span>
<span id="l_1190" class="hl fld"><span class="hl lin"> 1190 </span>        best <span class="hl opt">=</span> <span class="hl kwb">min</span><span class="hl opt">(</span>all_runs<span class="hl opt">) /</span> number</span>
<span id="l_1191" class="hl fld"><span class="hl lin"> 1191 </span>        worst <span class="hl opt">=</span> <span class="hl kwb">max</span><span class="hl opt">(</span>all_runs<span class="hl opt">) /</span> number</span>
<span id="l_1192" class="hl fld"><span class="hl lin"> 1192 </span>        timeit_result <span class="hl opt">=</span> <span class="hl kwd">TimeitResult</span><span class="hl opt">(</span>number<span class="hl opt">,</span> repeat<span class="hl opt">,</span> best<span class="hl opt">,</span> worst<span class="hl opt">,</span> all_runs<span class="hl opt">,</span> tc<span class="hl opt">,</span> precision<span class="hl opt">)</span></span>
<span id="l_1193" class="hl fld"><span class="hl lin"> 1193 </span></span>
<span id="l_1194" class="hl fld"><span class="hl lin"> 1194 </span>        <span class="hl slc"># Restore global vars from conflict_globs</span></span>
<span id="l_1195" class="hl fld"><span class="hl lin"> 1195 </span>        <span class="hl kwa">if</span> conflict_globs<span class="hl opt">:</span></span>
<span id="l_1196" class="hl fld"><span class="hl lin"> 1196 </span>           glob<span class="hl opt">.</span><span class="hl kwd">update</span><span class="hl opt">(</span>conflict_globs<span class="hl opt">)</span></span>
<span id="l_1197" class="hl fld"><span class="hl lin"> 1197 </span>                </span>
<span id="l_1198" class="hl fld"><span class="hl lin"> 1198 </span>        <span class="hl kwa">if not</span> quiet <span class="hl opt">:</span></span>
<span id="l_1199" class="hl fld"><span class="hl lin"> 1199 </span>            <span class="hl slc"># Check best timing is greater than zero to avoid a</span></span>
<span id="l_1200" class="hl fld"><span class="hl lin"> 1200 </span>            <span class="hl slc"># ZeroDivisionError.</span></span>
<span id="l_1201" class="hl fld"><span class="hl lin"> 1201 </span>            <span class="hl slc"># In cases where the slowest timing is lesser than a microsecond</span></span>
<span id="l_1202" class="hl fld"><span class="hl lin"> 1202 </span>            <span class="hl slc"># we assume that it does not really matter if the fastest</span></span>
<span id="l_1203" class="hl fld"><span class="hl lin"> 1203 </span>            <span class="hl slc"># timing is 4 times faster than the slowest timing or not.</span></span>
<span id="l_1204" class="hl fld"><span class="hl lin"> 1204 </span>            <span class="hl kwa">if</span> worst <span class="hl opt">&gt;</span> <span class="hl num">4</span> <span class="hl opt">*</span> best <span class="hl kwa">and</span> best <span class="hl opt">&gt;</span> <span class="hl num">0</span> <span class="hl kwa">and</span> worst <span class="hl opt">&gt;</span> <span class="hl num">1e-6</span><span class="hl opt">:</span></span>
<span id="l_1205" class="hl fld"><span class="hl lin"> 1205 </span>                <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;The slowest run took</span> <span class="hl ipl">%0</span><span class="hl sng">.2f times longer than the &quot;</span></span>
<span id="l_1206" class="hl fld"><span class="hl lin"> 1206 </span>                      <span class="hl sng">&quot;fastest. This could mean that an intermediate result &quot;</span></span>
<span id="l_1207" class="hl fld"><span class="hl lin"> 1207 </span>                      <span class="hl sng">&quot;is being cached.&quot;</span> <span class="hl opt">% (</span>worst <span class="hl opt">/</span> best<span class="hl opt">))</span></span>
<span id="l_1208" class="hl fld"><span class="hl lin"> 1208 </span>           </span>
<span id="l_1209" class="hl fld"><span class="hl lin"> 1209 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span> timeit_result <span class="hl opt">)</span></span>
<span id="l_1210" class="hl fld"><span class="hl lin"> 1210 </span></span>
<span id="l_1211" class="hl fld"><span class="hl lin"> 1211 </span>            <span class="hl kwa">if</span> tc <span class="hl opt">&gt;</span> tc_min<span class="hl opt">:</span></span>
<span id="l_1212" class="hl fld"><span class="hl lin"> 1212 </span>                <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&quot;Compiler time: %.2f s&quot;</span> <span class="hl opt">%</span> tc<span class="hl opt">)</span></span>
<span id="l_1213" class="hl fld"><span class="hl lin"> 1213 </span>        <span class="hl kwa">if</span> return_result<span class="hl opt">:</span></span>
<span id="l_1214" class="hl fld"><span class="hl lin"> 1214 </span>            <span class="hl kwa">return</span> timeit_result</span>
<span id="l_1215" class="hl fld"><span class="hl lin"> 1215 </span></span>
<span id="l_1216" class="hl fld"><span class="hl lin"> 1216 </span>    <span class="hl kwb">&#64;skip_doctest</span></span>
<span id="l_1217" class="hl fld"><span class="hl lin"> 1217 </span>    <span class="hl kwb">&#64;no_var_expand</span></span>
<span id="l_1218" class="hl fld"><span class="hl lin"> 1218 </span>    <span class="hl kwb">&#64;needs_local_scope</span></span>
<span id="l_1219" class="hl fld"><span class="hl lin"> 1219 </span>    <span class="hl kwb">&#64;line_cell_magic</span></span>
<span id="l_1220" class="hl fld"><span class="hl lin"> 1220 </span>    <span class="hl kwb">&#64;output_can_be_silenced</span></span>
<span id="l_1221" class="hl fld"><span class="hl lin"> 1221 </span>    <span class="hl kwa">def</span> <span class="hl kwd">time</span><span class="hl opt">(</span>self<span class="hl opt">,</span>line<span class="hl opt">=</span><span class="hl sng">&#39;&#39;</span><span class="hl opt">,</span> cell<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">,</span> local_ns<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">):</span></span>
<span id="l_1222" class="hl fld"><span class="hl lin"> 1222 </span>        <span class="hl sng">&quot;&quot;&quot;Time execution of a Python statement or expression.</span></span>
<span id="l_1223" class="hl fld"><span class="hl lin"> 1223 </span><span class="hl sng"></span></span>
<span id="l_1224" class="hl fld"><span class="hl lin"> 1224 </span><span class="hl sng">        The CPU and wall clock times are printed, and the value of the</span></span>
<span id="l_1225" class="hl fld"><span class="hl lin"> 1225 </span><span class="hl sng">        expression (if any) is returned.  Note that under Win32, system time</span></span>
<span id="l_1226" class="hl fld"><span class="hl lin"> 1226 </span><span class="hl sng">        is always reported as 0, since it can not be measured.</span></span>
<span id="l_1227" class="hl fld"><span class="hl lin"> 1227 </span><span class="hl sng"></span></span>
<span id="l_1228" class="hl fld"><span class="hl lin"> 1228 </span><span class="hl sng">        This function can be used both as a line and cell magic:</span></span>
<span id="l_1229" class="hl fld"><span class="hl lin"> 1229 </span><span class="hl sng"></span></span>
<span id="l_1230" class="hl fld"><span class="hl lin"> 1230 </span><span class="hl sng">        - In line mode you can time a single-line statement (though multiple</span></span>
<span id="l_1231" class="hl fld"><span class="hl lin"> 1231 </span><span class="hl sng">          ones can be chained with using semicolons).</span></span>
<span id="l_1232" class="hl fld"><span class="hl lin"> 1232 </span><span class="hl sng"></span></span>
<span id="l_1233" class="hl fld"><span class="hl lin"> 1233 </span><span class="hl sng">        - In cell mode, you can time the cell body (a directly</span></span>
<span id="l_1234" class="hl fld"><span class="hl lin"> 1234 </span><span class="hl sng">          following statement raises an error).</span></span>
<span id="l_1235" class="hl fld"><span class="hl lin"> 1235 </span><span class="hl sng"></span></span>
<span id="l_1236" class="hl fld"><span class="hl lin"> 1236 </span><span class="hl sng">        This function provides very basic timing functionality.  Use the timeit</span></span>
<span id="l_1237" class="hl fld"><span class="hl lin"> 1237 </span><span class="hl sng">        magic for more control over the measurement.</span></span>
<span id="l_1238" class="hl fld"><span class="hl lin"> 1238 </span><span class="hl sng"></span></span>
<span id="l_1239" class="hl fld"><span class="hl lin"> 1239 </span><span class="hl sng">        .. versionchanged:: 7.3</span></span>
<span id="l_1240" class="hl fld"><span class="hl lin"> 1240 </span><span class="hl sng">            User variables are no longer expanded,</span></span>
<span id="l_1241" class="hl fld"><span class="hl lin"> 1241 </span><span class="hl sng">            the magic line is always left unmodified.</span></span>
<span id="l_1242" class="hl fld"><span class="hl lin"> 1242 </span><span class="hl sng"></span></span>
<span id="l_1243" class="hl fld"><span class="hl lin"> 1243 </span><span class="hl sng">        Examples</span></span>
<span id="l_1244" class="hl fld"><span class="hl lin"> 1244 </span><span class="hl sng">        --------</span></span>
<span id="l_1245" class="hl fld"><span class="hl lin"> 1245 </span><span class="hl sng">        ::</span></span>
<span id="l_1246" class="hl fld"><span class="hl lin"> 1246 </span><span class="hl sng"></span></span>
<span id="l_1247" class="hl fld"><span class="hl lin"> 1247 </span><span class="hl sng">          In [1]: %time 2**128</span></span>
<span id="l_1248" class="hl fld"><span class="hl lin"> 1248 </span><span class="hl sng">          CPU times: user 0.00 s, sys: 0.00 s, total: 0.00 s</span></span>
<span id="l_1249" class="hl fld"><span class="hl lin"> 1249 </span><span class="hl sng">          Wall time: 0.00</span></span>
<span id="l_1250" class="hl fld"><span class="hl lin"> 1250 </span><span class="hl sng">          Out[1]: 340282366920938463463374607431768211456L</span></span>
<span id="l_1251" class="hl fld"><span class="hl lin"> 1251 </span><span class="hl sng"></span></span>
<span id="l_1252" class="hl fld"><span class="hl lin"> 1252 </span><span class="hl sng">          In [2]: n = 1000000</span></span>
<span id="l_1253" class="hl fld"><span class="hl lin"> 1253 </span><span class="hl sng"></span></span>
<span id="l_1254" class="hl fld"><span class="hl lin"> 1254 </span><span class="hl sng">          In [3]: %time sum(range(n))</span></span>
<span id="l_1255" class="hl fld"><span class="hl lin"> 1255 </span><span class="hl sng">          CPU times: user 1.20 s, sys: 0.05 s, total: 1.25 s</span></span>
<span id="l_1256" class="hl fld"><span class="hl lin"> 1256 </span><span class="hl sng">          Wall time: 1.37</span></span>
<span id="l_1257" class="hl fld"><span class="hl lin"> 1257 </span><span class="hl sng">          Out[3]: 499999500000L</span></span>
<span id="l_1258" class="hl fld"><span class="hl lin"> 1258 </span><span class="hl sng"></span></span>
<span id="l_1259" class="hl fld"><span class="hl lin"> 1259 </span><span class="hl sng">          In [4]: %time print &#39;hello world&#39;</span></span>
<span id="l_1260" class="hl fld"><span class="hl lin"> 1260 </span><span class="hl sng">          hello world</span></span>
<span id="l_1261" class="hl fld"><span class="hl lin"> 1261 </span><span class="hl sng">          CPU times: user 0.00 s, sys: 0.00 s, total: 0.00 s</span></span>
<span id="l_1262" class="hl fld"><span class="hl lin"> 1262 </span><span class="hl sng">          Wall time: 0.00</span></span>
<span id="l_1263" class="hl fld"><span class="hl lin"> 1263 </span><span class="hl sng"></span></span>
<span id="l_1264" class="hl fld"><span class="hl lin"> 1264 </span><span class="hl sng">        .. note::</span></span>
<span id="l_1265" class="hl fld"><span class="hl lin"> 1265 </span><span class="hl sng">            The time needed by Python to compile the given expression will be</span></span>
<span id="l_1266" class="hl fld"><span class="hl lin"> 1266 </span><span class="hl sng">            reported if it is more than 0.1s.</span></span>
<span id="l_1267" class="hl fld"><span class="hl lin"> 1267 </span><span class="hl sng"></span></span>
<span id="l_1268" class="hl fld"><span class="hl lin"> 1268 </span><span class="hl sng">            In the example below, the actual exponentiation is done by Python</span></span>
<span id="l_1269" class="hl fld"><span class="hl lin"> 1269 </span><span class="hl sng">            at compilation time, so while the expression can take a noticeable</span></span>
<span id="l_1270" class="hl fld"><span class="hl lin"> 1270 </span><span class="hl sng">            amount of time to compute, that time is purely due to the</span></span>
<span id="l_1271" class="hl fld"><span class="hl lin"> 1271 </span><span class="hl sng">            compilation::</span></span>
<span id="l_1272" class="hl fld"><span class="hl lin"> 1272 </span><span class="hl sng"></span></span>
<span id="l_1273" class="hl fld"><span class="hl lin"> 1273 </span><span class="hl sng">                In [5]: %time 3**9999;</span></span>
<span id="l_1274" class="hl fld"><span class="hl lin"> 1274 </span><span class="hl sng">                CPU times: user 0.00 s, sys: 0.00 s, total: 0.00 s</span></span>
<span id="l_1275" class="hl fld"><span class="hl lin"> 1275 </span><span class="hl sng">                Wall time: 0.00 s</span></span>
<span id="l_1276" class="hl fld"><span class="hl lin"> 1276 </span><span class="hl sng"></span></span>
<span id="l_1277" class="hl fld"><span class="hl lin"> 1277 </span><span class="hl sng">                In [6]: %time 3**999999;</span></span>
<span id="l_1278" class="hl fld"><span class="hl lin"> 1278 </span><span class="hl sng">                CPU times: user 0.00 s, sys: 0.00 s, total: 0.00 s</span></span>
<span id="l_1279" class="hl fld"><span class="hl lin"> 1279 </span><span class="hl sng">                Wall time: 0.00 s</span></span>
<span id="l_1280" class="hl fld"><span class="hl lin"> 1280 </span><span class="hl sng">                Compiler : 0.78 s</span></span>
<span id="l_1281" class="hl fld"><span class="hl lin"> 1281 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_1282" class="hl fld"><span class="hl lin"> 1282 </span>        <span class="hl slc"># fail immediately if the given expression can&#39;t be compiled</span></span>
<span id="l_1283" class="hl fld"><span class="hl lin"> 1283 </span>        </span>
<span id="l_1284" class="hl fld"><span class="hl lin"> 1284 </span>        <span class="hl kwa">if</span> line <span class="hl kwa">and</span> cell<span class="hl opt">:</span></span>
<span id="l_1285" class="hl fld"><span class="hl lin"> 1285 </span>            <span class="hl kwa">raise</span> <span class="hl kwd">UsageError</span><span class="hl opt">(</span><span class="hl sng">&quot;Can&#39;t use statement directly after &#39;</span><span class="hl ipl">%%</span><span class="hl sng">time&#39;!&quot;</span><span class="hl opt">)</span></span>
<span id="l_1286" class="hl fld"><span class="hl lin"> 1286 </span>        </span>
<span id="l_1287" class="hl fld"><span class="hl lin"> 1287 </span>        <span class="hl kwa">if</span> cell<span class="hl opt">:</span></span>
<span id="l_1288" class="hl fld"><span class="hl lin"> 1288 </span>            expr <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">transform_cell</span><span class="hl opt">(</span>cell<span class="hl opt">)</span></span>
<span id="l_1289" class="hl fld"><span class="hl lin"> 1289 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_1290" class="hl fld"><span class="hl lin"> 1290 </span>            expr <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">transform_cell</span><span class="hl opt">(</span>line<span class="hl opt">)</span></span>
<span id="l_1291" class="hl fld"><span class="hl lin"> 1291 </span></span>
<span id="l_1292" class="hl fld"><span class="hl lin"> 1292 </span>        <span class="hl slc"># Minimum time above which parse time will be reported</span></span>
<span id="l_1293" class="hl fld"><span class="hl lin"> 1293 </span>        tp_min <span class="hl opt">=</span> <span class="hl num">0.1</span></span>
<span id="l_1294" class="hl fld"><span class="hl lin"> 1294 </span></span>
<span id="l_1295" class="hl fld"><span class="hl lin"> 1295 </span>        t0 <span class="hl opt">=</span> <span class="hl kwd">clock</span><span class="hl opt">()</span></span>
<span id="l_1296" class="hl fld"><span class="hl lin"> 1296 </span>        expr_ast <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">.</span><span class="hl kwd">ast_parse</span><span class="hl opt">(</span>expr<span class="hl opt">)</span></span>
<span id="l_1297" class="hl fld"><span class="hl lin"> 1297 </span>        tp <span class="hl opt">=</span> <span class="hl kwd">clock</span><span class="hl opt">()-</span>t0</span>
<span id="l_1298" class="hl fld"><span class="hl lin"> 1298 </span></span>
<span id="l_1299" class="hl fld"><span class="hl lin"> 1299 </span>        <span class="hl slc"># Apply AST transformations</span></span>
<span id="l_1300" class="hl fld"><span class="hl lin"> 1300 </span>        expr_ast <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">transform_ast</span><span class="hl opt">(</span>expr_ast<span class="hl opt">)</span></span>
<span id="l_1301" class="hl fld"><span class="hl lin"> 1301 </span></span>
<span id="l_1302" class="hl fld"><span class="hl lin"> 1302 </span>        <span class="hl slc"># Minimum time above which compilation time will be reported</span></span>
<span id="l_1303" class="hl fld"><span class="hl lin"> 1303 </span>        tc_min <span class="hl opt">=</span> <span class="hl num">0.1</span></span>
<span id="l_1304" class="hl fld"><span class="hl lin"> 1304 </span></span>
<span id="l_1305" class="hl fld"><span class="hl lin"> 1305 </span>        expr_val<span class="hl opt">=</span><span class="hl kwa">None</span></span>
<span id="l_1306" class="hl fld"><span class="hl lin"> 1306 </span>        <span class="hl kwa">if</span> <span class="hl kwb">len</span><span class="hl opt">(</span>expr_ast<span class="hl opt">.</span>body<span class="hl opt">)==</span><span class="hl num">1</span> <span class="hl kwa">and</span> <span class="hl kwb">isinstance</span><span class="hl opt">(</span>expr_ast<span class="hl opt">.</span>body<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">],</span> ast<span class="hl opt">.</span>Expr<span class="hl opt">):</span></span>
<span id="l_1307" class="hl fld"><span class="hl lin"> 1307 </span>            mode <span class="hl opt">=</span> <span class="hl sng">&#39;eval&#39;</span></span>
<span id="l_1308" class="hl fld"><span class="hl lin"> 1308 </span>            source <span class="hl opt">=</span> <span class="hl sng">&#39;&lt;timed eval&gt;&#39;</span></span>
<span id="l_1309" class="hl fld"><span class="hl lin"> 1309 </span>            expr_ast <span class="hl opt">=</span> ast<span class="hl opt">.</span><span class="hl kwd">Expression</span><span class="hl opt">(</span>expr_ast<span class="hl opt">.</span>body<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">].</span>value<span class="hl opt">)</span></span>
<span id="l_1310" class="hl fld"><span class="hl lin"> 1310 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_1311" class="hl fld"><span class="hl lin"> 1311 </span>            mode <span class="hl opt">=</span> <span class="hl sng">&#39;exec&#39;</span></span>
<span id="l_1312" class="hl fld"><span class="hl lin"> 1312 </span>            source <span class="hl opt">=</span> <span class="hl sng">&#39;&lt;timed exec&gt;&#39;</span></span>
<span id="l_1313" class="hl fld"><span class="hl lin"> 1313 </span>            <span class="hl slc"># multi-line %%time case</span></span>
<span id="l_1314" class="hl fld"><span class="hl lin"> 1314 </span>            <span class="hl kwa">if</span> <span class="hl kwb">len</span><span class="hl opt">(</span>expr_ast<span class="hl opt">.</span>body<span class="hl opt">) &gt;</span> <span class="hl num">1</span> <span class="hl kwa">and</span> <span class="hl kwb">isinstance</span><span class="hl opt">(</span>expr_ast<span class="hl opt">.</span>body<span class="hl opt">[-</span><span class="hl num">1</span><span class="hl opt">],</span> ast<span class="hl opt">.</span>Expr<span class="hl opt">):</span></span>
<span id="l_1315" class="hl fld"><span class="hl lin"> 1315 </span>                expr_val<span class="hl opt">=</span> expr_ast<span class="hl opt">.</span>body<span class="hl opt">[-</span><span class="hl num">1</span><span class="hl opt">]</span></span>
<span id="l_1316" class="hl fld"><span class="hl lin"> 1316 </span>                expr_ast <span class="hl opt">=</span> expr_ast<span class="hl opt">.</span>body<span class="hl opt">[:-</span><span class="hl num">1</span><span class="hl opt">]</span></span>
<span id="l_1317" class="hl fld"><span class="hl lin"> 1317 </span>                expr_ast <span class="hl opt">=</span> <span class="hl kwd">Module</span><span class="hl opt">(</span>expr_ast<span class="hl opt">, [])</span></span>
<span id="l_1318" class="hl fld"><span class="hl lin"> 1318 </span>                expr_val <span class="hl opt">=</span> ast<span class="hl opt">.</span><span class="hl kwd">Expression</span><span class="hl opt">(</span>expr_val<span class="hl opt">.</span>value<span class="hl opt">)</span></span>
<span id="l_1319" class="hl fld"><span class="hl lin"> 1319 </span></span>
<span id="l_1320" class="hl fld"><span class="hl lin"> 1320 </span>        t0 <span class="hl opt">=</span> <span class="hl kwd">clock</span><span class="hl opt">()</span></span>
<span id="l_1321" class="hl fld"><span class="hl lin"> 1321 </span>        code <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">(</span>expr_ast<span class="hl opt">,</span> source<span class="hl opt">,</span> mode<span class="hl opt">)</span></span>
<span id="l_1322" class="hl fld"><span class="hl lin"> 1322 </span>        tc <span class="hl opt">=</span> <span class="hl kwd">clock</span><span class="hl opt">()-</span>t0</span>
<span id="l_1323" class="hl fld"><span class="hl lin"> 1323 </span></span>
<span id="l_1324" class="hl fld"><span class="hl lin"> 1324 </span>        <span class="hl slc"># skew measurement as little as possible</span></span>
<span id="l_1325" class="hl fld"><span class="hl lin"> 1325 </span>        glob <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns</span>
<span id="l_1326" class="hl fld"><span class="hl lin"> 1326 </span>        wtime <span class="hl opt">=</span> time<span class="hl opt">.</span>time</span>
<span id="l_1327" class="hl fld"><span class="hl lin"> 1327 </span>        <span class="hl slc"># time execution</span></span>
<span id="l_1328" class="hl fld"><span class="hl lin"> 1328 </span>        wall_st <span class="hl opt">=</span> <span class="hl kwd">wtime</span><span class="hl opt">()</span></span>
<span id="l_1329" class="hl fld"><span class="hl lin"> 1329 </span>        <span class="hl kwa">if</span> mode<span class="hl opt">==</span><span class="hl sng">&#39;eval&#39;</span><span class="hl opt">:</span></span>
<span id="l_1330" class="hl fld"><span class="hl lin"> 1330 </span>            st <span class="hl opt">=</span> <span class="hl kwd">clock2</span><span class="hl opt">()</span></span>
<span id="l_1331" class="hl fld"><span class="hl lin"> 1331 </span>            <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_1332" class="hl fld"><span class="hl lin"> 1332 </span>                out <span class="hl opt">=</span> <span class="hl kwb">eval</span><span class="hl opt">(</span>code<span class="hl opt">,</span> glob<span class="hl opt">,</span> local_ns<span class="hl opt">)</span></span>
<span id="l_1333" class="hl fld"><span class="hl lin"> 1333 </span>            <span class="hl kwa">except</span><span class="hl opt">:</span></span>
<span id="l_1334" class="hl fld"><span class="hl lin"> 1334 </span>                self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">showtraceback</span><span class="hl opt">()</span></span>
<span id="l_1335" class="hl fld"><span class="hl lin"> 1335 </span>                <span class="hl kwa">return</span></span>
<span id="l_1336" class="hl fld"><span class="hl lin"> 1336 </span>            end <span class="hl opt">=</span> <span class="hl kwd">clock2</span><span class="hl opt">()</span></span>
<span id="l_1337" class="hl fld"><span class="hl lin"> 1337 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_1338" class="hl fld"><span class="hl lin"> 1338 </span>            st <span class="hl opt">=</span> <span class="hl kwd">clock2</span><span class="hl opt">()</span></span>
<span id="l_1339" class="hl fld"><span class="hl lin"> 1339 </span>            <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_1340" class="hl fld"><span class="hl lin"> 1340 </span>                <span class="hl kwa">exec</span><span class="hl opt">(</span>code<span class="hl opt">,</span> glob<span class="hl opt">,</span> local_ns<span class="hl opt">)</span></span>
<span id="l_1341" class="hl fld"><span class="hl lin"> 1341 </span>                out<span class="hl opt">=</span><span class="hl kwa">None</span></span>
<span id="l_1342" class="hl fld"><span class="hl lin"> 1342 </span>                <span class="hl slc"># multi-line %%time case</span></span>
<span id="l_1343" class="hl fld"><span class="hl lin"> 1343 </span>                <span class="hl kwa">if</span> expr_val <span class="hl kwa">is not None</span><span class="hl opt">:</span></span>
<span id="l_1344" class="hl fld"><span class="hl lin"> 1344 </span>                    code_2 <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwb">compile</span><span class="hl opt">(</span>expr_val<span class="hl opt">,</span> source<span class="hl opt">,</span> <span class="hl sng">&#39;eval&#39;</span><span class="hl opt">)</span></span>
<span id="l_1345" class="hl fld"><span class="hl lin"> 1345 </span>                    out <span class="hl opt">=</span> <span class="hl kwb">eval</span><span class="hl opt">(</span>code_2<span class="hl opt">,</span> glob<span class="hl opt">,</span> local_ns<span class="hl opt">)</span></span>
<span id="l_1346" class="hl fld"><span class="hl lin"> 1346 </span>            <span class="hl kwa">except</span><span class="hl opt">:</span></span>
<span id="l_1347" class="hl fld"><span class="hl lin"> 1347 </span>                self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">showtraceback</span><span class="hl opt">()</span></span>
<span id="l_1348" class="hl fld"><span class="hl lin"> 1348 </span>                <span class="hl kwa">return</span></span>
<span id="l_1349" class="hl fld"><span class="hl lin"> 1349 </span>            end <span class="hl opt">=</span> <span class="hl kwd">clock2</span><span class="hl opt">()</span></span>
<span id="l_1350" class="hl fld"><span class="hl lin"> 1350 </span></span>
<span id="l_1351" class="hl fld"><span class="hl lin"> 1351 </span>        wall_end <span class="hl opt">=</span> <span class="hl kwd">wtime</span><span class="hl opt">()</span></span>
<span id="l_1352" class="hl fld"><span class="hl lin"> 1352 </span>        <span class="hl slc"># Compute actual times and report</span></span>
<span id="l_1353" class="hl fld"><span class="hl lin"> 1353 </span>        wall_time <span class="hl opt">=</span> wall_end <span class="hl opt">-</span> wall_st</span>
<span id="l_1354" class="hl fld"><span class="hl lin"> 1354 </span>        cpu_user <span class="hl opt">=</span> end<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">] -</span> st<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">]</span></span>
<span id="l_1355" class="hl fld"><span class="hl lin"> 1355 </span>        cpu_sys <span class="hl opt">=</span> end<span class="hl opt">[</span><span class="hl num">1</span><span class="hl opt">] -</span> st<span class="hl opt">[</span><span class="hl num">1</span><span class="hl opt">]</span></span>
<span id="l_1356" class="hl fld"><span class="hl lin"> 1356 </span>        cpu_tot <span class="hl opt">=</span> cpu_user <span class="hl opt">+</span> cpu_sys</span>
<span id="l_1357" class="hl fld"><span class="hl lin"> 1357 </span>        <span class="hl slc"># On windows cpu_sys is always zero, so only total is displayed</span></span>
<span id="l_1358" class="hl fld"><span class="hl lin"> 1358 </span>        <span class="hl kwa">if</span> sys<span class="hl opt">.</span>platform <span class="hl opt">!=</span> <span class="hl sng">&quot;win32&quot;</span><span class="hl opt">:</span></span>
<span id="l_1359" class="hl fld"><span class="hl lin"> 1359 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span></span>
<span id="l_1360" class="hl fld"><span class="hl lin"> 1360 </span>                f<span class="hl sng">&quot;CPU times: user</span> <span class="hl ipl">{_format_time(cpu_user)}</span><span class="hl sng">, sys:</span> <span class="hl ipl">{_format_time(cpu_sys)}</span><span class="hl sng">, total:</span> <span class="hl ipl">{_format_time(cpu_tot)}</span><span class="hl sng">&quot;</span></span>
<span id="l_1361" class="hl fld"><span class="hl lin"> 1361 </span>            <span class="hl opt">)</span></span>
<span id="l_1362" class="hl fld"><span class="hl lin"> 1362 </span>        <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_1363" class="hl fld"><span class="hl lin"> 1363 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span>f<span class="hl sng">&quot;CPU times: total:</span> <span class="hl ipl">{_format_time(cpu_tot)}</span><span class="hl sng">&quot;</span><span class="hl opt">)</span></span>
<span id="l_1364" class="hl fld"><span class="hl lin"> 1364 </span>        <span class="hl kwa">print</span><span class="hl opt">(</span>f<span class="hl sng">&quot;Wall time:</span> <span class="hl ipl">{_format_time(wall_time)}</span><span class="hl sng">&quot;</span><span class="hl opt">)</span></span>
<span id="l_1365" class="hl fld"><span class="hl lin"> 1365 </span>        <span class="hl kwa">if</span> tc <span class="hl opt">&gt;</span> tc_min<span class="hl opt">:</span></span>
<span id="l_1366" class="hl fld"><span class="hl lin"> 1366 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span>f<span class="hl sng">&quot;Compiler :</span> <span class="hl ipl">{_format_time(tc)}</span><span class="hl sng">&quot;</span><span class="hl opt">)</span></span>
<span id="l_1367" class="hl fld"><span class="hl lin"> 1367 </span>        <span class="hl kwa">if</span> tp <span class="hl opt">&gt;</span> tp_min<span class="hl opt">:</span></span>
<span id="l_1368" class="hl fld"><span class="hl lin"> 1368 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span>f<span class="hl sng">&quot;Parser   :</span> <span class="hl ipl">{_format_time(tp)}</span><span class="hl sng">&quot;</span><span class="hl opt">)</span></span>
<span id="l_1369" class="hl fld"><span class="hl lin"> 1369 </span>        <span class="hl kwa">return</span> out</span>
<span id="l_1370" class="hl fld"><span class="hl lin"> 1370 </span></span>
<span id="l_1371" class="hl fld"><span class="hl lin"> 1371 </span>    <span class="hl kwb">&#64;skip_doctest</span></span>
<span id="l_1372" class="hl fld"><span class="hl lin"> 1372 </span>    <span class="hl kwb">&#64;line_magic</span></span>
<span id="l_1373" class="hl fld"><span class="hl lin"> 1373 </span>    <span class="hl kwa">def</span> <span class="hl kwd">macro</span><span class="hl opt">(</span>self<span class="hl opt">,</span> parameter_s<span class="hl opt">=</span><span class="hl sng">&#39;&#39;</span><span class="hl opt">):</span></span>
<span id="l_1374" class="hl fld"><span class="hl lin"> 1374 </span>        <span class="hl sng">&quot;&quot;&quot;Define a macro for future re-execution. It accepts ranges of history,</span></span>
<span id="l_1375" class="hl fld"><span class="hl lin"> 1375 </span><span class="hl sng">        filenames or string objects.</span></span>
<span id="l_1376" class="hl fld"><span class="hl lin"> 1376 </span><span class="hl sng"></span></span>
<span id="l_1377" class="hl fld"><span class="hl lin"> 1377 </span><span class="hl sng">        Usage:</span><span class="hl esc">\\</span></span>
<span id="l_1378" class="hl fld"><span class="hl lin"> 1378 </span><span class="hl sng">          %macro [options] name n1-n2 n3-n4 ... n5 .. n6 ...</span></span>
<span id="l_1379" class="hl fld"><span class="hl lin"> 1379 </span><span class="hl sng"></span></span>
<span id="l_1380" class="hl fld"><span class="hl lin"> 1380 </span><span class="hl sng">        Options:</span></span>
<span id="l_1381" class="hl fld"><span class="hl lin"> 1381 </span><span class="hl sng"></span></span>
<span id="l_1382" class="hl fld"><span class="hl lin"> 1382 </span><span class="hl sng">          -r: use &#39;raw&#39; input.  By default, the &#39;processed&#39; history is used,</span></span>
<span id="l_1383" class="hl fld"><span class="hl lin"> 1383 </span><span class="hl sng">          so that magics are loaded in their transformed version to valid</span></span>
<span id="l_1384" class="hl fld"><span class="hl lin"> 1384 </span><span class="hl sng">          Python.  If this option is given, the raw input as typed at the</span></span>
<span id="l_1385" class="hl fld"><span class="hl lin"> 1385 </span><span class="hl sng">          command line is used instead.</span></span>
<span id="l_1386" class="hl fld"><span class="hl lin"> 1386 </span><span class="hl sng">          </span></span>
<span id="l_1387" class="hl fld"><span class="hl lin"> 1387 </span><span class="hl sng">          -q: quiet macro definition.  By default, a tag line is printed </span></span>
<span id="l_1388" class="hl fld"><span class="hl lin"> 1388 </span><span class="hl sng">          to indicate the macro has been created, and then the contents of </span></span>
<span id="l_1389" class="hl fld"><span class="hl lin"> 1389 </span><span class="hl sng">          the macro are printed.  If this option is given, then no printout</span></span>
<span id="l_1390" class="hl fld"><span class="hl lin"> 1390 </span><span class="hl sng">          is produced once the macro is created.</span></span>
<span id="l_1391" class="hl fld"><span class="hl lin"> 1391 </span><span class="hl sng"></span></span>
<span id="l_1392" class="hl fld"><span class="hl lin"> 1392 </span><span class="hl sng">        This will define a global variable called `name` which is a string</span></span>
<span id="l_1393" class="hl fld"><span class="hl lin"> 1393 </span><span class="hl sng">        made of joining the slices and lines you specify (n1,n2,... numbers</span></span>
<span id="l_1394" class="hl fld"><span class="hl lin"> 1394 </span><span class="hl sng">        above) from your input history into a single string. This variable</span></span>
<span id="l_1395" class="hl fld"><span class="hl lin"> 1395 </span><span class="hl sng">        acts like an automatic function which re-executes those lines as if</span></span>
<span id="l_1396" class="hl fld"><span class="hl lin"> 1396 </span><span class="hl sng">        you had typed them. You just type &#39;name&#39; at the prompt and the code</span></span>
<span id="l_1397" class="hl fld"><span class="hl lin"> 1397 </span><span class="hl sng">        executes.</span></span>
<span id="l_1398" class="hl fld"><span class="hl lin"> 1398 </span><span class="hl sng"></span></span>
<span id="l_1399" class="hl fld"><span class="hl lin"> 1399 </span><span class="hl sng">        The syntax for indicating input ranges is described in %history.</span></span>
<span id="l_1400" class="hl fld"><span class="hl lin"> 1400 </span><span class="hl sng"></span></span>
<span id="l_1401" class="hl fld"><span class="hl lin"> 1401 </span><span class="hl sng">        Note: as a &#39;hidden&#39; feature, you can also use traditional python slice</span></span>
<span id="l_1402" class="hl fld"><span class="hl lin"> 1402 </span><span class="hl sng">        notation, where N:M means numbers N through M-1.</span></span>
<span id="l_1403" class="hl fld"><span class="hl lin"> 1403 </span><span class="hl sng"></span></span>
<span id="l_1404" class="hl fld"><span class="hl lin"> 1404 </span><span class="hl sng">        For example, if your history contains (print using %hist -n )::</span></span>
<span id="l_1405" class="hl fld"><span class="hl lin"> 1405 </span><span class="hl sng"></span></span>
<span id="l_1406" class="hl fld"><span class="hl lin"> 1406 </span><span class="hl sng">          44: x=1</span></span>
<span id="l_1407" class="hl fld"><span class="hl lin"> 1407 </span><span class="hl sng">          45: y=3</span></span>
<span id="l_1408" class="hl fld"><span class="hl lin"> 1408 </span><span class="hl sng">          46: z=x+y</span></span>
<span id="l_1409" class="hl fld"><span class="hl lin"> 1409 </span><span class="hl sng">          47: print x</span></span>
<span id="l_1410" class="hl fld"><span class="hl lin"> 1410 </span><span class="hl sng">          48: a=5</span></span>
<span id="l_1411" class="hl fld"><span class="hl lin"> 1411 </span><span class="hl sng">          49: print &#39;x&#39;,x,&#39;y&#39;,y</span></span>
<span id="l_1412" class="hl fld"><span class="hl lin"> 1412 </span><span class="hl sng"></span></span>
<span id="l_1413" class="hl fld"><span class="hl lin"> 1413 </span><span class="hl sng">        you can create a macro with lines 44 through 47 (included) and line 49</span></span>
<span id="l_1414" class="hl fld"><span class="hl lin"> 1414 </span><span class="hl sng">        called my_macro with::</span></span>
<span id="l_1415" class="hl fld"><span class="hl lin"> 1415 </span><span class="hl sng"></span></span>
<span id="l_1416" class="hl fld"><span class="hl lin"> 1416 </span><span class="hl sng">          In [55]: %macro my_macro 44-47 49</span></span>
<span id="l_1417" class="hl fld"><span class="hl lin"> 1417 </span><span class="hl sng"></span></span>
<span id="l_1418" class="hl fld"><span class="hl lin"> 1418 </span><span class="hl sng">        Now, typing `my_macro` (without quotes) will re-execute all this code</span></span>
<span id="l_1419" class="hl fld"><span class="hl lin"> 1419 </span><span class="hl sng">        in one pass.</span></span>
<span id="l_1420" class="hl fld"><span class="hl lin"> 1420 </span><span class="hl sng"></span></span>
<span id="l_1421" class="hl fld"><span class="hl lin"> 1421 </span><span class="hl sng">        You don&#39;t need to give the line-numbers in order, and any given line</span></span>
<span id="l_1422" class="hl fld"><span class="hl lin"> 1422 </span><span class="hl sng">        number can appear multiple times. You can assemble macros with any</span></span>
<span id="l_1423" class="hl fld"><span class="hl lin"> 1423 </span><span class="hl sng">        lines from your input history in any order.</span></span>
<span id="l_1424" class="hl fld"><span class="hl lin"> 1424 </span><span class="hl sng"></span></span>
<span id="l_1425" class="hl fld"><span class="hl lin"> 1425 </span><span class="hl sng">        The macro is a simple object which holds its value in an attribute,</span></span>
<span id="l_1426" class="hl fld"><span class="hl lin"> 1426 </span><span class="hl sng">        but IPython&#39;s display system checks for macros and executes them as</span></span>
<span id="l_1427" class="hl fld"><span class="hl lin"> 1427 </span><span class="hl sng">        code instead of printing them when you type their name.</span></span>
<span id="l_1428" class="hl fld"><span class="hl lin"> 1428 </span><span class="hl sng"></span></span>
<span id="l_1429" class="hl fld"><span class="hl lin"> 1429 </span><span class="hl sng">        You can view a macro&#39;s contents by explicitly printing it with::</span></span>
<span id="l_1430" class="hl fld"><span class="hl lin"> 1430 </span><span class="hl sng"></span></span>
<span id="l_1431" class="hl fld"><span class="hl lin"> 1431 </span><span class="hl sng">          print macro_name</span></span>
<span id="l_1432" class="hl fld"><span class="hl lin"> 1432 </span><span class="hl sng"></span></span>
<span id="l_1433" class="hl fld"><span class="hl lin"> 1433 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_1434" class="hl fld"><span class="hl lin"> 1434 </span>        opts<span class="hl opt">,</span>args <span class="hl opt">=</span> self<span class="hl opt">.</span><span class="hl kwd">parse_options</span><span class="hl opt">(</span>parameter_s<span class="hl opt">,</span><span class="hl sng">&#39;rq&#39;</span><span class="hl opt">,</span>mode<span class="hl opt">=</span><span class="hl sng">&#39;list&#39;</span><span class="hl opt">)</span></span>
<span id="l_1435" class="hl fld"><span class="hl lin"> 1435 </span>        <span class="hl kwa">if not</span> args<span class="hl opt">:</span>   <span class="hl slc"># List existing macros</span></span>
<span id="l_1436" class="hl fld"><span class="hl lin"> 1436 </span>            <span class="hl kwa">return</span> <span class="hl kwb">sorted</span><span class="hl opt">(</span>k <span class="hl kwa">for</span> k<span class="hl opt">,</span>v <span class="hl kwa">in</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">.</span><span class="hl kwd">items</span><span class="hl opt">()</span> <span class="hl kwa">if</span> <span class="hl kwb">isinstance</span><span class="hl opt">(</span>v<span class="hl opt">,</span> Macro<span class="hl opt">))</span></span>
<span id="l_1437" class="hl fld"><span class="hl lin"> 1437 </span>        <span class="hl kwa">if</span> <span class="hl kwb">len</span><span class="hl opt">(</span>args<span class="hl opt">) ==</span> <span class="hl num">1</span><span class="hl opt">:</span></span>
<span id="l_1438" class="hl fld"><span class="hl lin"> 1438 </span>            <span class="hl kwa">raise</span> <span class="hl kwd">UsageError</span><span class="hl opt">(</span></span>
<span id="l_1439" class="hl fld"><span class="hl lin"> 1439 </span>                <span class="hl sng">&quot;%macro insufficient args; usage &#39;%macro name n1-n2 n3-4...&quot;</span><span class="hl opt">)</span></span>
<span id="l_1440" class="hl fld"><span class="hl lin"> 1440 </span>        name<span class="hl opt">,</span> codefrom <span class="hl opt">=</span> args<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">],</span> <span class="hl sng">&quot; &quot;</span><span class="hl opt">.</span><span class="hl kwd">join</span><span class="hl opt">(</span>args<span class="hl opt">[</span><span class="hl num">1</span><span class="hl opt">:])</span></span>
<span id="l_1441" class="hl fld"><span class="hl lin"> 1441 </span></span>
<span id="l_1442" class="hl fld"><span class="hl lin"> 1442 </span>        <span class="hl slc">#print &#39;rng&#39;,ranges  # dbg</span></span>
<span id="l_1443" class="hl fld"><span class="hl lin"> 1443 </span>        <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_1444" class="hl fld"><span class="hl lin"> 1444 </span>            lines <span class="hl opt">=</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">find_user_code</span><span class="hl opt">(</span>codefrom<span class="hl opt">,</span> <span class="hl sng">&#39;r&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">)</span></span>
<span id="l_1445" class="hl fld"><span class="hl lin"> 1445 </span>        <span class="hl kwa">except</span> <span class="hl opt">(</span><span class="hl kwc">ValueError</span><span class="hl opt">,</span> <span class="hl kwc">TypeError</span><span class="hl opt">)</span> <span class="hl kwa">as</span> e<span class="hl opt">:</span></span>
<span id="l_1446" class="hl fld"><span class="hl lin"> 1446 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span>e<span class="hl opt">.</span>args<span class="hl opt">[</span><span class="hl num">0</span><span class="hl opt">])</span></span>
<span id="l_1447" class="hl fld"><span class="hl lin"> 1447 </span>            <span class="hl kwa">return</span></span>
<span id="l_1448" class="hl fld"><span class="hl lin"> 1448 </span>        macro <span class="hl opt">=</span> <span class="hl kwd">Macro</span><span class="hl opt">(</span>lines<span class="hl opt">)</span></span>
<span id="l_1449" class="hl fld"><span class="hl lin"> 1449 </span>        self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">define_macro</span><span class="hl opt">(</span>name<span class="hl opt">,</span> macro<span class="hl opt">)</span></span>
<span id="l_1450" class="hl fld"><span class="hl lin"> 1450 </span>        <span class="hl kwa">if not</span> <span class="hl opt">(</span> <span class="hl sng">&#39;q&#39;</span> <span class="hl kwa">in</span> opts<span class="hl opt">) :</span> </span>
<span id="l_1451" class="hl fld"><span class="hl lin"> 1451 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&#39;Macro `</span><span class="hl ipl">%s</span><span class="hl sng">` created. To execute, type its name (without quotes).&#39;</span> <span class="hl opt">%</span> name<span class="hl opt">)</span></span>
<span id="l_1452" class="hl fld"><span class="hl lin"> 1452 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl sng">&#39;=== Macro contents: ===&#39;</span><span class="hl opt">)</span></span>
<span id="l_1453" class="hl fld"><span class="hl lin"> 1453 </span>            <span class="hl kwa">print</span><span class="hl opt">(</span>macro<span class="hl opt">,</span> end<span class="hl opt">=</span><span class="hl sng">&#39; &#39;</span><span class="hl opt">)</span></span>
<span id="l_1454" class="hl fld"><span class="hl lin"> 1454 </span></span>
<span id="l_1455" class="hl fld"><span class="hl lin"> 1455 </span>    <span class="hl kwb">&#64;magic_arguments.magic_arguments</span><span class="hl opt">()</span></span>
<span id="l_1456" class="hl fld"><span class="hl lin"> 1456 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span><span class="hl sng">&#39;output&#39;</span><span class="hl opt">,</span> <span class="hl kwb">type</span><span class="hl opt">=</span><span class="hl kwb">str</span><span class="hl opt">,</span> default<span class="hl opt">=</span><span class="hl sng">&#39;&#39;</span><span class="hl opt">,</span> nargs<span class="hl opt">=</span><span class="hl sng">&#39;?&#39;</span><span class="hl opt">,</span></span>
<span id="l_1457" class="hl fld"><span class="hl lin"> 1457 </span>        <span class="hl kwb">help</span><span class="hl opt">=</span><span class="hl sng">&quot;&quot;&quot;The name of the variable in which to store output.</span></span>
<span id="l_1458" class="hl fld"><span class="hl lin"> 1458 </span><span class="hl sng">        This is a utils.io.CapturedIO object with stdout/err attributes</span></span>
<span id="l_1459" class="hl fld"><span class="hl lin"> 1459 </span><span class="hl sng">        for the text of the captured output.</span></span>
<span id="l_1460" class="hl fld"><span class="hl lin"> 1460 </span><span class="hl sng"></span></span>
<span id="l_1461" class="hl fld"><span class="hl lin"> 1461 </span><span class="hl sng">        CapturedOutput also has a show() method for displaying the output,</span></span>
<span id="l_1462" class="hl fld"><span class="hl lin"> 1462 </span><span class="hl sng">        and __call__ as well, so you can use that to quickly display the</span></span>
<span id="l_1463" class="hl fld"><span class="hl lin"> 1463 </span><span class="hl sng">        output.</span></span>
<span id="l_1464" class="hl fld"><span class="hl lin"> 1464 </span><span class="hl sng"></span></span>
<span id="l_1465" class="hl fld"><span class="hl lin"> 1465 </span><span class="hl sng">        If unspecified, captured output is discarded.</span></span>
<span id="l_1466" class="hl fld"><span class="hl lin"> 1466 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_1467" class="hl fld"><span class="hl lin"> 1467 </span>    <span class="hl opt">)</span></span>
<span id="l_1468" class="hl fld"><span class="hl lin"> 1468 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span><span class="hl sng">&#39;--no-stderr&#39;</span><span class="hl opt">,</span> action<span class="hl opt">=</span><span class="hl sng">&quot;store_true&quot;</span><span class="hl opt">,</span></span>
<span id="l_1469" class="hl fld"><span class="hl lin"> 1469 </span>        <span class="hl kwb">help</span><span class="hl opt">=</span><span class="hl sng">&quot;&quot;&quot;Don&#39;t capture stderr.&quot;&quot;&quot;</span></span>
<span id="l_1470" class="hl fld"><span class="hl lin"> 1470 </span>    <span class="hl opt">)</span></span>
<span id="l_1471" class="hl fld"><span class="hl lin"> 1471 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span><span class="hl sng">&#39;--no-stdout&#39;</span><span class="hl opt">,</span> action<span class="hl opt">=</span><span class="hl sng">&quot;store_true&quot;</span><span class="hl opt">,</span></span>
<span id="l_1472" class="hl fld"><span class="hl lin"> 1472 </span>        <span class="hl kwb">help</span><span class="hl opt">=</span><span class="hl sng">&quot;&quot;&quot;Don&#39;t capture stdout.&quot;&quot;&quot;</span></span>
<span id="l_1473" class="hl fld"><span class="hl lin"> 1473 </span>    <span class="hl opt">)</span></span>
<span id="l_1474" class="hl fld"><span class="hl lin"> 1474 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span><span class="hl sng">&#39;--no-display&#39;</span><span class="hl opt">,</span> action<span class="hl opt">=</span><span class="hl sng">&quot;store_true&quot;</span><span class="hl opt">,</span></span>
<span id="l_1475" class="hl fld"><span class="hl lin"> 1475 </span>        <span class="hl kwb">help</span><span class="hl opt">=</span><span class="hl sng">&quot;&quot;&quot;Don&#39;t capture IPython&#39;s rich display.&quot;&quot;&quot;</span></span>
<span id="l_1476" class="hl fld"><span class="hl lin"> 1476 </span>    <span class="hl opt">)</span></span>
<span id="l_1477" class="hl fld"><span class="hl lin"> 1477 </span>    <span class="hl kwb">&#64;cell_magic</span></span>
<span id="l_1478" class="hl fld"><span class="hl lin"> 1478 </span>    <span class="hl kwa">def</span> <span class="hl kwd">capture</span><span class="hl opt">(</span>self<span class="hl opt">,</span> line<span class="hl opt">,</span> cell<span class="hl opt">):</span></span>
<span id="l_1479" class="hl fld"><span class="hl lin"> 1479 </span>        <span class="hl sng">&quot;&quot;&quot;run the cell, capturing stdout, stderr, and IPython&#39;s rich display() calls.&quot;&quot;&quot;</span></span>
<span id="l_1480" class="hl fld"><span class="hl lin"> 1480 </span>        args <span class="hl opt">=</span> magic_arguments<span class="hl opt">.</span><span class="hl kwd">parse_argstring</span><span class="hl opt">(</span>self<span class="hl opt">.</span>capture<span class="hl opt">,</span> line<span class="hl opt">)</span></span>
<span id="l_1481" class="hl fld"><span class="hl lin"> 1481 </span>        out <span class="hl opt">=</span> <span class="hl kwa">not</span> args<span class="hl opt">.</span>no_stdout</span>
<span id="l_1482" class="hl fld"><span class="hl lin"> 1482 </span>        err <span class="hl opt">=</span> <span class="hl kwa">not</span> args<span class="hl opt">.</span>no_stderr</span>
<span id="l_1483" class="hl fld"><span class="hl lin"> 1483 </span>        disp <span class="hl opt">=</span> <span class="hl kwa">not</span> args<span class="hl opt">.</span>no_display</span>
<span id="l_1484" class="hl fld"><span class="hl lin"> 1484 </span>        <span class="hl kwa">with</span> <span class="hl kwd">capture_output</span><span class="hl opt">(</span>out<span class="hl opt">,</span> err<span class="hl opt">,</span> disp<span class="hl opt">)</span> <span class="hl kwa">as</span> io<span class="hl opt">:</span></span>
<span id="l_1485" class="hl fld"><span class="hl lin"> 1485 </span>            self<span class="hl opt">.</span>shell<span class="hl opt">.</span><span class="hl kwd">run_cell</span><span class="hl opt">(</span>cell<span class="hl opt">)</span></span>
<span id="l_1486" class="hl fld"><span class="hl lin"> 1486 </span>        <span class="hl kwa">if</span> DisplayHook<span class="hl opt">.</span><span class="hl kwd">semicolon_at_end_of_expression</span><span class="hl opt">(</span>cell<span class="hl opt">):</span></span>
<span id="l_1487" class="hl fld"><span class="hl lin"> 1487 </span>            <span class="hl kwa">if</span> args<span class="hl opt">.</span>output <span class="hl kwa">in</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">:</span></span>
<span id="l_1488" class="hl fld"><span class="hl lin"> 1488 </span>                <span class="hl kwa">del</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">[</span>args<span class="hl opt">.</span>output<span class="hl opt">]</span></span>
<span id="l_1489" class="hl fld"><span class="hl lin"> 1489 </span>        <span class="hl kwa">elif</span> args<span class="hl opt">.</span>output<span class="hl opt">:</span></span>
<span id="l_1490" class="hl fld"><span class="hl lin"> 1490 </span>            self<span class="hl opt">.</span>shell<span class="hl opt">.</span>user_ns<span class="hl opt">[</span>args<span class="hl opt">.</span>output<span class="hl opt">] =</span> io</span>
<span id="l_1491" class="hl fld"><span class="hl lin"> 1491 </span></span>
<span id="l_1492" class="hl fld"><span class="hl lin"> 1492 </span>    <span class="hl kwb">&#64;skip_doctest</span></span>
<span id="l_1493" class="hl fld"><span class="hl lin"> 1493 </span>    <span class="hl kwb">&#64;magic_arguments.magic_arguments</span><span class="hl opt">()</span></span>
<span id="l_1494" class="hl fld"><span class="hl lin"> 1494 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span><span class="hl sng">&quot;name&quot;</span><span class="hl opt">,</span> <span class="hl kwb">type</span><span class="hl opt">=</span><span class="hl kwb">str</span><span class="hl opt">,</span> default<span class="hl opt">=</span><span class="hl sng">&quot;default&quot;</span><span class="hl opt">,</span> nargs<span class="hl opt">=</span><span class="hl sng">&quot;?&quot;</span><span class="hl opt">)</span></span>
<span id="l_1495" class="hl fld"><span class="hl lin"> 1495 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span></span>
<span id="l_1496" class="hl fld"><span class="hl lin"> 1496 </span>        <span class="hl sng">&quot;--remove&quot;</span><span class="hl opt">,</span> action<span class="hl opt">=</span><span class="hl sng">&quot;store_true&quot;</span><span class="hl opt">,</span> <span class="hl kwb">help</span><span class="hl opt">=</span><span class="hl sng">&quot;remove the current transformer&quot;</span></span>
<span id="l_1497" class="hl fld"><span class="hl lin"> 1497 </span>    <span class="hl opt">)</span></span>
<span id="l_1498" class="hl fld"><span class="hl lin"> 1498 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span></span>
<span id="l_1499" class="hl fld"><span class="hl lin"> 1499 </span>        <span class="hl sng">&quot;--list&quot;</span><span class="hl opt">,</span> action<span class="hl opt">=</span><span class="hl sng">&quot;store_true&quot;</span><span class="hl opt">,</span> <span class="hl kwb">help</span><span class="hl opt">=</span><span class="hl sng">&quot;list existing transformers name&quot;</span></span>
<span id="l_1500" class="hl fld"><span class="hl lin"> 1500 </span>    <span class="hl opt">)</span></span>
<span id="l_1501" class="hl fld"><span class="hl lin"> 1501 </span>    <span class="hl kwb">&#64;magic_arguments.argument</span><span class="hl opt">(</span></span>
<span id="l_1502" class="hl fld"><span class="hl lin"> 1502 </span>        <span class="hl sng">&quot;--list-all&quot;</span><span class="hl opt">,</span></span>
<span id="l_1503" class="hl fld"><span class="hl lin"> 1503 </span>        action<span class="hl opt">=</span><span class="hl sng">&quot;store_true&quot;</span><span class="hl opt">,</span></span>
<span id="l_1504" class="hl fld"><span class="hl lin"> 1504 </span>        <span class="hl kwb">help</span><span class="hl opt">=</span><span class="hl sng">&quot;list existing transformers name and code template&quot;</span><span class="hl opt">,</span></span>
<span id="l_1505" class="hl fld"><span class="hl lin"> 1505 </span>    <span class="hl opt">)</span></span>
<span id="l_1506" class="hl fld"><span class="hl lin"> 1506 </span>    <span class="hl kwb">&#64;line_cell_magic</span></span>
<span id="l_1507" class="hl fld"><span class="hl lin"> 1507 </span>    <span class="hl kwa">def</span> <span class="hl kwd">code_wrap</span><span class="hl opt">(</span>self<span class="hl opt">,</span> line<span class="hl opt">,</span> cell<span class="hl opt">=</span><span class="hl kwa">None</span><span class="hl opt">):</span></span>
<span id="l_1508" class="hl fld"><span class="hl lin"> 1508 </span>        <span class="hl sng">&quot;&quot;&quot;</span></span>
<span id="l_1509" class="hl fld"><span class="hl lin"> 1509 </span><span class="hl sng">        Simple magic to quickly define a code transformer for all IPython&#39;s future imput.</span></span>
<span id="l_1510" class="hl fld"><span class="hl lin"> 1510 </span><span class="hl sng"></span></span>
<span id="l_1511" class="hl fld"><span class="hl lin"> 1511 </span><span class="hl sng">        ``__code__`` and ``__ret__`` are special variable that represent the code to run</span></span>
<span id="l_1512" class="hl fld"><span class="hl lin"> 1512 </span><span class="hl sng">        and the value of the last expression of ``__code__`` respectively.</span></span>
<span id="l_1513" class="hl fld"><span class="hl lin"> 1513 </span><span class="hl sng"></span></span>
<span id="l_1514" class="hl fld"><span class="hl lin"> 1514 </span><span class="hl sng">        Examples</span></span>
<span id="l_1515" class="hl fld"><span class="hl lin"> 1515 </span><span class="hl sng">        --------</span></span>
<span id="l_1516" class="hl fld"><span class="hl lin"> 1516 </span><span class="hl sng"></span></span>
<span id="l_1517" class="hl fld"><span class="hl lin"> 1517 </span><span class="hl sng">        .. ipython::</span></span>
<span id="l_1518" class="hl fld"><span class="hl lin"> 1518 </span><span class="hl sng"></span></span>
<span id="l_1519" class="hl fld"><span class="hl lin"> 1519 </span><span class="hl sng">            In [1]:</span> <span class="hl ipl">%%code</span><span class="hl sng">_wrap before_after</span></span>
<span id="l_1520" class="hl fld"><span class="hl lin"> 1520 </span><span class="hl sng">               ...: print(&#39;before&#39;)</span></span>
<span id="l_1521" class="hl fld"><span class="hl lin"> 1521 </span><span class="hl sng">               ...: __code__</span></span>
<span id="l_1522" class="hl fld"><span class="hl lin"> 1522 </span><span class="hl sng">               ...: print(&#39;after&#39;)</span></span>
<span id="l_1523" class="hl fld"><span class="hl lin"> 1523 </span><span class="hl sng">               ...: __ret__</span></span>
<span id="l_1524" class="hl fld"><span class="hl lin"> 1524 </span><span class="hl sng"></span></span>
<span id="l_1525" class="hl fld"><span class="hl lin"> 1525 </span><span class="hl sng"></span></span>
<span id="l_1526" class="hl fld"><span class="hl lin"> 1526 </span><span class="hl sng">            In [2]: 1</span></span>
<span id="l_1527" class="hl fld"><span class="hl lin"> 1527 </span><span class="hl sng">            before</span></span>
<span id="l_1528" class="hl fld"><span class="hl lin"> 1528 </span><span class="hl sng">            after</span></span>
<span id="l_1529" class="hl fld"><span class="hl lin"> 1529 </span><span class="hl sng">            Out[2]: 1</span></span>
<span id="l_1530" class="hl fld"><span class="hl lin"> 1530 </span><span class="hl sng"></span></span>
<span id="l_1531" class="hl fld"><span class="hl lin"> 1531 </span><span class="hl sng">            In [3]:</span> <span class="hl ipl">%code</span><span class="hl sng">_wrap --list</span></span>
<span id="l_1532" class="hl fld"><span class="hl lin"> 1532 </span><span class="hl sng">            before_after</span></span>
<span id="l_1533" class="hl fld"><span class="hl lin"> 1533 </span><span class="hl sng"></span></span>
<span id="l_1534" class="hl fld"><span class="hl lin"> 1534 </span><span class="hl sng">            In [4]:</span> <span class="hl ipl">%code</span><span class="hl sng">_wrap --list-all</span></span>
<span id="l_1535" class="hl fld"><span class="hl lin"> 1535 </span><span class="hl sng">            before_after :</span></span>
<span id="l_1536" class="hl fld"><span class="hl lin"> 1536 </span><span class="hl sng">                print(&#39;before&#39;)</span></span>
<span id="l_1537" class="hl fld"><span class="hl lin"> 1537 </span><span class="hl sng">                __code__</span></span>
<span id="l_1538" class="hl fld"><span class="hl lin"> 1538 </span><span class="hl sng">                print(&#39;after&#39;)</span></span>
<span id="l_1539" class="hl fld"><span class="hl lin"> 1539 </span><span class="hl sng">                __ret__</span></span>
<span id="l_1540" class="hl fld"><span class="hl lin"> 1540 </span><span class="hl sng"></span></span>
<span id="l_1541" class="hl fld"><span class="hl lin"> 1541 </span><span class="hl sng">            In [5]:</span> <span class="hl ipl">%code</span><span class="hl sng">_wrap --remove before_after</span></span>
<span id="l_1542" class="hl fld"><span class="hl lin"> 1542 </span><span class="hl sng"></span></span>
<span id="l_1543" class="hl fld"><span class="hl lin"> 1543 </span><span class="hl sng">        &quot;&quot;&quot;</span></span>
<span id="l_1544" class="hl fld"><span class="hl lin"> 1544 </span>        args <span class="hl opt">=</span> magic_arguments<span class="hl opt">.</span><span class="hl kwd">parse_argstring</span><span class="hl opt">(</span>self<span class="hl opt">.</span>code_wrap<span class="hl opt">,</span> line<span class="hl opt">)</span></span>
<span id="l_1545" class="hl fld"><span class="hl lin"> 1545 </span></span>
<span id="l_1546" class="hl fld"><span class="hl lin"> 1546 </span>        <span class="hl kwa">if</span> args<span class="hl opt">.</span><span class="hl kwb">list</span><span class="hl opt">:</span></span>
<span id="l_1547" class="hl fld"><span class="hl lin"> 1547 </span>            <span class="hl kwa">for</span> name <span class="hl kwa">in</span> self<span class="hl num">._</span>transformers<span class="hl opt">.</span><span class="hl kwd">keys</span><span class="hl opt">():</span></span>
<span id="l_1548" class="hl fld"><span class="hl lin"> 1548 </span>                <span class="hl kwa">print</span><span class="hl opt">(</span>name<span class="hl opt">)</span></span>
<span id="l_1549" class="hl fld"><span class="hl lin"> 1549 </span>            <span class="hl kwa">return</span></span>
<span id="l_1550" class="hl fld"><span class="hl lin"> 1550 </span>        <span class="hl kwa">if</span> args<span class="hl opt">.</span>list_all<span class="hl opt">:</span></span>
<span id="l_1551" class="hl fld"><span class="hl lin"> 1551 </span>            <span class="hl kwa">for</span> name<span class="hl opt">,</span> _t <span class="hl kwa">in</span> self<span class="hl num">._</span>transformers<span class="hl opt">.</span><span class="hl kwd">items</span><span class="hl opt">():</span></span>
<span id="l_1552" class="hl fld"><span class="hl lin"> 1552 </span>                <span class="hl kwa">print</span><span class="hl opt">(</span>name<span class="hl opt">,</span> <span class="hl sng">&quot;:&quot;</span><span class="hl opt">)</span></span>
<span id="l_1553" class="hl fld"><span class="hl lin"> 1553 </span>                <span class="hl kwa">print</span><span class="hl opt">(</span><span class="hl kwd">indent</span><span class="hl opt">(</span>ast<span class="hl opt">.</span><span class="hl kwd">unparse</span><span class="hl opt">(</span>_t<span class="hl opt">.</span>template<span class="hl opt">),</span> <span class="hl sng">&quot;    &quot;</span><span class="hl opt">))</span></span>
<span id="l_1554" class="hl fld"><span class="hl lin"> 1554 </span>            <span class="hl kwa">print</span><span class="hl opt">()</span></span>
<span id="l_1555" class="hl fld"><span class="hl lin"> 1555 </span>            <span class="hl kwa">return</span></span>
<span id="l_1556" class="hl fld"><span class="hl lin"> 1556 </span></span>
<span id="l_1557" class="hl fld"><span class="hl lin"> 1557 </span>        to_remove <span class="hl opt">=</span> self<span class="hl num">._</span>transformers<span class="hl opt">.</span><span class="hl kwd">pop</span><span class="hl opt">(</span>args<span class="hl opt">.</span>name<span class="hl opt">,</span> <span class="hl kwa">None</span><span class="hl opt">)</span></span>
<span id="l_1558" class="hl fld"><span class="hl lin"> 1558 </span>        <span class="hl kwa">if</span> to_remove <span class="hl kwa">in</span> self<span class="hl opt">.</span>shell<span class="hl opt">.</span>ast_transformers<span class="hl opt">:</span></span>
<span id="l_1559" class="hl fld"><span class="hl lin"> 1559 </span>            self<span class="hl opt">.</span>shell<span class="hl opt">.</span>ast_transformers<span class="hl opt">.</span><span class="hl kwd">remove</span><span class="hl opt">(</span>to_remove<span class="hl opt">)</span></span>
<span id="l_1560" class="hl fld"><span class="hl lin"> 1560 </span>        <span class="hl kwa">if</span> cell <span class="hl kwa">is None or</span> args<span class="hl opt">.</span>remove<span class="hl opt">:</span></span>
<span id="l_1561" class="hl fld"><span class="hl lin"> 1561 </span>            <span class="hl kwa">return</span></span>
<span id="l_1562" class="hl fld"><span class="hl lin"> 1562 </span></span>
<span id="l_1563" class="hl fld"><span class="hl lin"> 1563 </span>        _trs <span class="hl opt">=</span> <span class="hl kwd">ReplaceCodeTransformer</span><span class="hl opt">(</span>ast<span class="hl opt">.</span><span class="hl kwd">parse</span><span class="hl opt">(</span>cell<span class="hl opt">))</span></span>
<span id="l_1564" class="hl fld"><span class="hl lin"> 1564 </span></span>
<span id="l_1565" class="hl fld"><span class="hl lin"> 1565 </span>        self<span class="hl num">._</span>transformers<span class="hl opt">[</span>args<span class="hl opt">.</span>name<span class="hl opt">] =</span> _trs</span>
<span id="l_1566" class="hl fld"><span class="hl lin"> 1566 </span>        self<span class="hl opt">.</span>shell<span class="hl opt">.</span>ast_transformers<span class="hl opt">.</span><span class="hl kwd">append</span><span class="hl opt">(</span>_trs<span class="hl opt">)</span></span>
<span id="l_1567" class="hl fld"><span class="hl lin"> 1567 </span></span>
<span id="l_1568" class="hl fld"><span class="hl lin"> 1568 </span></span>
<span id="l_1569" class="hl fld"><span class="hl lin"> 1569 </span><span class="hl kwa">def</span> <span class="hl kwd">parse_breakpoint</span><span class="hl opt">(</span>text<span class="hl opt">,</span> current_file<span class="hl opt">):</span></span>
<span id="l_1570" class="hl fld"><span class="hl lin"> 1570 </span>    <span class="hl sng">&#39;&#39;&#39;Returns (file, line) for file:line and (current_file, line) for line&#39;&#39;&#39;</span></span>
<span id="l_1571" class="hl fld"><span class="hl lin"> 1571 </span>    colon <span class="hl opt">=</span> text<span class="hl opt">.</span><span class="hl kwd">find</span><span class="hl opt">(</span><span class="hl sng">&#39;:&#39;</span><span class="hl opt">)</span></span>
<span id="l_1572" class="hl fld"><span class="hl lin"> 1572 </span>    <span class="hl kwa">if</span> colon <span class="hl opt">== -</span><span class="hl num">1</span><span class="hl opt">:</span></span>
<span id="l_1573" class="hl fld"><span class="hl lin"> 1573 </span>        <span class="hl kwa">return</span> current_file<span class="hl opt">,</span> <span class="hl kwb">int</span><span class="hl opt">(</span>text<span class="hl opt">)</span></span>
<span id="l_1574" class="hl fld"><span class="hl lin"> 1574 </span>    <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_1575" class="hl fld"><span class="hl lin"> 1575 </span>        <span class="hl kwa">return</span> text<span class="hl opt">[:</span>colon<span class="hl opt">],</span> <span class="hl kwb">int</span><span class="hl opt">(</span>text<span class="hl opt">[</span>colon<span class="hl opt">+</span><span class="hl num">1</span><span class="hl opt">:])</span></span>
<span id="l_1576" class="hl fld"><span class="hl lin"> 1576 </span>    </span>
<span id="l_1577" class="hl fld"><span class="hl lin"> 1577 </span><span class="hl kwa">def</span> <span class="hl kwd">_format_time</span><span class="hl opt">(</span>timespan<span class="hl opt">,</span> precision<span class="hl opt">=</span><span class="hl num">3</span><span class="hl opt">):</span></span>
<span id="l_1578" class="hl fld"><span class="hl lin"> 1578 </span>    <span class="hl sng">&quot;&quot;&quot;Formats the timespan in a human readable form&quot;&quot;&quot;</span></span>
<span id="l_1579" class="hl fld"><span class="hl lin"> 1579 </span></span>
<span id="l_1580" class="hl fld"><span class="hl lin"> 1580 </span>    <span class="hl kwa">if</span> timespan <span class="hl opt">&gt;=</span> <span class="hl num">60.0</span><span class="hl opt">:</span></span>
<span id="l_1581" class="hl fld"><span class="hl lin"> 1581 </span>        <span class="hl slc"># we have more than a minute, format that in a human readable form</span></span>
<span id="l_1582" class="hl fld"><span class="hl lin"> 1582 </span>        <span class="hl slc"># Idea from http://snipplr.com/view/5713/</span></span>
<span id="l_1583" class="hl fld"><span class="hl lin"> 1583 </span>        parts <span class="hl opt">= [(</span><span class="hl sng">&quot;d&quot;</span><span class="hl opt">,</span> <span class="hl num">60</span><span class="hl opt">*</span><span class="hl num">60</span><span class="hl opt">*</span><span class="hl num">24</span><span class="hl opt">),(</span><span class="hl sng">&quot;h&quot;</span><span class="hl opt">,</span> <span class="hl num">60</span><span class="hl opt">*</span><span class="hl num">60</span><span class="hl opt">),(</span><span class="hl sng">&quot;min&quot;</span><span class="hl opt">,</span> <span class="hl num">60</span><span class="hl opt">), (</span><span class="hl sng">&quot;s&quot;</span><span class="hl opt">,</span> <span class="hl num">1</span><span class="hl opt">)]</span></span>
<span id="l_1584" class="hl fld"><span class="hl lin"> 1584 </span>        time <span class="hl opt">= []</span></span>
<span id="l_1585" class="hl fld"><span class="hl lin"> 1585 </span>        leftover <span class="hl opt">=</span> timespan</span>
<span id="l_1586" class="hl fld"><span class="hl lin"> 1586 </span>        <span class="hl kwa">for</span> suffix<span class="hl opt">,</span> length <span class="hl kwa">in</span> parts<span class="hl opt">:</span></span>
<span id="l_1587" class="hl fld"><span class="hl lin"> 1587 </span>            value <span class="hl opt">=</span> <span class="hl kwb">int</span><span class="hl opt">(</span>leftover <span class="hl opt">/</span> length<span class="hl opt">)</span></span>
<span id="l_1588" class="hl fld"><span class="hl lin"> 1588 </span>            <span class="hl kwa">if</span> value <span class="hl opt">&gt;</span> <span class="hl num">0</span><span class="hl opt">:</span></span>
<span id="l_1589" class="hl fld"><span class="hl lin"> 1589 </span>                leftover <span class="hl opt">=</span> leftover <span class="hl opt">%</span> length</span>
<span id="l_1590" class="hl fld"><span class="hl lin"> 1590 </span>                time<span class="hl opt">.</span><span class="hl kwd">append</span><span class="hl opt">(</span>u<span class="hl sng">&#39;</span><span class="hl ipl">%s%s</span><span class="hl sng">&#39;</span> <span class="hl opt">% (</span><span class="hl kwb">str</span><span class="hl opt">(</span>value<span class="hl opt">),</span> suffix<span class="hl opt">))</span></span>
<span id="l_1591" class="hl fld"><span class="hl lin"> 1591 </span>            <span class="hl kwa">if</span> leftover <span class="hl opt">&lt;</span> <span class="hl num">1</span><span class="hl opt">:</span></span>
<span id="l_1592" class="hl fld"><span class="hl lin"> 1592 </span>                <span class="hl kwa">break</span></span>
<span id="l_1593" class="hl fld"><span class="hl lin"> 1593 </span>        <span class="hl kwa">return</span> <span class="hl sng">&quot; &quot;</span><span class="hl opt">.</span><span class="hl kwd">join</span><span class="hl opt">(</span>time<span class="hl opt">)</span></span>
<span id="l_1594" class="hl fld"><span class="hl lin"> 1594 </span></span>
<span id="l_1595" class="hl fld"><span class="hl lin"> 1595 </span>    </span>
<span id="l_1596" class="hl fld"><span class="hl lin"> 1596 </span>    <span class="hl slc"># Unfortunately the unicode &#39;micro&#39; symbol can cause problems in</span></span>
<span id="l_1597" class="hl fld"><span class="hl lin"> 1597 </span>    <span class="hl slc"># certain terminals.  </span></span>
<span id="l_1598" class="hl fld"><span class="hl lin"> 1598 </span>    <span class="hl slc"># See bug: https://bugs.launchpad.net/ipython/+bug/348466</span></span>
<span id="l_1599" class="hl fld"><span class="hl lin"> 1599 </span>    <span class="hl slc"># Try to prevent crashes by being more secure than it needs to</span></span>
<span id="l_1600" class="hl fld"><span class="hl lin"> 1600 </span>    <span class="hl slc"># E.g. eclipse is able to print a µ, but has no sys.stdout.encoding set.</span></span>
<span id="l_1601" class="hl fld"><span class="hl lin"> 1601 </span>    units <span class="hl opt">= [</span>u<span class="hl sng">&quot;s&quot;</span><span class="hl opt">,</span> u<span class="hl sng">&quot;ms&quot;</span><span class="hl opt">,</span>u<span class="hl sng">&#39;us&#39;</span><span class="hl opt">,</span><span class="hl sng">&quot;ns&quot;</span><span class="hl opt">]</span> <span class="hl slc"># the save value   </span></span>
<span id="l_1602" class="hl fld"><span class="hl lin"> 1602 </span>    <span class="hl kwa">if</span> <span class="hl kwb">hasattr</span><span class="hl opt">(</span>sys<span class="hl opt">.</span>stdout<span class="hl opt">,</span> <span class="hl sng">&#39;encoding&#39;</span><span class="hl opt">)</span> <span class="hl kwa">and</span> sys<span class="hl opt">.</span>stdout<span class="hl opt">.</span>encoding<span class="hl opt">:</span></span>
<span id="l_1603" class="hl fld"><span class="hl lin"> 1603 </span>        <span class="hl kwa">try</span><span class="hl opt">:</span></span>
<span id="l_1604" class="hl fld"><span class="hl lin"> 1604 </span>            u<span class="hl sng">&#39;</span><span class="hl esc">\xb5</span><span class="hl sng">&#39;</span><span class="hl opt">.</span><span class="hl kwd">encode</span><span class="hl opt">(</span>sys<span class="hl opt">.</span>stdout<span class="hl opt">.</span>encoding<span class="hl opt">)</span></span>
<span id="l_1605" class="hl fld"><span class="hl lin"> 1605 </span>            units <span class="hl opt">= [</span>u<span class="hl sng">&quot;s&quot;</span><span class="hl opt">,</span> u<span class="hl sng">&quot;ms&quot;</span><span class="hl opt">,</span>u<span class="hl sng">&#39;</span><span class="hl esc">\xb5</span><span class="hl sng">s&#39;</span><span class="hl opt">,</span><span class="hl sng">&quot;ns&quot;</span><span class="hl opt">]</span></span>
<span id="l_1606" class="hl fld"><span class="hl lin"> 1606 </span>        <span class="hl kwa">except</span><span class="hl opt">:</span></span>
<span id="l_1607" class="hl fld"><span class="hl lin"> 1607 </span>            <span class="hl kwa">pass</span></span>
<span id="l_1608" class="hl fld"><span class="hl lin"> 1608 </span>    scaling <span class="hl opt">= [</span><span class="hl num">1</span><span class="hl opt">,</span> <span class="hl num">1</span>e3<span class="hl opt">,</span> <span class="hl num">1</span>e6<span class="hl opt">,</span> <span class="hl num">1</span>e9<span class="hl opt">]</span></span>
<span id="l_1609" class="hl fld"><span class="hl lin"> 1609 </span>        </span>
<span id="l_1610" class="hl fld"><span class="hl lin"> 1610 </span>    <span class="hl kwa">if</span> timespan <span class="hl opt">&gt;</span> <span class="hl num">0.0</span><span class="hl opt">:</span></span>
<span id="l_1611" class="hl fld"><span class="hl lin"> 1611 </span>        order <span class="hl opt">=</span> <span class="hl kwb">min</span><span class="hl opt">(-</span><span class="hl kwb">int</span><span class="hl opt">(</span>math<span class="hl opt">.</span><span class="hl kwd">floor</span><span class="hl opt">(</span>math<span class="hl opt">.</span><span class="hl kwd">log10</span><span class="hl opt">(</span>timespan<span class="hl opt">)) //</span> <span class="hl num">3</span><span class="hl opt">),</span> <span class="hl num">3</span><span class="hl opt">)</span></span>
<span id="l_1612" class="hl fld"><span class="hl lin"> 1612 </span>    <span class="hl kwa">else</span><span class="hl opt">:</span></span>
<span id="l_1613" class="hl fld"><span class="hl lin"> 1613 </span>        order <span class="hl opt">=</span> <span class="hl num">3</span></span>
<span id="l_1614" class="hl fld"><span class="hl lin"> 1614 </span>    <span class="hl kwa">return</span> <span class="hl sng">&quot;%.*g</span> <span class="hl ipl">%s</span><span class="hl sng">&quot;</span> <span class="hl opt">% (</span>precision<span class="hl opt">,</span> timespan <span class="hl opt">*</span> scaling<span class="hl opt">[</span>order<span class="hl opt">],</span> units<span class="hl opt">[</span>order<span class="hl opt">])</span></span>
</pre></BODY></HTML><!--HTML generated by highlight, http://www.andre-simon.de/-->
