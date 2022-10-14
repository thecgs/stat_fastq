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
后来是搜到了一个C++版本（https://github.com/haiwufan/fastq_stat），根据这个版本修改了源码（增加了一些指标），速度大幅提升。此外根据python封装了这个工具。


定制统计fastq输出格式的
