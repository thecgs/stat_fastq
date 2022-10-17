#! /bin/env bash

CWD=$(dirname $(realpath $0))
chmod +x ${CWD}/stat_fastq; chmod +x ${CWD}/stat_fastq.py
echo "export PATH=\$PATH:$CWD" >> ~/.bashrc
source ~/.bashrc
pip install pandas -i https://www.douban.com/simple
pip install plotnine -i https://www.douban.com/simple
echo -e '\033[32mInstall finished!\033[0m'
