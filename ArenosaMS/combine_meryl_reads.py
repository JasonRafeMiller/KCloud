'''
We used meryl-locate -existence twice.
It ran separately on R1 and R2 reads.
It matched each read against two meryl databases.
It wrote two separate reports.
Here combine those reports and list passing reads.
Enforce KCloud rule: 
both reads must share k-mers with the first db (e.g. MminusS)
and neither read may share any k-mers with the second db (e.g. SminusM).
'''
import sys
MINLEN=50  # min mers per read in pair

def walk_reads(fn):
    '''Assume tab-delimited text file with four columns as generated by meryl:
    read-name mers-in-read db1 common1 db2 common2.'''
    with open (fn, 'r') as fin:
        for line in fin:
            line = line.strip()
            fields = line.split('\t')
            yield fields

def main(infile1,infile2,outfile1,outfile2):
    R1_generator = walk_reads(infile1)
    R2_generator = walk_reads(infile2)
    total_pairs = 0
    too_short = 0
    not_allelic = 0
    try:
        OF1 = open(outfile1,'w') 
        OF2 = open(outfile2,'w') 
        R1_report = next(R1_generator)
        R2_report = next(R2_generator)
        while (R1_report is not None):
            total_pairs += 1
            (R1_name,R1_mers,db1,R1_db1,db2,R1_db2) = R1_report
            (R2_name,R2_mers,db1,R2_db1,db2,R2_db2) = R2_report
            # print("processing",R1_name,R2_name)
            if (R1_name != R2_name):
                print("Unexpected: R1 not equal R1", R1_name, R2_name)
                exit(1)
            R1_len = int(R1_mers)
            R2_len = int(R2_mers)
            if (R1_len<MINLEN and R2_len<MINLEN):
                too_short += 1
                # print("Too short:", R1_mers, R2_mers)
            else:
                db1_count = int(R1_db1)+int(R2_db1)
                db2_count = int(R2_db2)+int(R2_db2)
                if (db1_count>0 and db2_count==0):
                    print(R1_name, file=OF1)
                    # print("Allelic 1:",R1_name,R1_db1,R1_db2,R2_db1,R2_db2)
                elif (db1_count==0 and db2_count>0):
                    print(R1_name, file=OF2)
                    # print("Allelic 2:",R1_name,R1_db1,R1_db2,R2_db1,R2_db2)
                else:
                    not_allelic += 1
                    # print("Not Allele:",R1_name,R1_db1,R1_db2,R2_db1,R2_db2)
            R1_report = next(R1_generator)
            R2_report = next(R2_generator)
        close(OF1)
        close(OF2)
    except StopIteration:
        print("EOF")
    except:
        print("FAIL due to file problem!")
    print("Input pairs:", total_pairs)
    print("Total too short:", too_short)
    print("Total not allelic:", not_allelic)

infile1 = sys.argv[1]
infile2 = sys.argv[2]
outfile1 = sys.argv[3]
outfile2 = sys.argv[4]
# example: python combine.py MxS_BR1_R1.tab MxS_BR1_R2.tab MxS_BR1_MminusS.txt MxS_BR1_SminusM.txt
main(infile1,infile2,outfile1,outfile2)


