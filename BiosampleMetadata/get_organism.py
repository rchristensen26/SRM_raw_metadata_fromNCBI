"""
Get the organism ID for each BioSample from the NCBI metadata text file.
Later, I will append the organism ID column by BioSample ID, and we can
decide if we want to remove BioSamples with assigned organism names.
"""

import re
import pandas as pd

# read in metadata file (text file from NCBI ugh)
metadata_file = open("biosample_metadata_2021and2022.txt", 'r')

lines = metadata_file.readlines()

samples = []
organisms = []

for line in lines:
    line = line.rstrip("\n")
    if re.search("Identifiers: BioSample: ", line):
        sample = re.sub(r'Identifiers: BioSample: ', "", line)
        sample = re.sub(r';(.*)', "", sample)
        samples.append(sample)
    if re.search("Organism:", line):
        organism = re.sub(r'Organism: ', "", line)
        organisms.append(organism)

df = pd.DataFrame(list(zip(samples, organisms)),
                  columns=["sample_id", "organism"])

print("samples: " + str(len(samples)))
print("organisms: " + str(len(organisms)))
pd.DataFrame(df).to_csv("sample_organisms_2021and2022data.txt")
