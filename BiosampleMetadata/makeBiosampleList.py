""""
Extract biosample IDs from the wgs selector table. Create new file with list of biosample IDs to be
searched on NCBI for metadata.

INPUT:
    wgs_selector: wgs_selector table of accession numbers (without duplicate accessions and "NZ_" prefix)
    batch_size: size of biosample ID batches to search (will be separated by newline for readability)

OUTPUT:
    biosample_list_outputf: file with nonduplicate biosample IDs in batches

"""

import csv
import sys

wgs_selector = sys.argv[1]
# biosample_list_outputf = sys.argv[2]
# batch_size = int(sys.argv[3])

reader = csv.DictReader(open(wgs_selector, mode='r'))

biosample_list = []
n = 0

for row in reader:
    n += 1
    biosample = row["biosample_ss"]
    if biosample not in biosample_list:
        biosample_list.append(biosample)

print("number of biosamples: " + str(len(biosample_list)))
print("number of wgs accession numbers: " + str(n))

# with open(biosample_list_outputf, mode='w') as outfile:
#     for i in range(0, len(biosample_list), batch_size):
#         outfile.write(" ".join(biosample_list[i:i+batch_size:1]))
#         outfile.write("\n")
