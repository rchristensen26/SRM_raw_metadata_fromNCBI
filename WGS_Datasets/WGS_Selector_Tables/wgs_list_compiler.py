""""
This code parses a wgs_selector cvs table (from NBI's WGS Selector Tool) in order to
create a list of WGS accession numbers to be used as the input when downloading
WGS datasets (re: "prefetch" command). This code also filters out duplicate accessions
with the "NZ_" prefix.

INPUT
    WGS_SELECTOR_CVS: CVS file downloaded from NCBI's WGS Selector Tool. Table in CVS
        format with "prefix_s" in the first column, which is the accession numbers.

OUTPUT
    wgs_accession_num_file: Text file with compiled accession numbers from WGS_SELECTOR_CVS,
        separated by a space
"""

import csv
import os

WGS_SELECTOR_CVS = "wgs_selector_isolationsource_faec_02022022.csv"
WGS_SELECTOR_DIR = "/Users/rebeccachristensen/Desktop/Cremer_Lab_2022/dsrAB_Project_2022_Scripts/" \
                   "WGS_Datasets/WGS_Selector_Tables/02012022"
WGS_ACCESSION_NUM_DIR = "/Users/rebeccachristensen/Desktop/Cremer_Lab_2022/dsrAB_Project_2022_Scripts/WGS_Datasets/" \
                        "WGS_Accession_Numbers/02012022"


def main():
    accession_num_list = parse_wgs_selector(WGS_SELECTOR_CVS, [])  # compile list of accession numbers from csv file

    make_accession_num_file(accession_num_list)


def parse_wgs_selector(wgs_selector, accession_num_list):
    os.chdir(WGS_SELECTOR_DIR)
    with open(wgs_selector, mode='r') as f_read:  # open file and parse as csv file in read mode
        csv_reader = csv.reader(f_read)

        next(csv_reader)  # skip header in first line

        for row in csv_reader:  # parse accession numbers row by row
            accession_num = row[0]

            if "NZ_" in accession_num:  # skip over row if accession number as "NZ_" prefix
                continue

            accession_num_list.append(accession_num)  # add accession num to list

    return accession_num_list


def make_accession_num_file(accession_num_list):
    os.chdir(WGS_ACCESSION_NUM_DIR)

    # create new file for the list of accession numbers, using the naming convention for the input csv file
    wgs_accession_num_file = WGS_SELECTOR_CVS.replace("selector", "accessionnum")

    with open(wgs_accession_num_file, mode='w') as f:
        f.write("\n".join(accession_num_list))  # write list as space-separated string to accession number output file


if __name__ == '__main__':
    main()
