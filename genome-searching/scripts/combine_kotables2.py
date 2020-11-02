#!/usr/bin/env python
import pandas as pd
import glob
import os
import sys

kofamlist = pd.read_csv(sys.argv[1], sep='\t', index_col=0) #read in kolist file
KO_index = pd.read_csv(sys.argv[2], sep='\t', index_col=0).index

out_df = pd.DataFrame(columns=KO_index)
header = sys.argv[4]
for csv_file in glob.glob(os.path.join(sys.argv[3],header+'*csv')):
    print(csv_file) 
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
out_df.to_csv(sys.argv[5])
