import csv
import subprocess
import random
import string
import argparse
import pandas as pd

def generate_random_name(length=3):
    """Generate a random name of specified length."""
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))

def run_autodock_protocol(smiles, ligand_name, pdb_code):
    """Run the Autodock protocol with the given parameters."""
    try:
        command = ["./generate_pdb_with_ref.sh", smiles, ligand_name, pdb_code]
        print(command)
        subprocess.run(command, check=True)  # Add check=True to raise exception on non-zero exit code
    except subprocess.CalledProcessError as e:
        print(f"Error running Autodock protocol for PDB code {pdb_code}: {e}")

def main(csv_file):
    """Main function to read CSV file and execute Autodock protocol."""
    df = pd.read_csv(csv_file)
    df_smiles = df.dropna(subset=["smiles"])
    smiles = df_smiles['smiles'].tolist()
    pdbs = df['pdb'].tolist()
    for smile in smiles:
        ligand_name = generate_random_name()
        for pdb in pdbs:
            run_autodock_protocol(smile, ligand_name, pdb)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Makes all the dockings')
    parser.add_argument('csv', type=str, help='csv file')
    args = parser.parse_args()
    csv_file = args.csv # Update with your CSV file path
    main(csv_file)