"""
This code comapres the accession numbers in the concatenated accession number file "CATFILE"
with the individual accession number files from the accession numbers directory "ACNUM_DIR"

Reason being, for some reason the cat command from my terminal resulted in a CATFILE with
fewer accession numbers than the sum of all accession numbers in each file that was concatenated.
Upon inspection of results, CATFILE is missing accession numbers from the first or last line of
each accession number file...
I FOUND THE ANSWER. Shout out to Scottley. Each file being added to the CATFILE needs to end in a newline!
"""

import os

CATFILE = "/Users/rebeccachristensen/Desktop/Cremer_Lab_2022/dsrAB_Project_2022_Scripts/WGS_Datasets/" \
          "WGS_Accession_Numbers/wgs_accessionnum_combined_0201-022022.txt"
ACNUM_DIR = "/Users/rebeccachristensen/Desktop/Cremer_Lab_2022/dsrAB_Project_2022_Scripts/WGS_Datasets/" \
            "WGS_Accession_Numbers/02012022/"
NO_DUPS_CATFILE = "/Users/rebeccachristensen/Desktop/Cremer_Lab_2022/dsrAB_Project_2022_Scripts/WGS_Datasets/" \
          "WGS_Accession_Numbers/wgs_accessionnum_combined_0201-022022_nodups.txt"


def main():

    # read in catfile and accession numbers as a list
    with open(CATFILE,mode='r') as f:
        lines = f.readlines()
        cat_list = list(lines)

    os.chdir(ACNUM_DIR)

    # read in each accession number file, and accession numbers as a list
    for file in os.listdir(ACNUM_DIR):
        with open(file,mode='r') as f:
            compare_lines = f.readlines()
            compare_list = list(compare_lines)

            # compare accession numbers between accession number file and cat file
            # if accession num isn't in catfile, print accession number and the corresponding file name
            for accession_num in compare_list:
                if accession_num not in cat_list:
                    print(file)
                    print(accession_num)

    # check for duplicates in catfile
    setlist = set(cat_list)
    # print(len(setlist))
    # print(len(cat_list))

    # RESULT: 95,350 numbers in catfile. 73,495 numbers in set file. There are many duplicates!!!
    # next: remove duplicates! write set list to new file
    # with open(NO_DUPS_CATFILE, mode='w') as f:
    #     f.write(''.join(setlist))

    # check that no accession numbers were left behind in the catfile!
    for item in cat_list:
        if item not in setlist:
            print(item)
    # all accession numbers were accounted for :D


if __name__ == '__main__':
    main()