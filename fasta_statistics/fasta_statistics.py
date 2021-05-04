""" 
Assignment: Statistics extraction
Write a python program for extracting statistics from fasta/fastq files. 
The program must take as a first argument from the command line the name of the input fasta file
to be analyzed and write to an output text file (whose name is passed as a second argument from
the command line) a summary of the computed statistics.
The following are the expected output statistics:
- Statistics of single bases across all the reads: Number of A,T,C,G
- Number of reads having at least one low complexity sequence: AAAAAA, TTTTTT, CCCCCC or GGGGGG.
- Number of reads having the number of GC couples (so called GC content) higher than a threshold
  GC_THRESHOLD passed as third argument from the command line
- For each read having a GC content higher than GC_THRESHOLD, report the read_id and the number of GC couples
"""
import sys

if len(sys.argv) != 4:
    raise Exception("Program needs 3 options.")

_, input_file, output_file, gc_threshold = sys.argv

gc_threshold = int(gc_threshold)

with open(output_file, "w") as stats:
    original_stdout = sys.stdout
    sys.stdout = stats
    with open(input_file, "r") as fast:
        freq = {}
        low_complexity_subsequences = list(
            map(lambda str: str * 6, ["A", "T", "C", "G"])
        )
        for line in fast:
            if line.startswith(">"):
                # READ ID
                read_id = line[1:-1]
                gc_count = 0
                has_low_complexity_seq = 0
            else:
                # SEQUENCE
                for element in range(0, len(line) - 1):
                    char = line[element]
                    freq[char] = freq.get(char, 0) + 1
                    if element > 0 and line[element - 1 : element + 1] == "GC":
                        gc_count += 1
                    if (
                        has_low_complexity_seq == 0
                        and element >= len(low_complexity_subsequences[0]) - 1
                    ):
                        for low_complexity_subseq in low_complexity_subsequences:
                            if (
                                line[
                                    element
                                    - len(low_complexity_subseq)
                                    + 1 : element
                                    + 1
                                ]
                                == low_complexity_subseq
                            ):
                                has_low_complexity_seq += 1
                                break

                print("----\nStats for read ", read_id, ": ")

                if gc_count > gc_threshold:
                    print("GC frequency: ", gc_count)
                if has_low_complexity_seq > 0:
                    print("Has at least one low complexity sequence")
                print("----")
    print("###\nTACG Stats across all reads:", freq, "\n###")
    sys.stdout = original_stdout
