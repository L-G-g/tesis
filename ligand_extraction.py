import os
import argparse
from Bio.PDB import PDBParser, PDBIO, Select
import re

def is_het(residue):
    res = residue.id[0]
    return res != " " and res != "W"


class ResidueSelect(Select):
    def __init__(self, chain, residue):
        self.chain = chain
        self.residue = residue

    def accept_chain(self, chain):
        return chain.id == self.chain.id

    def accept_residue(self, residue):
        """ Recognition of heteroatoms - Remove water molecules """
        return residue == self.residue and is_het(residue)


def extract_ligands(path, pdb):
    """ Extraction of the heteroatoms of .pdb files """
    
    pattern = re.compile(r'\b[A-Z\d]{2,3}\b')
    for pfb_file in os.listdir(path):
        i = 1
        if pfb_file.endswith(str(pdb)) and not pfb_file.startswith("lig_"):
            pdb_code = pfb_file[:-4]
            pdb = PDBParser().get_structure(pdb_code, path + '/' + pfb_file)
            io = PDBIO()
            io.set_structure(pdb)
            for model in pdb:
                for chain in model:
                    for residue in chain:
                        if not is_het(residue):
                            continue
                        res_name = pattern.findall(str(residue))[0]
                        io.save(f"lig_{res_name}_{i}.pdb", ResidueSelect(chain, residue))
                        i += 1

def main():
    parser = argparse.ArgumentParser(description='Extract heteroatoms from PDB files.')
    parser.add_argument('path', type=str, help='Path to the PDB files')
    parser.add_argument('--pdb', type=str, default='<pdb>', help='PDB file pattern to match')
    args = parser.parse_args()
    print(args.path, str(args.pdb))
    extract_ligands(args.path, str(args.pdb))

if __name__ == "__main__":
    main()
