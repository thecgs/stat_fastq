all: build;

build: ;
	g++ -Wall -O3 -o fastq_stat fastq_stat.cpp

clean: ;
	rm -f fastq_stat
