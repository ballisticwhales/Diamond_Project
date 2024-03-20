from Bio import SeqIO
import math

# Load sequences
filename = "astral-scopedom-seqres-gd-sel-gs-bib-40-2.07.fa"
records = list(SeqIO.parse(filename, "fasta"))

# Determine batch size
batch_size = math.ceil(len(records) / 10)

# Split into batches and save
for i in range(10):
    batch_records = records[i * batch_size:(i + 1) * batch_size]
    batch_filename = f"batch_{i + 1}.fa"
    SeqIO.write(batch_records, batch_filename, "fasta")