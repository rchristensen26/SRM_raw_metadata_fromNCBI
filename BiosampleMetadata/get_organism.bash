#!/bin/bash
metadata_file="biosample_metadata_practice.txt"
#cat $metadata_file | while read line; do
#  sample=$(grep "BioSample" \
#  | sed "s/Identifiers: BioSample: //" \
#  | sed "s/\;.*//")
#  echo $sample
#  organism=$(grep "Organism:" \
#  | sed "s/Organism: //")
#  echo $sample","$organism
#  echo $line
IFS=$'\n'
lines=$(cat $metadata_file)
for line in $lines; do
  echo $line
  sample=$(grep "BioSample")
  echo $sample
#  organism=$(grep "Organism:" \
#  | sed "s/Organism: //")
#  echo $sample","$organism
#  echo $line
done
