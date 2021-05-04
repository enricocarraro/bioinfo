"""
Assignment : Consensus Region

Write a python program that reconstructs the consensus regions on a specific
chromosome starting from a tab-separated file called alignments.txt made up
of three columns: the read ID, the sequence of the read and the alignment 
position of the read onto the reference genome. An example of alignments.txt
is available in this folder.

Exploiting the sequence and the alignment position of each read, build the 
consensus regions on the selected chromosome. Please note that all reads have
the same length and that multiple consensus regions are allowed for the same
chromosome.
"""

import sys

if len(sys.argv) != 4:
    raise Exception("Program needs 3 options.")

_, alignments_file, reference_genome_file, output_file = sys.argv

reference_genome_len = 0

with open(reference_genome_file, 'r') as ref:
    for line in ref:
        reference_genome_len += len(line.strip())

consensus = [{} for x in range(reference_genome_len)]


with open(alignments_file, 'r') as alignments:
    for line in alignments:
        _, cur_read, offset = line.split("\t")
        offset = int(offset)

        for i in range(len(cur_read)):
            if cur_read[i] in consensus[offset+i]:
                consensus[offset+i][cur_read[i]] += 1
            else:
                consensus[offset+i][cur_read[i]] = 1


with open(output_file, 'w') as output:
    original_stdout = sys.stdout
    sys.stdout = output
    last_skip = False
    for consensus_element in consensus:
        if len(consensus_element) == 0:
            print("", end = "" if last_skip else "\n")
            last_skip = True
        else:
            most_frequent = max([(consensus_element[x], x) for x in consensus_element])
            print(most_frequent[1], end="")
            last_skip = False

    sys.stdout = original_stdout
