# python3
from gooey import *
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
# imput parameters
@Gooey(required_cols=2, program_name='protein physicochemical properties calculator', header_bg_color= '#DCDCDC', terminal_font_color= '#DCDCDC', terminal_panel_color= '#DCDCDC')
def main():
    ap = GooeyParser(description="outputs the id, pI, charge and molecular weight of each protein")
    ap.add_argument("-in", "--input", required=True, widget='FileChooser', help="input fasta file")
    ap.add_argument("-txt", "--txt", required=False,  widget='FileChooser', help=" 1-column txt file with pH values, to calculate the protein charge")
    ap.add_argument("-pH", "--pH", type=float, default=7.0, required=False, help="pH to calculate the protein charge(default is 7.0)")
    ap.add_argument("-pro", "--program", type=int, default=1, required=False, help="program to select 1) 1 pH value , 2) many pH values 1 per protein, 3) many pH values for all proteins. Default is 1")
    ap.add_argument("-out", "--output", required=True, widget='FileSaver', help="output txt file with id, pI, charge, molecular weight and pH columns")
    args = vars(ap.parse_args())
    # main
    headers = []
    seqs = []
    pI = [] 
    charge = []
    mw = [] # setup empty lists
    # choose program
    # same pH value for all proteins
    if args['program'] == 1:
        for record in SeqIO.parse(args['input'], "fasta"):
            headers.append(record.id)
            prot = ProteinAnalysis(str(record.seq))
            pI.append(round(prot.isoelectric_point(), 2))
            mw.append(round(prot.molecular_weight(), 2))
            charge.append(round(prot.charge_at_pH(args['pH']), 2))
        # create data frame
        df = pd.DataFrame()
        df['id'] = headers
        df['pI'] = pI
        df['charge'] = charge
        df['mw'] = mw
        df['pH'] = args['pH']
        # export
        with open(args['output'], 'a') as f:
            f.write(
                df.to_csv(header = True, index = False, sep = '\t', doublequote= False, line_terminator= '\n')
            )
    # 1 pH value for each protein
    elif args['program'] == 2:
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
        df['pH'] = ph_values
        # export
        with open(args['output'], 'a') as f:
            f.write(
                df.to_csv(header = True, index = False, sep = '\t', doublequote= False, line_terminator= '\n')
            )
    # many pH values for each protein
    else:
        # setup empty list
        physioprot = []
        # import txt file with pH values
        with open(args['txt'], 'r') as f:
            ph_values = f.readlines()
        ph_values = [x.strip() for x in ph_values]
        # iterate for each pH value in each fasta record
        for i in ph_values:
            for record in SeqIO.parse(args['input'], "fasta"):
                headers.append(record.id)
                prot = ProteinAnalysis(str(record.seq))
                pI.append(round(prot.isoelectric_point(), 2))
                mw.append(round(prot.molecular_weight(), 2))
                charge.append(round(prot.charge_at_pH(float(i)), 2))
            # create data frame
            df = pd.DataFrame()
            df['id'] = headers
            df['pI'] = pI
            df['charge'] = charge
            df['mw'] = mw
            df['pH'] = float(i)
            # append to list to merge with other dataframes that have different pH values
            physioprot.append(df)
            # remove dataframes and list to be reused again
            headers.clear(); pI.clear(); charge.clear(); mw.clear(); del df
        # combine dataframes to 1
        df_merged = pd.concat(physioprot)
        # export
        with open(args['output'], 'a') as f:
            f.write(
                df_merged.to_csv(header = True, index = False, sep = '\t', doublequote= False, line_terminator= '\n')
            )

if __name__ == '__main__':
    main()
