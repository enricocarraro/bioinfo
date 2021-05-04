# Assignment:
#
# Write a python program that generates both fasta and fastq files containing reads with the following characteristics:
# -Read id contains a progressive number starting from 0. -Sequences have length 50 bp
# -Bases are randomly generated using a A,T,C,G alphabet, but probability of each base for each read should be given from the command line as a set of numbers (probA, probT, probC, probG)
# -The number of reads should be passed as an argument from the command line
# -The name of the fasta/fastq file should be passed as an argument from the command line
# -For fastq files only: the quality of each base is randomly selected.
# Example:
# python3 program.py simulatedfasta.fa 100 30 30 30 10


import random
import sys
from itertools import accumulate

if len(sys.argv) != 7:
    raise Exception("Program needs 7 parameters.")

_, output_file, sequences, *probs = sys.argv

probs = list(map(int, probs))
prefix_probs = list(accumulate(probs))

print(output_file, sequences, probs)

fa = output_file.endswith(".fa")

with open(output_file, 'w') as fast:
    original_stdout = sys.stdout
    sys.stdout = fast

    for sequence in range(0, int(sequences)):
        print(">" if fa else "@", sequence, sep='')
        t, a, c, g = [0, 0, 0, 0]
        for char in range(50):
            toss = random.randint(1, 101)
            if toss <= prefix_probs[0]:
                print("T", end="")
                t += 1
            elif toss <= prefix_probs[1]:
                print("A", end="")
                a += 1
            elif toss <= prefix_probs[2]:
                print("C", end="")
                c += 1
            else:
                print("G", end="")
                g += 1
        print("")
        if not fa:
            print("@", sequence, sep='')
            print(
                ''.join(list(map(chr, [random.randint(33, 73) for _ in range(50)]))))

    sys.stdout = original_stdout
