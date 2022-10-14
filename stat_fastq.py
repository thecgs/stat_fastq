#!/usr/bin/env python
# coding: utf-8

import os
import re
import sys
import subprocess
import pandas as pd
from concurrent.futures import ProcessPoolExecutor as pool

verison = "v2.00"
usage = f"""
\033[36mUsage:\033[0m
    \033[36mexample 1:\033[0m
    {sys.argv[0]} <fastq.fofn> [option]
    \033[36mexample 2:\033[0m
    {sys.argv[0]} <file.fastq.gz> [option]
    \033[36mexample 3:\033[0m
    {sys.argv[0]} <file.fastq1.gz> [file.fastq2.gz] [file.fastq3.gz] ... [option]
    
\033[36mOption:\033[0m
    -t   --Transposition  Transposition Stdout format [default: Vertical]
    -d   --Distribution   Open output "Reads length distribution" file [default: Close]
    -n   --Reads_Num      Close ouput Reads of Number [default: Open]
    -b   --Reads_Base     Close ouput Reads of Bese Number [default: Open]
    -10  --Q10            Close ouput Q10 [default: Open]
    -20  --Q20            Close ouput Q20 [default: Open]
    -30  --Q30            Close ouput Q30 [default: Open]
    -40  --Q40            Close ouput Q40 [default: Open]
    -qmi --Min_qual       Close ouput Min quality value [default: Open]
    -qma --Max_qual       Close ouput Max quality value [default: Open]
    -AT  --AT_Bases       Close ouput AT Beses of Number [default: Open]
    -GC  --GC_Bases       Close ouput GC Beses of Number [default: Open]
    -A   --A_Bases        Close ouput A Beses of Number [default: Open]
    -T   --T_Bases        Close ouput T Beses of Number [default: Open]
    -G   --G_Bases        Close ouput G Beses of Number [default: Open]
    -C   --C_Bases        Close ouput C Beses of Number [default: Open]
    -N   --N_Bases        Close ouput N Beses of Number [default: Open]
    -lmi --Min_len        Close ouput Read length Min value [default: Open]
    -lma --Max_len        Close ouput Read length Max value [default: Open]
    -lme --Mean_len       Close ouput Read length Mean value [default: Open]
    -p   --Phread_Type    Close ouput Phread Type [default: Open]
    -h   --help           Show the help message and exit
    -v   --version        Show the version message

Note: The [option] can be anywhere
Datetime: 2022/10/12; Author: Guisen Chen; Email: thecgs001@foxmail.com; Cite: https://github.com/thecgs/stat_fastq
"""

def get_params(argv: set):
    params = []
    argv = set(argv)
    for s in argv:
        if re.findall('^-.*',s) == []:
            pass
        else:
            param = re.findall('^-.*',s)[0]
            params.append(param)
            sys.argv.remove(param)
    return params

def prefix(name: str):
    """
    移去一个后缀
    """
    prefix = re.sub('\.[^.]*$','',name)
    return prefix

def is_fofn():
    """
    判断是否是一个fastq的文件列表
    """
    try:
        with open(sys.argv[1],'r') as f:
            if f.read(1) == '@':
                result = False
            else:
                result = True
    except UnicodeDecodeError:
        result = False
    return result

def run_stat_fastq(fastq: str):
    Sample = os.path.basename(prefix(prefix(fastq)))
    cmd = subprocess.run(f'/usr/bin/zcat {fastq} | {os.path.dirname(sys.argv[0])}/stat_fastq -',\
                         stdout=subprocess.PIPE, shell=True)
    result = cmd.stdout.decode()
    tmp = []
    for l in result.split('\n'):
        if l == '':
            pass
        else:
            tmp.append(l.strip())
    Base_stat_dict = {}
    for i in range(0, 19):
        Base_stat_dict[tmp[i].split('\t')[0]] = tmp[i].split('\t')[1]
    stat = pd.Series(Base_stat_dict, name=Sample)
    if "-d" in params or "--Distribution" in params:
        with open(f'{Sample}.Reads_Length_Distribution.tsv','w') as f:
            f.write('Reads of Length(nt)\tReads of Number\tReads of Frequence Precent(%)\n')
            for i in range(20, len(tmp)):
                f.write(f'{tmp[i]}\n')
    return stat

def main(fastq_list: list):
    """
    主程序多线程运行
    """
    isfofn = is_fofn()
    if isfofn == True:
        fofns = []
        with open(fastq_list[0]) as f:
            for l in f:
                fofns.append(l.strip())
        fastq_list = fofns
    if len(fastq_list) == 1:
        res=run_stat_fastq(fastq_list[0])
        stat = pd.DataFrame(res).T
    else:
        if 4 < os.cpu_count():
            thread = 4
        else:
            thread = os.cpu_count()
        with pool(max_workers=thread) as t:
            res = t.map(run_stat_fastq, fastq_list)
            tmp = []
            for i in res:
                tmp.append(i)
            stat = pd.DataFrame(tmp)
    indexs = {'Reads_Num':['-n','--Reads_Num'], \
              'Reads_Base(nt)':['-b','--Reads_Base'], \
              'Q10(%)':['-10','--Q10'], \
              'Q20(%)':['-20','--Q20'], \
              'Q30(%)':['-30','--Q30'], \
              'Q40(%)':['-40','--Q40'], \
              'Min_qual':['-qmi', '--Min_qual'], \
              'Max_qual':['-qma', '--Max_qual'], \
              'AT_Bases(%)':['-AT', '--AT_Bases'], \
              'GC_Bases(%)':['-GC', '--GC_Bases'], \
              'A_Bases(%)':['-A', '--A_Bases'], \
              'T_Bases(%)':['-T', '--T_Bases'], \
              'G_Bases(%)':['-G', '--G_Bases'], \
              'C_Bases(%)':['-C', '--C_Bases'], \
              'N_Bases(%)':['-N', '--N_Bases'],\
              'Min_len':['-lmi', '--Min_len'], \
              'Max_len':['-lma', '--Max_len'], \
              'Mean_len':['-lme', '--Mean_len'], \
              'Phread_Type':['-p', '--Phread_Type']}
    for key, value in indexs.items():
        if value[0] in params or value[1] in params:
            stat = stat.drop(str(key), axis=1)
    if '-t' in params or '--Transposition' in params:
        print(stat)
    else:
        print(stat.T)

pd.set_option('display.width',1000)
pd.set_option('display.max_columns',1000)
params = get_params(sys.argv)
if '-h' in params or '--help' in params:
    print(usage)
    sys.exit()
if len(sys.argv) ==1 and params == []:
    print(usage)
    sys.exit()
if '-v' in params or '--verison' in params:
    print(verison)
    sys.exit()

main(sys.argv[1:])