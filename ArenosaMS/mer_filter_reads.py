import sys
import gzip
from datetime import datetime
import time
import psutil
import pickle

# Reject a read pair if it has one negative k-mer.
# Require at least one positive k-mer.
# Skip by 8s.
# Test mat and pat together.

# Assume paired-end RNA-seq and canonical mer counts.
# Read pairs reflect both strands of the cDNA copy of the mRNA.
KSIZE=16  # length of k-mers in our meryl dtabases
KSTEP=8   # not necessary to check every consecutive k-mer

class FastqReader():
    '''Return a line iterator on a gzip text file.'''
    def __init__(self,filename):
        self.fn = filename
        try:
            self.fin = gzip.open(self.fn,'rb')
        except:
            print("Cannot open", filename)
            sys.exit(1)
    def close(self):
        self.fin.close()
    def __iter__(self):
        return self.fin

def get_read_pair(iter1,iter2):
    '''Read 4 lines from each text file iterator. Load ID and SEQ.'''
    try:
        r1=list()
        id = next(iter1).rstrip()
        id = id.split(b' ')[0] # chop bar code
        r1.append(id[1:]) # chop @ symbol
        r1.append(next(iter1).rstrip()) # nucleotides (bytes)
        next(iter1) # unused
        next(iter1) # quality values
        r2 = list()
        id = next(iter2).rstrip()
        id = id.split(b' ')[0]
        r2.append(id[1:])
        r2.append(next(iter2).rstrip())
        next(iter2)
        next(iter2)
        rp = (r1,r2)
        return rp
    except StopIteration as e:
        return None

A = bytes('A',encoding='utf-8')
C = bytes('C',encoding='utf-8')
G = bytes('G',encoding='utf-8')
T = bytes('T',encoding='utf-8')
N = bytes('N',encoding='utf-8')
keys=[A,C,G,T,N]
values=[T,G,C,A,N]
complement = dict(zip(keys,values)) # TO DO: faster to use array?
def reverse_complement(dna):
    L = len(dna)  # TO DO: hard-code to Ksize?
    rc = bytearray(L)
    pos = L-1
    for i in range(L):
        nuc=dna[i:i+1] # dna[i] returns an int but this returns a byte
        cmp = complement[nuc]
        rc[pos]=int.from_bytes(cmp,"big") # byte order required, even for one byte
        pos = pos-1
    rcb = bytes(rc) # compatible with our mers.keys
    return rcb

def load_kmers(datafile,cachename):
    try:
        with open(cachename, 'rb') as handle:
            print('Loading kmers from cache',cachename)
            kd = pickle.load(handle)
    except:
        kd = dict()
        with open (datafile, 'r') as fin:
            print('Loading kmers from file',datafile)
            for line in fin:
                fields = line.rstrip().split('\t')
                mer = bytes(fields[0],'utf-8')
                cnt = int(fields[1])
                kd[mer]=cnt
        print('Saving kmers to cache',cachename)
        with open(cachename, 'wb') as handle:
            pickle.dump(kd, handle)
    return kd

def test_read_pair(rp,mat_mers,pat_mers):
    has_mat = False
    has_pat = False
    for i in range(2):
        r = rp[i][1]  # TO DO: class with read_pair.get_nucleotides(i) method
        for s in range(0,len(r)-KSIZE+1,KSTEP):
            substring = r[s:s+KSIZE]
            # TO DO: optimize. k is constant. use canonical mer.
            if not has_mat:
                has_mat = substring in mat_mers.keys() or reverse_complement(substring) in mat_mers.keys()
            if not has_pat:
                has_pat = substring in pat_mers.keys() or reverse_complement(substring) in pat_mers.keys()
            if has_mat and has_pat:
                return 'both'   # should not happen
    if has_mat and not has_pat:
        return 'mat'
    if has_pat and not has_mat:
        return 'pat'
    return None   # all k-mers are common, read pair is uninformative
    
if __name__ == '__main__':
    if True:
        print('Test reverse complement')
        fwd=bytes('AATTTCCGGG',encoding='utf-8')
        rev=reverse_complement(fwd)
        print(fwd)
        print(rev)

    if len(sys.argv)!=6:
        print('Required Parameters: RUN_NAME MAT_KMERS PAT_KMERS FASTQ1 FASTQ2')
        sys.exit(1)
        
    print('Get process handle...')
    process = psutil.Process()

    # Assume: meryl print meryl_intersect.db > distinct_mers.txt
    # Example inputs
    RUN_NAME = 'SxM'
    MAT_KMERS = 'IntersectSxM_SminusM/distinct_mers.txt'
    PAT_KMERS = 'IntersectSxM_MminusS/distinct_mers.txt'
    FASTQ1 = 'test/SxM_BR1_R1_10Ksubset.fq.gz'
    FASTQ2 = 'test/SxM_BR1_R2_10Ksubset.fq.gz'

    print('Parse argv...')
    RUN_NAME = sys.argv[1]
    MAT_KMERS = sys.argv[2]
    PAT_KMERS = sys.argv[3]
    FASTQ1 = sys.argv[4]
    FASTQ2 = sys.argv[5]
    MAT_FILE = RUN_NAME+ '.mat.IDs.txt'
    PAT_FILE = RUN_NAME+ '.pat.IDs.txt'
    MAT_CACHE = RUN_NAME+'.mat.kmer.cache.pkl'
    PAT_CACHE = RUN_NAME+'.pat.kmer.cache.pkl'
    
    print('Mat Kmers :', MAT_KMERS)
    print('Pat Kmers :', PAT_KMERS)
    print('Fastq 1 :', FASTQ1)
    print('Fastq 2 :', FASTQ2)
    print('Output :', MAT_FILE,PAT_FILE)

    print('Load Mat Kmers',flush=True)
    print(datetime.now(),'now')
    start = time.time()
    mat_mers = load_kmers(MAT_KMERS,MAT_CACHE)
    end = time.time()
    print(end - start, 'elapsed')
    print('Count =',len(mat_mers))
    print(datetime.now(),'now')
    footprint=process.memory_info().rss
    print(f'RAM {footprint:,} bytes')

    print('Load Pat Kmers',flush=True)
    print(datetime.now(),'now')
    start = time.time()
    pat_mers = load_kmers(PAT_KMERS,PAT_CACHE)
    end = time.time()
    print(end - start, 'elapsed')
    print('Count =',len(pat_mers))
    print(datetime.now(),'now')
    footprint=process.memory_info().rss
    print(f'RAM {footprint:,} bytes')
    
    reads1 = FastqReader(FASTQ1)
    reads2 = FastqReader(FASTQ2)
    iter1 = iter(reads1)
    iter2 = iter(reads2)
    print('Processing reads...',flush=True)
    print(datetime.now(),'now')
    start = time.time()
    total = 0
    maternal = 0
    paternal = 0
    both = 0
    uninformative = 0
    with open(MAT_FILE, 'w') as mat_out, open(PAT_FILE, 'w') as pat_out:
        rp=get_read_pair(iter1,iter2)
        print('first read pair',rp)
        while rp != None:
            total += 1
            choice = test_read_pair(rp,mat_mers,pat_mers)
            # TO DO: use read_pair.get_id() or use index into file
            if choice == 'mat':
                mat_out.write(rp[0][0].decode())
                mat_out.write('\n')
                maternal += 1
            elif choice == 'pat':
                pat_out.write(rp[0][0].decode())
                pat_out.write('\n')
                paternal += 1
            elif choice == 'both':
                both += 1
            else:
                uninformative += 1
            rp=get_read_pair(iter1,iter2)
    end = time.time()
    reads1.close()
    reads2.close()
    print(end - start, 'elapsed')
    print('Total =',total)
    print('Maternal =',maternal)
    print('Paternal =',paternal)
    print('Both =',both)
    print('Uninformative =',uninformative)
    if total>0:
        print('Time per read =',(end - start)/total)
    print(datetime.now(),'now')
    print('Done')
    
