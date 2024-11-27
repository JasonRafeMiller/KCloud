'''
Input two files like SxM_BR1.mat.gene_counts.tsv
Input two files like SxM_BR1.pat.gene_counts.tsv
Expect tsv files with no header, and lines like...

jg10000.t1	422
jg10002.t1	64

In cross SxM, mat is SS and pat is MM.
The first file should represent SS.
The second file should represent MM.

Output files like SxM_BR4.tsv
Generate tsv files with lines like...

gene  allele      count
jg10000.t1    SS    20
jg10002.t1    MM    10
'''
import sys

def load_counts(fn):
    gene_counts = dict()
    with open (fn, 'r') as fin:
        header = "NO HEADER" # None
        for line in fin:
            if header is None:
                header = line
                continue
            line = line.strip()
            (gene,count) = line.split('\t')
            if gene in gene_counts.keys():
                raise Exception('Gene seen twice:',gene)
            gene_counts[gene]=count
    return gene_counts
    
SS_file = sys.argv[1]
MM_file = sys.argv[2]
out_file = sys.argv[3]
print('Reading SS from',SS_file)
SS_dict = load_counts(SS_file)
print('Reading MM from',MM_file)
MM_dict = load_counts(MM_file)

all_genes = set()
for gene in SS_dict.keys():
    all_genes.add(gene)
for gene in MM_dict.keys():
    all_genes.add(gene)
sorted_genes = sorted(list(all_genes))

with open (out_file, 'w') as fout:
    print('gene','allele','count', sep='\t', file=fout)
    for gene in sorted_genes:
        if gene in SS_dict.keys():
            print(gene, 'SS', SS_dict[gene], sep='\t', file=fout)
        if gene in MM_dict.keys():
            print(gene, 'MM', MM_dict[gene], sep='\t', file=fout)
print('Wrote to',out_file)

