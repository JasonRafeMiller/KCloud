import sys
import gzip
from datetime import datetime
import time

# Input 1: Genes file.
# Contains read IDs assigned to genes by Bowtie.
# Generated by extract_gene_per_read.sh
# Columns 1 and 3 from a 'samtools view' of bam file.
# Stream this file, assumed longer than any parent file.
# Example filename and first line: SxM_BR1_genes.csv
# A00943:178:H52HWDRXY:1:2101:1615:1000,jg9197.t1

# Input 2-? : Parent file(s).
# Files like BR1.mat, BR1.pat, BR2.mat, BR2.pat, ...
# Each file has read IDs assigned to parent by KCloud.
# Load these into RAM, assumed shorter than genes file.
# Example filename and first line: MxS.mat.IDs.txt
# A00943:310:HG7VTDRXY:1:2104:31485:35603

# Output file: min_and_fold.tsv, used by IRP
# Contains three numbers per gene.
# Header and example line:
# MinOneRep	MinOneSamp Fold
# jg8489.t1 1350 8351 394.520833

def load_reads(reads_fn):
    '''Return a presence/absence dict.'''
    reads = dict()
    with gzip.open(reads_fn,'rb') as fin:
        for line in fin:
            line = line.strip()
            parent_read = line  # bytes
            reads[parent_read]=True
    return reads

def write_folds():
    global GUIDE,COUNTS
    MAXINT = 1000000   # for min function
    crosses = GUIDE.get_cross_names()
    replicates = GUIDE.get_replicate_names()
    genes = COUNTS.get_gene_names()
    print('gene\tMinOneRep\tMinSumReps\tFold')
    for gene in genes:
        minOneRep = MAXINT
        minSumReps = MAXINT
        correctMaps = 0
        incorrectMaps = 0
        for cross in crosses:
            pref = GUIDE.get_preference(cross)
            sumReps = 0
            for rep in replicates:
                mcount = COUNTS.get_count(gene,cross,rep,'mat')
                pcount = COUNTS.get_count(gene,cross,rep,'pat')
                oneRep = mcount + pcount
                sumReps = sumReps + oneRep
                minOneRep = min(minOneRep,oneRep)
                if pref=='mat':
                    correctMaps += mcount
                    incorrectMaps += pcount
                else:
                    correctMaps += pcount
                    incorrectMaps += mcount
        minSumReps = min(minSumReps,minOneRep)
        if incorrectMaps==0:
            fold = MAXINT
        else:
            fold = (correctMaps-incorrectMaps)/incorrectMaps
        print(gene,minOneRep,minSumReps,fold,sep='\t')

class count_struct():
    def __init__(self,crosses,replicates):
        self.genes = dict()
        self.crosses = crosses
        self.replicates = replicates
    def get_gene_names(self):
        genes = [str(x) for x in self.genes.keys()]
        return genes
    def increment(self,gene,cross,rep,allele):
        if gene not in self.genes.keys():
            record = dict()
            for cross in self.crosses:
                for rep in self.replicates:
                    for allele in ('mat','pat'):
                        key=(cross,rep,allele)
                        record[key]=0
            self.genes[gene]=record
        record = self.genes[gene]
        key=(cross,rep,allele)
        record[key] += 1
    def get_count(self,gene,cross,rep,allele):
        record = self.genes[gene]
        key=(cross,rep,allele)
        value = record[key]
        return value

class guide_struct():
    def __init__(self):
        self.samples = dict()
        self.preferences = dict()
    def __str__(self):
        show = "Files Guide"
        for key in self.samples.keys():
            cross,rep = key
            record = self.samples[key]
            show += '\n'+str(key)
            show += ' maps='+record['gene']
            show += ' mat='+record['mat']
            show += ' pat='+record['pat']
            show += ' pref='+self.preferences[cross]
        return show
    def add(self,type,cross,rep,filename):
        key = (cross,rep)
        if key not in self.samples.keys():
            record = dict()
            self.samples[key]=record
        record=self.samples[key]
        record[type]=filename
        # First parent listed is the preferred one.
        # Assume same for all biological replicates.
        if cross not in self.preferences.keys():
            if type=='mat' or type=='pat':
                self.preferences[cross]=type
    def get_samples(self):
        return list(self.samples.keys())
    def get_preference(self,cross):
        return self.preferences[cross]
    def get_filename(self,type,cross,rep):
        # type is one of {gene, mat, pat}
        key = (cross,rep)
        record = self.samples[key]
        filename = record[type]
        return filename
    def get_cross_names(self):
        names = set()
        for key in self.samples.keys():
            (cross,rep)=key
            names.add(cross)
        return names
    def get_replicate_names(self):
        names = set()
        for key in self.samples.keys():
            (cross,rep)=key
            names.add(rep)
        return names

def process_one(cross,replicate):
    '''
    initialize data structure for counts
    for each parent file:
        load the parent read IDs
        stream the gene assignments
        accumulate counts in data structure
    compute and output the totals
    '''
    global GUIDE
    gene_file = GUIDE.get_filename('gene',cross,replicate)
    mat_file = GUIDE.get_filename('mat',cross,replicate)
    pat_file = GUIDE.get_filename('pat',cross,replicate)
    print('Cross',cross,'replicate',replicate)
    mat_dict = load_reads(mat_file)
    print('Mat reads loaded:',len(mat_dict.keys()))
    pat_dict = load_reads(pat_file)
    print('Pat reads loaded:',len(pat_dict.keys()))
    print('Streaming',gene_file,'...')
    # accumulate statistics while streaming genes file
    global COUNTS
    cnt=0
    with gzip.open(gene_file,'rb') as fin:
        for line in fin:
            line = line.strip()
            fields = line.split(b',')
            mapped_read = fields[0]
            gene_id = fields[1]
            gene_id = gene_id.decode("utf-8")
            if mapped_read in mat_dict:
                COUNTS.increment(gene_id,cross,replicate,'mat')
            if mapped_read in pat_dict:
                COUNTS.increment(gene_id,cross,replicate,'pat')
            cnt += 1
    print(cnt,'genes processed.')

def process_all():
    global GUIDE
    crosses = GUIDE.get_cross_names()
    replicates = GUIDE.get_replicate_names()
    for cross in crosses:
        for replicate in replicates:
            process_one(cross,replicate)

def main(guide_fn):
    global GUIDE,COUNTS
    GUIDE = guide_struct()
    with open (guide_fn, 'r') as fin:
        header = None
        for line in fin:
            line = line.strip()
            if line[0]=='#':
                continue # ignore comments
            if header is None:
                header = line
                continue
            type,cross,rep,filename=line.split('\t')
            GUIDE.add(type,cross,rep,filename)
    crosses = GUIDE.get_cross_names()
    replicates = GUIDE.get_replicate_names()
    print('Crosses:',crosses)
    print('Replicates:',replicates)
    print(str(GUIDE))
    COUNTS = count_struct(crosses,replicates)
    process_all()
    write_folds()

if __name__ == '__main__':
    num_params = len(sys.argv)
    if num_params != 2:
        print('Expect one parameter: files_guide.tsv')
        print('Num parameters seen:',num_params)
        print('Parameters seen:', sys.argv)
        sys.exit(1)

    print('Parse argv...')
    SCRIPT_FN = sys.argv[0]
    GUIDE_FN = sys.argv[1]

    main(GUIDE_FN)
