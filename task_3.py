import os
import subprocess

merger_script_path = "/home/mr3392/iBLAST/source/BlastpMergerModule.py"
file_base_path = "/home/mr3392/diamond_project/"
'''
# Loop through the first 9 files to create DIAMOND databases
for i in range(1, 10):
    fa_file = f"{file_base_path}batch_{i}"
    db_command = f"diamond makedb --in {fa_file}.fa -d {fa_file}.dmnd"
    os.system(db_command)  # Create the database
'''
# Run batch_10.fa through each database and output as XML
results = []
for i in range(1, 10):
    db_file = f"{file_base_path}batch_{i}.dmnd"
    output_file = f"{file_base_path}result{i}.xml"
    blast_command = f"diamond blastp -d {db_file} -q {file_base_path}batch_10.fa -o {output_file} -f 5 --ultra-sensitive"
    os.system(blast_command)
    results.append(output_file)

# Now, to incrementally merge the result files
merged_result = results[0]
for i in range(1, len(results)):
    output_file = os.path.join(file_base_path, f"result{''.join([str(j) for j in range(1, i+2)])}.xml")
    merge_command = f"python3 {merger_script_path} {merged_result} {results[i]} {output_file}"
    subprocess.run(merge_command, shell=True)
    merged_result = output_file  # Update merged_result to the latest merged file

print(f"Final merged file: {merged_result}")
