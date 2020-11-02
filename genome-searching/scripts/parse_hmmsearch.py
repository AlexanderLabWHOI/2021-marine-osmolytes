from Bio import SearchIO
import pandas as pd
import glob
import os


def retrieve_max_hmm_scores(hmmfile):
    with open(hmmfile, 'r') as handle:
        max_hit = 0
        max_dom = 0
        for record in SearchIO.parse(handle, 'hmmer3-tab'):
            for hit in (record.hits):
                if hit.bitscore> max_hit:
                    max_hit = hit.bitscore 
            for dom in (record.hsps):
                if dom.bitscore > max_dom:
                    max_dom = dom.bitscore
    
    return(max_hit, max_dom)

df = pd.DataFrame(columns=['full_bitscore', 'domain_bitscore'])

hmm_dir = os.path.dirname(snakemake.input[0])
for hmmfile in glob.glob(os.path.join(hmm_dir,'K*')):
    index_name = os.path.basename(hmmfile)
    full_bitscore, domain_bitscore = retrieve_max_hmm_scores(hmmfile)
    df.loc[index_name] = (full_bitscore, domain_bitscore)

df.to_csv(snakemake.output[0], sep='\t')

