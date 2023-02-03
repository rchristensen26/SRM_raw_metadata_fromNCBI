""""
Remove "NZ_"-prefixed accession numbers and duplicate accession numbers from compiled CSV file of
WGS datasets (as a selector table in CSV format downloaded from NCBI.

INPUT: compiled WGS selector table
OUTPUT: *clean* compiled WGS selector table
"""

import sys
import csv
import os

wgs_selector = sys.argv[1]
wgs_selector_clean = os.path.splitext(os.path.basename(wgs_selector))[0] + "_clean.csv"

accession_num_list = []  # make a list to keep track of duplicate accession numbers

n_row = 0
n_row_clean = 0

with open(wgs_selector, mode='r') as f_read:  # open file and parse as csv file in read mode
    with open(wgs_selector_clean, mode='w') as f_write:
        csv_reader = csv.reader(f_read)
        csv_writer = csv.writer(f_write)

        next(csv_reader)  # skip header in first line

        for row in csv_reader:  # parse accession numbers row by row
            n_row += 1
            accession_num = row[0]
            # check if accession number already accession number list
            if accession_num not in accession_num_list:
                accession_num_list.append(accession_num)
                # check if "NZ_" in prefix
                if "NZ_" not in accession_num:
                    n_row_clean += 1
                    csv_writer.writerow(row)

print("N rows in original selector table: " + str(n_row))  # expected: 111,914. actual: 111,981
print("N rows in CLEAN selector table: " + str(n_row_clean))  # expected: 73,495. actual: 73496
# check which accession numbers are missing from accession number list!
# all accession numbers are accounted for ...

# with open("/Users/rebeccachristensen/Desktop/Cremer_Lab_2022/dsrAB_Project_2022_Scripts/WGS_Datasets/WGS_Accession_Numbers/wgs_accessionnum_combined_0201-022022_nodups.txt") as f:
#     accession_num_file = f.read()
#     accession_num_file_list = accession_num_file.split()
#
# for accession_num in accession_num_list:
#     if "NZ_" not in accession_num:
#         if accession_num not in accession_num_file_list:
#             print(accession_num)
#
# for accession_num in accession_num_file_list:
#     if accession_num not in accession_num_list:
#         print(accession_num)
