# stat_fastq
这是一个统计fastq文件各类指标的工具。 

该项目的早期版本完全由python编写，起初，历遍fastq的代码如下：
```
import sys
import gzip
from itertools import islice
file =  sys.argv[1]

def read_fastq(fastq:str):
    n = 0
    f = gzip.open(fastq, 'rb')
    while True:
        try:
            name = next(islice(f,n,n+4,1)).strip().decode()
            seq = next(islice(f,n,n+4,1)).strip().decode()
            comment = next(islice(f,n,n+4,1)).strip().decode()
            qual = next(islice(f,n,n+4,1)).strip().decode()
            n += 4
            yield (name, seq, comment, qual,n)
        except StopIteration:
            break
    f.close()

for l in read_fastq(file):
    print(l)
```
后来改用了第三放库`pyfastx`，快了很多，代码如下：
```
import pyfastx
with pyfastx.Fastq(fastq, build_index=False) as f:
    for read in fq:
        name, seq, quals = read
```
后来是搜到了一个C++版本（ https://github.com/haiwufan/fastq_stat ），根据这个版本修改了源码（增加了一些指标），速度大幅提升。此外根据python封装了这个工具。


这个工具命名为stat_fastq, 他可以定制输出的格式和指标。使用方法如下：
```
Usage:
    example 1:
    /nfs1/public2/User/chenguisen/01.biosoftware/stat_fastq/stat_fastq.py <fastq.fofn> [option]
    example 2:
    /nfs1/public2/User/chenguisen/01.biosoftware/stat_fastq/stat_fastq.py <file.fastq.gz> [option]
    example 3:
    /nfs1/public2/User/chenguisen/01.biosoftware/stat_fastq/stat_fastq.py <file.fastq1.gz> [file.fastq2.gz] [file.fastq3.gz] ... [option]

Option:
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
Datetime: 2022/10/12; Author: Guisen Chen; Email: thecgs001@foxmail.com; Cite: https//www.github.com/thesg](https://github.com/thecgs/stat_fastq
```


