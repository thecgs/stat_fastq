#include <map>
#include<stdio.h>
#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
#include <algorithm>
#include <vector>
#include <sstream>
using namespace std;
const float VERSION = 0.2;
const int MAX_LENGTH = 1000;

class Stats {
    public:
        // Read and Base stats
        unsigned long int read_total;
        unsigned long int base_total;
        unsigned long int base_A, base_T, base_C, base_G, base_N;
        
        // Length stats
        unsigned int len_min;
        unsigned int len_max;
        double len_mean;
        map<unsigned int, unsigned long int> len_counts;
        
        // Qual stats
        int phred;
        unsigned int min_phred; 
        unsigned int max_phred;
        unsigned int min_qual;
        unsigned int max_qual;
        vector<unsigned long> qual_vector;
        unsigned long q10, q20, q30, q40, q50;
        
        // initialize
        void init(void) {
            read_total = 0;
            base_total = 0;
            base_A = base_T = 0;
            base_G = base_C = 0;
            base_N = 0;
            len_min = 1000 ;
            len_max = 0;
            len_mean = 0;
            min_qual = 1000;
            max_qual = 0;
            min_phred = 1000;
            max_phred = 0;
            q10 = q20 = q30 = q40 = q50 = 0;
            qual_vector.resize(127,0);
            phred = 33;
        }
        
        void guess_phred() {
            if (max_phred > 74 && min_phred > 58) {
                phred = 64;
            } else if (max_phred <= 74 && min_phred >= 33) {
                phred = 33;
            } else {
                phred = 33;
            }
        }
        
        void getBaseType(string seq) {
            for(int i=0;i<seq.size();i++){
                if(seq[i] == 'A'){
                    base_A+=1;
                }else if(seq[i] == 'T'){
                    base_T+=1;
                }else if(seq[i] == 'C'){
                    base_C+=1;
                }else if(seq[i] == 'G'){
                    base_G+=1;
                }else if(seq[i] == 'N'){
                    base_N+=1;
                }
            }
        }
        
        void len_stat(string seq) {
            if (1 == len_counts.count(seq.length())){
                len_counts[seq.length()]+=1;
                }
            else{
                len_counts[seq.length()] = 1;
            }
        }
        void show_len_distribution() {
            cout << "\nReads_of_Length(nt)\tReads_of_Number\tReads_of_Frequence_Precent(%)\n";
            for (map<unsigned int, unsigned long int>::iterator it = len_counts.begin(); it != len_counts.end(); it++) {
                //cout << it -> first << it -> second << it -> second/read_total
                //printf(it->second, read_total);
                printf("%d\t%d\t%.4f\n", it->first, it->second, (double)((*it).second*100)/read_total);
                }
        }
        
        void transform_quality(string qual) {
            for (int i = 0; i < qual.length(); i++) {
                unsigned int qual_val = (unsigned int)qual[i];
                min_phred = min_phred < qual_val ? min_phred : qual_val;
                max_phred = max_phred > qual_val ? max_phred : qual_val;
                min_qual = min_qual < qual_val ? min_qual : qual_val;
                max_qual = max_qual > qual_val ? max_qual : qual_val;
                qual_vector[qual_val] += 1;
            }
        }
        
        void qual_stats(void) {
            int index = 0;
            for(int i=10;i<=51;i+=1){
                index=i+phred;
                q10+=qual_vector[index];
                if(i>=20){
                    q20 += qual_vector[index];
                }
                if(i>=30){
                    q30 += qual_vector[index];
                }
                if(i>=40){
                    q40 += qual_vector[index];
                }
                if (i >= 50) {
                    q50 += qual_vector[index];
                }
            }
        }
        
        void jsonify_stats() {
            string t1 = "\t";
            len_mean = base_total * 1.0 / read_total;
            double q10_percent = q10 * 100.0 / base_total;
            double q20_percent = q20 * 100.0 / base_total;
            double q30_percent = q30 * 100.0 / base_total;
            double q40_percent = q40 * 100.0 / base_total;
            double q50_percent = q50 * 100.0 / base_total;
            double AT_percent = (base_A + base_T) * 100.0 / base_total;
            double GC_percent = (base_C + base_G) * 100.0 / base_total;
            double A_percent = (base_A * 100.0) / base_total;
            double T_percent = (base_T * 100.0) / base_total;
            double G_percent = (base_G * 100.0) / base_total;
            double C_percent = (base_G * 100.0) / base_total;
            double N_percent = (base_N * 100.0) / base_total;
            
            //cout << "Reads\tBases\tQ30%\tQ20%\tGC%\tNppm\tAve_len\tMin_len\tMax_len\n";
            //cout << read_total << t1 << base_total << t1 << q30_percent << t1 << q20_percent << t1 << GC_percent << t1 << Nppm << t1 << len_mean << t1 << len_min << t1 << len_max << "\n";
            
            cout << "\nReads_Num\t" << read_total << "\n";
            cout << "Reads_Base(nt)\t" << base_total << "\n";
            cout << "Q10(%)\t" << q10_percent << "%" << "\n";
            cout << "Q20(%)\t" << q20_percent << "%" << "\n";
            cout << "Q30(%)\t" << q30_percent << "%" << "\n";
            cout << "Q40(%)\t" << q40_percent << "%" << "\n";
            cout << "Q50(%)\t" << q50_percent << "%" << "\n";
            cout << "Min_qual\t" << min_qual - phred << "\n";
            cout << "Max_qual\t" << max_qual - phred << "\n";
            cout << "AT_Bases(%)\t" << base_A + base_T << "(" << AT_percent << "%)" << "\n";
            cout << "GC_Bases(%)\t" << base_G + base_C << "(" << GC_percent << "%)" << "\n";
            cout << "A_Bases(%)\t" << base_A << "(" << A_percent << "%)" << "\n";
            cout << "T_Bases(%)\t" << base_T << "(" << T_percent << "%)" << "\n";
            cout << "G_Bases(%)\t" << base_G << "(" << G_percent << "%)" << "\n";
            cout << "C_Bases(%)\t" << base_C << "(" << C_percent << "%)" << "\n";
            cout << "N_Bases(%)\t" << base_N << "(" << N_percent << "%)" << "\n";
            cout << "Min_len\t" << len_min << "\n";
            cout << "Max_len\t" << len_max << "\n";
            cout << "Mean_len\t" << len_mean << "\n";
            cout << "Phread_Type\t" << phred << "\n";
        }
};
/*

	Author: 	haiwufan; Guisen, Chen
	citation： 	https://github.com/rpetit3/fastq-stats; https://github.com/thecgs/stat_fastq

*/


int main() {
    Stats stats;
    stats.init();
    string name, seq, plus, qual;
    ifstream in("/dev/stdin", ios::in);
    while(true) {
        if(!getline(in,name,'\n')) break;
        if(!getline(in,seq,'\n')) break;
        if(!getline(in,plus,'\n')) break;
        if(!getline(in,qual,'\n')) break;
        int len = seq.length();
        
        if(seq.length()!=qual.length())    {
                cout << "Error: " << name << " base length not equal qual length!!!\n";
        exit(1) ;
        }
        stats.read_total++;
        stats.base_total+=len;
        
        stats.len_min = stats.len_min<len ? stats.len_min : len;
        stats.len_max = stats.len_max<len ? len : stats.len_max;
        
        stats.getBaseType(seq);
        stats.transform_quality(qual);
        stats.len_stat(seq);
    }
    in.close();
//    Determine Stats
    stats.guess_phred();
    stats.qual_stats();
    stats.jsonify_stats();
    stats.show_len_distribution();
    return 0;
}