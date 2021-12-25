# python3
import argparse
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
# imput parameters
ap = argparse.ArgumentParser(description="outputs the id, pI, charge and molecular weight of each protein")
ap.add_argument("-in", "--input", required=True, help="input fasta file")
ap.add_argument("-txt", "--txt", required=False, help=" 1-column txt file with pH values 1 for each protein, to calculate the protein charge")
ap.add_argument("-pH", "--pH", type=float, default=7.0, required=False,help="pH to calculate the protein charge(default is 7.0)")
ap.add_argument("-pro", "--program", type=int, default=1, required=False, help="program to select 1) 1 pH value , 2) many pH values. Default is 1")
ap.add_argument("-out", "--output", required=True, help="output txt file")
args = vars(ap.parse_args())
# main
headers = []
seqs = []
pI = [] 
charge = []
mw = [] # setup empty lists
# choose program
if args['program'] == 1:
    for record in SeqIO.parse(args['input'], "fasta"):
        headers.append(record.id)
        prot = ProteinAnalysis(str(record.seq))
        pI.append(round(prot.isoelectric_point(), 2))
        mw.append(round(prot.molecular_weight(), 2))
        charge.append(round(prot.charge_at_pH(args['pH']), 2))
else:
    for record in SeqIO.parse(args['input'], "fasta"):
        headers.append(record.id)
        seqs.append(record.seq)
    # import txt file with pH values
    with open(args['txt'], 'r') as f:
        ph_values = f.readlines()
    ph_values = [x.strip() for x in ph_values] 
    # calculate the properties using a pair of the above 2 lists
    for (a, b) in zip(seqs, ph_values):
        prot = ProteinAnalysis(str(a))
        pI.append(round(prot.isoelectric_point(), 2))
        mw.append(round(prot.molecular_weight(), 2))
        charge.append(round(prot.charge_at_pH(float(b)), 2))
# create data frame
df = pd.DataFrame()
df['id'] = headers
df['pI'] = pI
df['charge'] = charge
df['mw'] = mw
# choose program
if args['program'] == 1: 
    df['pH'] = args['pH']
else:
    df['pH'] = ph_values
# export
with open(args['output'], 'a') as f:
    f.write(
        df.to_csv(header = True, index = False, sep = '\t', doublequote= False, line_terminator= '\n')
    )
