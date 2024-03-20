from Bio import SeqIO

# Initialize an empty list to hold all the records to be merged
merged_records = []

# Loop through each batch file, except the one you don't want to include
for i in range(10):
    if i == 0:
        continue
    
    batch_filename = f"batch_{i + 1}.fa"
    # Read the records from this batch and add them to the merged_records list
    batch_records = list(SeqIO.parse(batch_filename, "fasta"))
    merged_records.extend(batch_records)

# Specify the filename for the merged file
merged_filename = "merged_batches.fa"

# Write all the records to the new file
SeqIO.write(merged_records, merged_filename, "fasta")
