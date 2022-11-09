# stat_fastq
这是一个统计fastq文件各类指标的工具。 
这个工具命名为stat_fastq, 他可以定制输出的格式和指定输出指标。可以支持输入多个fastq文件，并且支持多线程执行.

软件的安装：
```
git clone https://github.com/thecgs/stat_fastq.git
bash ./stat_fastq/INSTALL.sh
```
`stat_fastq`文件是一个编译好的二进制文件，如果你需要重新编译，可以这样编译`g++ stat_fastq.cpp -o stat_fastq`，注意，编译完成的二进制文件需要和主程序`stat_fastq.py`在同一文件夹下

使用方法如下：
```
$ python stat_fastq.py -h

Usage:
    example 1:
    /nfs1/public2/User/chenguisen/01.biosoftware/stat_fastq/stat_fastq.py <fastq.fofn> [option]
    example 2:
    /nfs1/public2/User/chenguisen/01.biosoftware/stat_fastq/stat_fastq.py <file.fq.gz> [option]
    example 3:
    /nfs1/public2/User/chenguisen/01.biosoftware/stat_fastq/stat_fastq.py <file1.fq.gz> [file2.fq.gz] [file3.fq.gz] ... [option]

Option:
    -o   --output         Save output file of tsv format [default: Close]
    -t   --Transposition  Transposition Stdout format [default: Vertical]
    -d   --Distribution   Open output "Reads length distribution" file [default: Close]
    -g   --ggplot         Drawing Reads length distribution plot [default: Close]
    -n   --Reads_Num      Close ouput Reads of Number [default: Open]
    -b   --Reads_Base     Close ouput Reads of Bese Number [default: Open]
    -10  --Q10            Close ouput Q10 [default: Open]
    -20  --Q20            Close ouput Q20 [default: Open]
    -30  --Q30            Close ouput Q30 [default: Open]
    -40  --Q40            Close ouput Q40 [default: Open]
    -50  --Q50            Close ouput Q50 [default: Open]
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
```

例子一：
```
$ cat fastq.fofn
/data/2022/10-12/WT_1.fq.gz
/data/2022/10-12/M3_1.fq.gz
/data/2022/10-12/M3_2.fq.gz
/data/2022/10-12/WT_2.fq.gz

$ python stat_fastq.py fastq.fofn
                                WT_1                  M3_1                  M3_2                  WT_2
Reads_Num                   82561175              77216259              96803945             106000544
Reads_Base(nt)           12384176250           11582438850           14520591750           15900081600
Q10(%)                       99.997%              99.9993%              99.9993%              99.9995%
Q20(%)                      83.4571%              76.3126%              75.9509%              77.9955%
Q30(%)                      72.6262%              64.9859%              64.3737%              65.6465%
Q40(%)                      36.4314%              52.8567%              52.1012%              52.9124%
Min_qual                           2                     2                     2                     2
Max_qual                          41                    41                    41                    41
AT_Bases(%)     5105473290(41.2258%)  5676494935(49.0095%)  6982315472(48.0856%)  7493666735(47.1297%)
GC_Bases(%)     7278331828(58.7712%)  5905861065(50.9898%)  7538172361(51.9137%)  8406330226(52.8697%)
A_Bases(%)      2945803511(23.7868%)  3237282594(27.9499%)  4052007243(27.9052%)    4561738335(28.69%)
T_Bases(%)      2159669779(17.4389%)  2439212341(21.0596%)  2930308229(20.1804%)  2931928400(18.4397%)
G_Bases(%)      4815207048(38.8819%)  3452302746(29.8064%)  4462377776(30.7314%)  4906221582(30.8566%)
C_Bases(%)      2463124780(38.8819%)  2453558319(29.8064%)  3075794585(30.7314%)  3500108644(30.8566%)
N_Bases(%)       371132(0.00299682%)   82850(0.000715307%)  103917(0.000715653%)   84639(0.000532318%)
Min_len                          150                   150                   150                   150
Max_len                          150                   150                   150                   150
Mean_len                         150                   150                   150                   150
Phread_Type                       33                    33                    33                    33
```

例子二：
```
$ python stat_fastq.py fastq.fofn -t -A -T -G -C -10 -40
      Reads_Num Reads_Base(nt)    Q20(%)    Q30(%) Min_qual Max_qual           AT_Bases(%)           GC_Bases(%)            N_Bases(%) Min_len Max_len Mean_len Phread_Type
WT_1   82561175    12384176250  83.4571%  72.6262%        2       41  5105473290(41.2258%)  7278331828(58.7712%)   371132(0.00299682%)     150     150      150          33
M3_1   77216259    11582438850  76.3126%  64.9859%        2       41  5676494935(49.0095%)  5905861065(50.9898%)   82850(0.000715307%)     150     150      150          33
M3_2   96803945    14520591750  75.9509%  64.3737%        2       41  6982315472(48.0856%)  7538172361(51.9137%)  103917(0.000715653%)     150     150      150          33
WT_2  106000544    15900081600  77.9955%  65.6465%        2       41  7493666735(47.1297%)  8406330226(52.8697%)   84639(0.000532318%)     150     150      150          33
```

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
            yield (name, seq, puls, qual)
        except StopIteration:
            break
    f.close()

for l in read_fastq(file):
    print(l)
```
之后改用了第三方库`pyfastx`，快了很多，代码如下：
```
import pyfastx
with pyfastx.Fastq(fastq, build_index=False) as f:
    for read in fq:
        name, seq, quals = read
```
再后来搜到了一个C++版本（ https://github.com/haiwufan/fastq_stat ），根据这个版本修改了源码（增加了一些指标），速度大幅提升。并且根据python封装了这个工具
