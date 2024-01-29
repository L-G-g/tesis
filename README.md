# Crystallographic Data Retrieval
## Installation
Clone the repository in the desired directory:
```bash
git clone https://github.com/L-G-g/tesis.git
```

## Usage

To retrieve crystallographic data, use the following command to search for PDB (Protein Data Bank) crystals that match a specific UniProt with annotated Pfam domains and specific small molecules from ChEMBL (Chemical Entities of Biological Interest):

```bash
python query_to_pdb_parseable.py P00918 PF00194 CHEMBL578165 CHEMBL573209 CHEMBL567820 CHEMBL567821 CHEMBL3343261 CHEMBL441343 CHEMBL575341 CHEMBL3760079 CHEMBL65369
```

(OPTIONAL) If you have a `candidate_targets.csv` file, you can generate a candidate list in the form of a text file using the following command:

```bash
python prepare_candidate_list.py
python query_to_pdb_parseable.py --file candidate_list.txt
```

Output:
- `pdb_id.txt`: A text file containing the desired PDB IDs.
