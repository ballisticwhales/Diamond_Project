import subprocess
import time

# List to store timing results
timing_results = []

merger_script_path = "/home/mr3392/iBLAST/source/BlastpMergerModule.py"
file_base_path = "diamond_project/Task_2_results/"

for i in range(1, 3):  # run through batch 1 and 2
    start_time = time.time()

    db_name = f"diamond_project/batch_{i}.dmnd"
    diamond_command = f"diamond blastp -q diamond_project/batch_10.fa -d {db_name} -o {file_base_path}results_10_through_{i}.xml -f 5 --ultra-sensitive"
    subprocess.run(diamond_command, shell=True)

    end_time = time.time()
    elapsed_time = end_time - start_time
    timing_results.append((db_name, elapsed_time))
    
    print(f"Database {db_name}: Blast run completed in {elapsed_time} seconds.")

with open(f'{file_base_path}timing_results_2.txt', 'w') as f:
    for db_name, elapsed_time in timing_results:
        f.write(f"{db_name}: {elapsed_time} seconds\n")

output_file = "merged_10_through_1_and_2.xml"
merge_command = f"python3 {merger_script_path} {file_base_path}results_10_through_1.xml {file_base_path}results_10_through_2.xml {output_file}"
subprocess.run(merge_command, shell=True)