import pandas as pd
import glob
import os

kofamlist = pd.read_csv(os.path.join(snakemake.config['kofamscan_db'], 'ko_list'), sep='\t', index_col=0) #read in kolist file
KO_index = pd.read_csv(snakemake.input['ko_list'], sep='\t', index_col=0).index

out_df = pd.DataFrame(columns=KO_index)

for csv_file in snakemake.input['genomes']:
    df = pd.read_csv(csv_file, sep='\t', index_col=0)
    name = os.path.basename(csv_file).strip('.csv')

    for k in KO_index:
        column=None
        if kofamlist.loc[k, 'score_type']=='full':
            column = 'full_bitscore'
        elif kofamlist.loc[k, 'score_type']=='domain':
            column = 'domain_bitscore'
        if df.loc[k,column] > float(kofamlist.loc[k,'threshold']):
            out_df.loc[name, k]=1
        else:
            out_df.loc[name,k]=0
out_df.to_csv(snakemake.output[0])
