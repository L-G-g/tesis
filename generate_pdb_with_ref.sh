#!/bin/bash




# Check if Open Babel is installed
if ! command -v obabel &> /dev/null; then
    echo "Error: Open Babel is not installed. Please install it before running this script."
    exit 1
fi

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <SMILES_notation> <ChemBL> <Uniprot>"
    exit 1
fi



# Assign arguments to variables
smiles="$1"
ChemBL="$2"
pdb="${ChemBL}.pdb"
pdbqt="${ChemBL}.pdbqt"
r="$3"
receptor="${r}.pdb"
receptor_pdbqt="${receptor}qt"
r_maps_fld="${r}.maps.fld"

# Creates the directory
mkdir -p ""$ChemBL"_"$r""
cd ""$ChemBL"_"$r""

# Downloading the PDB file
wget -O "./$receptor" "https://files.rcsb.org/download/$receptor"

# Checking if download was successful
if [ $? -eq 0 ]; then
    echo "Download successful: $receptor is saved in the current working directory"
else
    echo "Download failed. Please verify the PDB code and try again."
fi


# Create directory if it doesn't exist
#output_dir="$r"
#mkdir -p "$output_dir"
output_dir=$(pwd)

# Run ligand extraction script
python3 ../ligand_extraction.py $output_dir --pdb $receptor &> /dev/null

# Move ligand files to output directory
#mv lig_*.pdb "$output_dir"

# Prompt user to choose from estructural ligands
ligand_files=("$output_dir"/lig_*.pdb)
if [ ${#ligand_files[@]} -eq 0 ]; then
    echo "No ligand files found."
    exit 1
fi

echo "Choose a ligand file:"
select ligand_file in "${ligand_files[@]}"; do
    if [ -n "$ligand_file" ]; then
        echo "You selected: $ligand_file"
        break
    else
        echo "Invalid selection."
    fi
done

# Assign output name to variable
ligand_pdbqt_full="${ligand_file%.*}.pdbqt"
# Extract filename with extension
ligand_pdbqt=$(basename "$ligand_pdbqt_full")

# Run the pdbqt transformation for the estructural ligand
output_estructural_pdbqt=$(pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -A hidrogens -l "$ligand_file" -o "$ligand_pdbqt" 2>&1)

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "Estructural ligand conversion successful. Output saved to $ligand_pdbqt."
else
    warning_message=$(echo "$output_estructural_pdbqt" | grep "WARNING:")
    echo "$warning_message"
fi

# Run Open Babel command
obabel -:"$smiles" -opdb --gen3d -O "$pdb" &> /dev/null

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "New ligand pdb conversion successful. Output saved to $pdb."
else
    echo "Error during conversion. Please the new ligand and try again."
fi

# Run the pdbqt transformation for the estructural ligand
pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l "$pdb" -o "$pdbqt" &> /dev/null

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "New ligand pdbqt conversion successful. Output saved to $pdbqt"
else
    echo "Error during conversion. Please the new ligand and try again."
fi

# Ron the random state transformation for the scructural ligand
pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/write_random_state_ligand.py -l "$pdbqt" -o ligando_dock.pdbqt &> /dev/null

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "Succesful random state transformation. Output saved to $pdbqt"
else
    echo "Unsuccesful random state transformation"
fi

# Run the receptor transformation, if needed it takes the first conformation.
output_prepare_receptor=$(pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -A hydrogens -r "$receptor" -o "$receptor_pdbqt" 2>&1)

if [[ "$output_prepare_receptor" == *"WARNING!"* ]]; then
        echo "Multiple conformations found. Will proceed with the first one"
        pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_pdb_split_alt_confs.py -r "$receptor" &> /dev/null
        r_maps_fld="${r}_A.maps.fld"
        receptor_A="${r}_A.pdb"
        receptor_A_pdbqt="${receptor_A}qt"
        pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -A hydrogens -r "$receptor_A" -o "$receptor_A_pdbqt" &> /dev/null
        receptor_pdbqt=$receptor_A_pdbqt

        if [ $? -eq 0 ]; then
            echo "Receptor pdbqt conversion successful. Output saved to $receptor_A_pdbqt."
        else
            echo "Error during conversion. Please check your input and try again."
        fi
else
    echo "Initial receptor pdbqt conversion successful. Output saved to $receptor_pdbqt."
fi

# Prepare a gfp with the estructural ligand to extract the gridcenter
output_gpf=$(pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_gpf4.py -y -l $ligand_pdbqt -r $receptor_pdbqt -o receptor_coordenadas.gpf 2>&1)

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "Estructural ligand conversion successful. Output saved to $ligand_pdbqt."
else
    warning_message=$(echo "$output_gpf")
    echo "$warning_message"
fi

# Run grep command to find the line containing "gridcenter"
output=$(grep "gridcenter" receptor_coordenadas.gpf)

# Extract coordinates using awk
coordinates=$(echo "$output" | awk '{print $2,$3,$4}')

# Replace spaces with commas
coordinates=${coordinates// /,}

# Format the output string
gridcenter="gridcenter='$coordinates'"

# Print the formatted output
pythonsh /home/gabi/tools/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_gpf4.py -l $pdbqt -r $receptor_pdbqt -p gridcenter=$coordinates -o receptor.gpf &> /dev/null

if [ $? -eq 0 ]; then
    echo "Final gpf generation successful, output save to receptor.gpf"
else
    echo "Error during final gpf generation. Please check your input and try again."
fi
# Make the map
autogrid4 -p receptor.gpf -l receptor.glg # no genera el mapa de nitrogeno

if [ $? -eq 0 ]; then
    echo "Maps generation successfull"
else
    echo "Error during final gpf generation. Please check your input and try again."
fi

# Run the
autodock_gpu_64wi -ffile $r_maps_fld -lfile ligando_dock.pdbqt -nrun 100 -gbest 1