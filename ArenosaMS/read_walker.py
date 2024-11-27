'''
We used KCloud, our k-mer analysis pipeline, to identify mat or pat reads.
Those are a subset of all reads.
We used bowtie to map all reads to transcripts.
For most reads, those have a transcript ID.
Assume both files were sorted with unix sort.
That allows us to walk both in tandem, like unix comm.
Now, count subset reads per transcript.
'''
import sys

def walk_reads(fn):
    '''Assume text file with Illumina read ID per line.
    This is a read subset generated by KCloud.'''
    with open (fn, 'r') as fin:
        for line in fin:
            line = line.strip()
            yield line

def walk_maps(fn):
    '''Assume text file format: readID \t geneID.
    This is from bowtie via samtools.'''
    with open (fn, 'r') as fin:
        for line in fin:
            line = line.strip()
            (read,gene) = line.split('\t')
            yield (read,gene)
    
gene_counts=dict()
def increment_gene_count(gene):
    if gene not in gene_counts.keys():
        gene_counts[gene]=0
    gene_counts[gene] += 1


def main(reads_file,maps_file):
    read_generator = walk_reads(reads_file)
    map_generator = walk_maps(maps_file)
    mapped_read,mapped_gene = next(map_generator)
    readID = next(read_generator)
    read_cnt = 1
    map_cnt = 1
    try:
        while True:
            if readID is None or mapped_read is None:
                break
            while readID is not None and readID < mapped_read:
                readID = next(read_generator)
                read_cnt += 1
            while mapped_read is not None and mapped_read < readID:
                mapped_read,mapped_gene = next(map_generator)
                map_cnt += 1
            if readID == mapped_read:
                increment_gene_count(mapped_gene)
            if readID is not None:
                readID = next(read_generator)
                read_cnt += 1
    except StopIteration:
        print('End of file')
    return gene_counts

reads_file = sys.argv[1]
maps_file = sys.argv[2]
out_file = sys.argv[3]
print('Reading read ID subset from',reads_file)
print('Reading gene maps from',maps_file)
gc = main(reads_file,maps_file)
print(len(gc.keys()), 'genes')
print(sum(gc.values()), 'mapped reads')
with open (out_file, 'w') as fout:
    genes = gc.keys()
    genes = sorted(list(genes))
    for gene in genes:
        print(gene, gc[gene], sep='\t', file=fout)
print('Wrote to',out_file)
