# python3
from gooey import *
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
# imput parameters
@Gooey(required_cols=2, program_name='protein physiochemical properties calculator', header_bg_color= '#DCDCDC', terminal_font_color= '#DCDCDC', terminal_panel_color= '#DCDCDC')
def main():
	ap = GooeyParser(description="outputs the id, pI, charge and molecular weight of each protein")
	ap.add_argument("-in", "--input_file", required=True, widget='FileChooser', help="input fasta file")
	ap.add_argument("-pH", "--pH", type=float, default=7.0, required=False, help="pH to calculate the protein charge(default is 7.0)")
	ap.add_argument("-out", "--output_file", required=True, widget='FileSaver', help="output txt file")
	args = vars(ap.parse_args())
	# main
	headers = []
	pI = [] 
	charge = []
	mw = [] # setup empty lists
	for record in SeqIO.parse(args['input_file'], "fasta"):
		headers.append(record.id)
		prot = ProteinAnalysis(str(record.seq))
		pI.append('%0.2f' % prot.isoelectric_point())
		mw.append('%0.2f' % prot.molecular_weight())
		charge.append('%0.2f' % prot.charge_at_pH(args['pH']))
	# create data frame
	df = pd.DataFrame()
	df['id'] = headers
	df['pI'] = pI
	df['charge'] = charge
	df['mw'] = mw
	# export
	with open(args['output_file'], 'a') as f:
	    f.write(
	        df.to_csv(header = True, index = False, sep = '\t', doublequote= False, line_terminator= '\n')
	    )

if __name__ == '__main__':
	main()
