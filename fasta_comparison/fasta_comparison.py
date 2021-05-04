"""
Assignment: Fasta comparison

Write a python program to compare two fasta files. 
The two fasta files are passed as first and second argument from the command line.
The two fasta files have the following characteristics:
-The fasta format of the two files is correct (no need to check the format) 
-Each read can take up one or multiple lines
-Each input file does not contain duplicated reads (i.e. identical reads)

The program must write as output a third fasta file containing only the reads that
are in common between the input files. The read ids in the output file should be
composed by the read id of the first file concatenated with the read id of the 
second file.
"""
import sys

if len(sys.argv) != 4:
    raise Exception("Program needs 3 options.")

_, input_file1, input_file2, output_file = sys.argv

with open(input_file1, "r") as fast:
    sequence = ""
    sequences = dict()
    for line in fast:
        if line.startswith(">"):
            # READ ID
            if len(sequence) > 0:
                sequences[sequence] = read_id
            sequence = ""
            read_id = line[1:-1]
        else:
            # SEQUENCE
            sequence += line[:-1]

with open(output_file, "w") as output:
    original_stdout = sys.stdout
    sys.stdout = output

    with open(input_file2, "r") as fast:
        for line in fast:
            if line.startswith(">"):
                # READ ID
                if len(sequence) > 0 and sequence in sequences:
                    print(
                        input_file1,
                        "-",
                        sequences[sequence],
                        "<-->",
                        input_file2,
                        "-",
                        read_id,
                    )
                read_id = line[1:-1]
                sequence = ""
            else:
                # SEQUENCE
                sequence += line[:-1]

    sys.stdout = original_stdout
