import pandas as pd

# Replace 'your_file.csv' with the actual path to your CSV file
file_path = 'candidate_targets.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)
df = df.drop(df.columns[[0, 3]], axis=1)
df[df.columns[0]], df[df.columns[1]] = df[df.columns[1]].copy(), df[df.columns[0]].copy()
df['Domain-binding similar ligands'] = df['Domain-binding similar ligands'].str.replace(',', '')
df[df.columns[0]] = df['Pfam'].str.extract(r'\|(.*?)\|')


with open('candidate_list.txt', 'w') as f:
    for _, row in df.iterrows():
        line = f"{row['Pfam']} {row['Protein']} {row['Domain-binding similar ligands'].replace(',', '')}\n"
        f.write(line)

        
