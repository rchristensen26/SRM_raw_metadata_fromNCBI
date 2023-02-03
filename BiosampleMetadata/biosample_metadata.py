"""
parses biosample metadata from NCBI text files, and adds sample info to each
corresponding wgs project. (Multiple wgs projects/contigs can come from the same sample.)

INPUT: 
    METADATA_INPUT: NCBI text files of biosample metadata
    QUERY_INFO: compiled csv file of all query info (does not contain sample ID)
    WGS_SELECTOR: csv file with sparse metadata and wgs project id

OUTPUT:
    BIOSAMPLE_METADATA_OUT: json with parsed biosample metadata
    QUERY_INFO_METADATA: query info csv with added sample metadata for each query seq

"""

import json
import csv
import os


biosample_metadata = "/Users/rebeccachristensen/Desktop/Cremer_Lab_2022/dsrAB_Project_2022_Scripts/BiosampleMetadata/2021_metadata_files/biosample_metadata_2021.txt"
basename = os.path.splitext(os.path.basename(biosample_metadata))[0]
biosample_metadata_csv = basename + ".csv"
biosample_metadata_json = basename + ".json"

wgs_selector = "/Users/rebeccachristensen/Desktop/Cremer_Lab_2022/dsrAB_Project_2022_Scripts/BiosampleMetadata/2021_metadata_files/wgs_selector_2021.csv"

biosample_list = "/Users/rebeccachristensen/Desktop/Cremer_Lab_2022/dsrAB_Project_2022_Scripts/BiosampleMetadata/2021_metadata_files/biosample_list_2021.txt"


def main():

    metadata_dict = parse_sample_metadata(biosample_metadata)

    with open(biosample_metadata_json, 'w') as f:
        json.dump(metadata_dict, f, indent=4)

    # add_metadata_to_query_info(metadata_dict, QUERY_INFO)
    #
    # species_list = get_species(QUERY_INFO)
    #
    # metadata_dict = add_queryinfo_to_metadata(metadata_dict, QUERY_INFO_METADATA, species_list)
    #
    # with open(METADATA_OUT, mode='w') as f:
    #     json.dump(metadata_dict, f, indent=4)
    #
    make_metadata_csv(metadata_dict, biosample_metadata_csv)

    check_sample_in_dict(metadata_dict, biosample_list)


def parse_sample_metadata(metadata_in):
    samples_dict = {}

    samples_list = as_lists(metadata_in)

    parse_list(samples_list, samples_dict)

    add_query_id(samples_dict, wgs_selector)

    return samples_dict


def as_lists(infile):
    file = open(infile, mode='r')

    all_list = []

    sublist = []

    for line in file:
        line = line.strip()
        if line != "":
            sublist.append(line)
        elif line == "" and len(sublist) != 0:
            all_list.append(sublist)
            sublist = []

    return all_list


def parse_list(inlist, sdict):
    for sample in inlist:
        parse_sample(sample, sdict)


def parse_sample(sample_l, sdict):
    for line in sample_l:
        if "Identifiers:" in line:
            id_l = line.split("Identifiers: BioSample: ")
            id_l = id_l[1].split(";")
            s_id = id_l[0]
            sdict[s_id] = {}

        if line.startswith("/"):

            line = line.strip("/")
            line = line.split("=")

            attr = line[0]
            val = line[1].strip("\"")

            if attr != "sample_id":
                sdict[s_id][attr] = val


def add_query_id(metadata_dict, wgs_selector):
    csv_reader = csv.DictReader(open(wgs_selector, mode='r'))

    for sample, values in metadata_dict.items():
        metadata_dict[sample]["query_ids"] = []

    for row in csv_reader:
        query_id = row["prefix_s"]
        sample_id = row["biosample_ss"]

        if sample_id in metadata_dict.keys():
            metadata_dict[sample_id]["query_ids"].append(query_id)


def add_metadata_to_query_info(metadata_dict, query_info_csv):
    csv_reader = csv.DictReader(open(query_info_csv, mode='r'))

    fieldnames = csv_reader.fieldnames

    attr_l = ["query_prefix", "sample_id1"]

    new_fieldnames = add_fieldnames(metadata_dict, attr_l)

    fieldnames.extend(new_fieldnames)

    csv_writer = csv.DictWriter(open(QUERY_INFO_METADATA, mode='w'), fieldnames=fieldnames)

    csv_writer.writeheader()

    for row in csv_reader:
        query_prefix = row["id"].partition(".")[0]
        row["query_prefix"] = query_prefix
        for sample, values in metadata_dict.items():
            if query_prefix in values["query_ids"]:
                row["sample_id1"] = sample
                for attr, val in values.items():
                    row[attr] = val

        csv_writer.writerow(row)


def add_fieldnames(metadata_dict, o_list):

    for sample, values in metadata_dict.items():
        for attribute in values.keys():
            if attribute not in o_list:
                o_list.append(attribute)

    return o_list


def get_species(query_info_csv):
    species_l = []
    csv_reader = csv.DictReader(open(query_info_csv, mode='r'))

    for row in csv_reader:
        species = row["closest_ref"]
        if species not in species_l:
            species_l.append(species)

    return species_l


def add_queryinfo_to_metadata(metadata_dict, query_metadata_csv, species_list):
    csv_reader = csv.DictReader(open(query_metadata_csv, mode='r'))

    # make dict for query info nested into each sample dict
    # for sample, values in metadata_dict.items():
    #     values["query_info"] = {}
    #     for query in values["query_ids"]:
    #         values["query_info"][query] = {}
    #
    # for row in csv_reader:
    #     sample_id = row["sample_id1"]
    #
    #     if sample_id in metadata_dict.keys():
    #         query = row["query_prefix"]
    #
    #         dict_nest = metadata_dict[sample_id]["query_info"][query]
    #
    #         dict_nest["region"] = row["region"]
    #         dict_nest["e_dups"] = row["n_edups"]
    #         dict_nest["dist"] = row["dist"]
    #
    #         closest_ref = row["closest_ref"].strip("[]")
    #         closest_ref = closest_ref.strip("\'")
    #         dict_nest["closest_ref"] = closest_ref

    for sample, values in metadata_dict.items():
        for species in species_list:
            values[species] = 0

    for row in csv_reader:
        sample_id = row["sample_id1"]

        if sample_id in metadata_dict.keys():
            species = row["closest_ref"]

            metadata_dict[sample_id][species] = 1

    for sample, values in metadata_dict.items():
        tot_species = 0
        for species in species_list:
            if values[species] > 0:
                tot_species += 1
        metadata_dict[sample]["tot_species"] = tot_species
    
    return metadata_dict


def make_metadata_csv(metadata_dict, metadata_file):
    fieldnames = add_fieldnames(metadata_dict, ["sample_id"])

    csv_writer = csv.DictWriter(open(metadata_file, mode='w'), fieldnames=fieldnames)

    csv_writer.writeheader()

    for sample, values in metadata_dict.items():
        row = {}
        row["sample_id"] = sample
        for attr, val in values.items():
            row[attr] = val

        csv_writer.writerow(row)


def check_sample_in_dict(metadata_dict, sample_list_f):
    with open(sample_list_f, 'r') as f:
        sample_f = f.read()
        samples = sample_f.split()

    n_samples_notInCSV = []
    for sample in samples:
        if sample not in metadata_dict.keys():
            n_samples_notInCSV.append(sample)

    with open("samplesNotInCSV.txt", 'w') as f:
        for sample in n_samples_notInCSV:
            f.write(sample)
            f.write("\n")


if __name__ == '__main__':
    main()
