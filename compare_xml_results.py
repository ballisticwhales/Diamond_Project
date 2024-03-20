import xml.etree.ElementTree as ET
from collections import Counter

def parse_xml_for_hits(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    hits = {}
    for iteration in root.findall('.//Iteration'):
        query_id = iteration.find('Iteration_query-ID').text
        query_def = iteration.find('Iteration_query-def').text
        iteration_hits = iteration.find('Iteration_hits')

        hits_for_iteration = []
        for hit in iteration_hits.findall('.//Hit'):
            hit_id = hit.find('Hit_id').text
            hit_def = hit.find('Hit_def').text

            hsp = hit.find('.//Hsp')
            hsp_qseq = hsp.find('Hsp_qseq').text if hsp is not None else None
            hsp_hseq = hsp.find('Hsp_hseq').text if hsp is not None else None

            hits_for_iteration.append((hit_id, hit_def, hsp_qseq, hsp_hseq, query_def))
        
        if hits_for_iteration:
            hits[query_id] = hits_for_iteration
    
    return hits


def compare_hits(*hits_files, output_file_path):
    def extract_ids(hits):
        return [hit_id for hits_list in hits.values() for hit_id, _, _, _, _ in hits_list]

    def write_hit_details(hits, ids, file):
        for query_id, hits_list in hits.items():
            for hit_id, hit_def, hsp_qseq, hsp_hseq, query_def in hits_list:
                if hit_id in ids:
                    file.write(f"Query ID: {query_id}, Query Definition: {query_def}\n")
                    file.write(f"Hit ID: {hit_id}, Hit Definition: {hit_def}\n")
                    if hsp_qseq and hsp_hseq:
                        file.write(f"Query Seq: {hsp_qseq}, Hit Seq: {hsp_hseq}\n")
                    file.write("\n")

    # Extract hit IDs from each file and count occurrences across all files
    all_hit_ids = [extract_ids(hits_file) for hits_file in hits_files]
    hit_id_counts = Counter(hit_id for file_hits in all_hit_ids for hit_id in file_hits)

    # Identify truly unique hits (those that appear exactly once across all files)
    unique_hit_ids = {hit_id for hit_id, count in hit_id_counts.items() if count == 1}

    # Find matched hits across all files
    matched_hits = set().union(*all_hit_ids)

    # Flatten hits_files into a single dictionary and remove duplicates
    combined_hits = {}
    for hits_file in hits_files:
        for query_id, hits_list in hits_file.items():
            if query_id not in combined_hits:
                combined_hits[query_id] = hits_list
            else:
                combined_hits[query_id].extend(h for h in hits_list if h not in combined_hits[query_id])

    with open(output_file_path, 'w') as file:
        # Iterate through each hits file for truly unique hits
        for i, hit_ids in enumerate(all_hit_ids):
            truly_unique_hits = set(hit_ids) & unique_hit_ids
            file.write(f"Total hits in file {i+1}: {len(hit_ids)}\n")
            file.write(f"Unique hits in file {i+1}: {len(truly_unique_hits)}\n")
            if len(truly_unique_hits) > 0:
                file.write(f"Details for unique hits in file {i+1}:\n")
                write_hit_details(hits_files[i], truly_unique_hits, file)
            else:
                file.write("\n")
    
        # Details for matched hits across all files
        file.write(f"Total matched hits: {len(matched_hits)}\n")
        file.write("Details for matched hits:\n")
        # Assuming matched hits details are the same in all files, write them using the last file
        write_hit_details(combined_hits, matched_hits, file)


# Define the base directory and the common part of the file name
base_dir = 'diamond_project/Task_1_results/results_'
file_paths = [base_dir + f'{i}.xml' for i in range(1, 10)]

# Parse XML files for hits using a loop
hits_files = [parse_xml_for_hits(file_path) for file_path in file_paths]

# Pass the list of hits files to the compare_hits function using the * operator to unpack the list
output_file_path = 'hits_comparison_output_task_1.txt'
compare_hits(*hits_files, output_file_path=output_file_path)

file_path1 = "diamond_project/Task_1_results/results_2.xml"
file_path2 = "diamond_project/Task_2_results/merged_10_through_1_and_2.xml"

hit_file1 = parse_xml_for_hits(file_path1)
hit_file2 = parse_xml_for_hits(file_path2)

output_file_path = 'hits_comparison_output_task_2.txt'
compare_hits(hit_file2, hit_file2, output_file_path=output_file_path)

file_path3 = "diamond_project/Task_1_results/results_9.xml"
file_path4 = "diamond_project/Task_3_results/result123456789.xml"

hit_file3 = parse_xml_for_hits(file_path3)
hit_file4 = parse_xml_for_hits(file_path4)

output_file_path = 'hits_comparison_output_task_3.txt'
compare_hits(hit_file3, hit_file4, output_file_path=output_file_path)