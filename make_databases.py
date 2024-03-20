from Bio import SeqIO

# This function will merge the batches into a single file and build a Diamond database
def build_diamond_db(batches, db_name):
    merged_records = []
    for batch_num in batches:
        batch_filename = f"diamond_project/batch_{batch_num}.fa"
        batch_records = list(SeqIO.parse(batch_filename, "fasta"))
        merged_records.extend(batch_records)
    merged_filename = f"{db_name}.fa"
    SeqIO.write(merged_records, merged_filename, "fasta")
    
    # Build the Diamond database
    subprocess.run(["diamond", "makedb", "--in", merged_filename, "-d", db_name])

for i in range(1, 10):  # From 2 to 9
    db_name = f"diamond_project/Task_1_results/training_db_1_to_{i}"
    build_diamond_db(range(1, i + 1), db_name)  # Build database with batches 1 to i