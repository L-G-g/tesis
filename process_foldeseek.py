import pandas as pd
import os

def read_m8_files(folder_path):
    # Creates the list of paths
    m8_files = [
        os.path.join(folder_path, filename)
        for filename in os.listdir(folder_path)
        if filename.endswith(".m8")
    ]

    # Creates the cols names and a list to store the dataframes
    cols = "query pdb_desc fident alnlen mismatch gapopen	qstart qend tstart tend x10	x11	x12	x13	x14	seq1 seq2 nums seq3 tax taxname".split()
    dataframes = []
    
    for file_path in m8_files:
        df = pd.read_csv(file_path, sep="\t", names=cols, index_col=False)
        df = df.dropna(subset=["pdb_desc"])
        df = df.dropna(subset=["taxname"]) 
        df = df[df['taxname'] == 'Homo sapiens'] # Saves sapiens entrys with descriptor.
        if file_path == '/home/gabi/tesis/1BYQ_P07900_FoldSeek_res/alis_pdb100.m8': # Handles the pdb100
            df["pdb_desc"] = [x.split("_")[0] for x in df.pdb_desc]
            df["pdb_desc"] = [x.split(".")[0] for x in df.pdb_desc]
        elif file_path == '/home/gabi/tesis/1BYQ_P07900_FoldSeek_res/alis_cath50.m8': # Handles the CATH
            df['codes'] = [x.split("_") for x in df.pdb_desc]
            df["pdb_desc"] = [x[0][:4] if len(x) == 1 else x[1] for x in df['codes']]
            df.drop(columns=['codes'], inplace=True)
        else: # Handles the AF
            df["pdb_desc"] = [x.split(" ")[0] for x in df.pdb_desc]
            df["pdb_desc"] = [x.split("-")[1] for x in df.pdb_desc]
            pass
        if not df.empty:
            dataframes.append(df)
    return dataframes

# Path to the FoldSeek res folder.
folder_path = "/home/gabi/tesis/1BYQ_P07900_FoldSeek_res" 

# Process each db into a dataframe and saves it into a list.
dataframes = read_m8_files(folder_path)

if dataframes:
    print('Files found!')
else:
   print("No .m8 files found in the specified folder.")

concatenated_df = pd.concat(dataframes)
concatenated_df.to_csv('foldseek_res.csv', index=False)
