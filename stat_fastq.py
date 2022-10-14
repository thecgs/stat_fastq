import os
import re
import sys
import gzip
import pyfastx
import pandas as pd
from concurrent.futures import ThreadPoolExecutor as pool

usage = f"""
usage:
    example 1:
    {sys.argv[0]} <file.fastq>
    example 2:
    {sys.argv[0]} <file.fastq.gz>
    example 3:
    {sys.argv[0]} <fastq.fofn>
    example 4:
    {sys.argv[0]} <file.fastq1.gz> [file.fastq2.gz] [file.fastq3.gz] ...
datetime: 2022/10/12; author: Guisen Chen; email: thecgs001@foxmail.com 
"""

if len(sys.argv) == 1:
    print(usage)
    sys.exit()

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
    except:
        result = False
    return result

def stat_fastq(fastq: str):
    """
    统计fastq
    """
    fq = pyfastx.Fastq(fastq, build_index=False)
    phread = fq.phred
    Sample = prefix(prefix(os.path.basename(fastq)))
    counts = {}
    Reads_Num = 0
    Reads_Base = 0
    N_Bases = 0
    A_Bases = 0 
    T_Bases = 0
    G_Bases = 0 
    C_Bases = 0
    Q10_Bases = 0
    Q20_Bases = 0
    Q30_Bases = 0
    Q40_Bases = 0
    Min_qual = 1000
    Max_qual = 0
    for read in fq:
        name, seq, quals = read
        for s in quals:
            quali = ord(s)-phread
            if Min_qual > quali:
                Min_qual = quali
            if Max_qual < quali:
                Max_qual = quali
            if quali >= 10:
                Q10_Bases += 1
            if quali >= 20:
                Q20_Bases += 1
            if quali >= 30:
                Q30_Bases += 1
            if quali >= 40:
                Q40_Bases += 1
        N_Bases += seq.count('N')
        A_Bases += seq.count('A')
        T_Bases += seq.count('T')
        G_Bases += seq.count('G')
        C_Bases += seq.count('C')
        Reads_Num += 1
        #print(Reads_Num)
        Reads_Base += len(seq)
        if len(seq) not in counts:
            counts[len(seq)] = 1
        elif len(seq) in counts:
            counts[len(seq)] +=1
    Min_len = min(counts.keys())
    Max_len = max(counts.keys())
    Mean_len = round(sum(map(lambda x: x[0]*x[1], counts.items()))/sum(counts.values()), 2)
    Q10 = round(Q10_Bases/Reads_Base*100, 2)
    Q20 = round(Q20_Bases/Reads_Base*100, 2)
    Q30 = round(Q30_Bases/Reads_Base*100, 2)
    Q40 = round(Q40_Bases/Reads_Base*100, 2)
    N_content = round(N_Bases/Reads_Base*100, 2)
    A_content = round(A_Bases/Reads_Base*100, 2) 
    T_content = round(T_Bases/Reads_Base*100, 2) 
    G_content = round(G_Bases/Reads_Base*100, 2) 
    C_content = round(C_Bases/Reads_Base*100, 2)
    GC_content = round((G_Bases+C_Bases)/Reads_Base*100, 2)
    AT_content = round((A_Bases+T_Bases)/Reads_Base*100, 2)

    indexs = ['Reads_Num','Reads_Base(nt)','Q10(%)','Q20(%)','Q30(%)','Q40(%)',\
            'Min_qual','Max_qual','AT(%)','GC(%)','A(%)','T(%)','G(%)','C(%)','N(%)',\
            'Min_len','Max_len','Mean_len','Phread_Type']
    stat_info = [Reads_Num, Reads_Base, Q10, Q20, Q30, Q40, Min_qual, Max_qual, \
            f'{A_Bases+T_Bases}({AT_content}%)',\
            f'{G_Bases+C_Bases}({GC_content}%)',\
            f'{A_Bases}({A_content}%)',\
            f'{T_Bases}({T_content}%)',\
            f'{G_Bases}({G_content}%)',\
            f'{C_Bases}({C_content}%)',\
            f'{N_Bases}({N_content}%)',\
            Min_len, Max_len, Mean_len, phread]
    locals()[Sample] = pd.Series(stat_info, index=indexs,name=Sample)
    df = pd.DataFrame({'Reads of length(nt)':counts.keys(), \
                       'Reads of number':counts.values(), \
                       'Reads of Frequence Precent(%)':[x for x in map(lambda x: round(x/Reads_Num*100, 2), counts.values())]})
    df = df.sort_values(by='Reads of length(nt)')
    df.to_csv(f'{Sample}.Reads_Length_Distribution.tsv', sep='\t',index=False)
    return locals()[Sample]

def main(fastq_list: list):
    """
    主程序多线程运行
    """
    isfofn = is_fofn()
    if isfofn == True:
        fqs = []
        with open(fastq_list[0]) as f:
            for l in f:
                fqs.append(l.strip())
            fastq_list = fqs
    with pool(max_workers=4) as t:
        res = t.map(stat_fastq, fastq_list)
        tmp = []
        for i in res:
            tmp.append(i)
    stat = pd.DataFrame(tmp)
    stat.T.to_csv(f'Reads_stat_.tsv', sep='\t')
    print(stat.T)

main(sys.argv[1:])
