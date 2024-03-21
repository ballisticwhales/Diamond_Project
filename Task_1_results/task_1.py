import subprocess
import time

# List to store timing results
timing_results = []
file_base_path = "diamond_project/Task_1_results/"

for i in range(1, 10):  # From 2 to 9
    db_name = f"{file_base_path}training_db_1_to_{i}.dmnd"

    # Run "Fold 10" against the current database and time the run
    start_time = time.time()
    
    diamond_command = f"diamond blastp -q diamond_project/batch_10.fa -d {db_name} -o {file_base_path}results_{i}.xml -f 5 --ultra-sensitive"
    subprocess.run(diamond_command, shell=True)

    end_time = time.time()
    elapsed_time = end_time - start_time
    timing_results.append((i, elapsed_time))
    
    print(f"Database {db_name}: Blast run completed in {elapsed_time} seconds.")

with open('timing_results.txt', 'w') as f:
    for i, elapsed_time in timing_results:
        f.write(f"DB {i}: {elapsed_time} seconds\n")