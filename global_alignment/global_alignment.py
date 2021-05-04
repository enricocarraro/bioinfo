"""
Assignment : Global alignment
Under the assumption that both input sequences a and b stem from the same origin,
a global alignment tries to identify matching parts and the changes needed to 
transfer one sequence into the other. The changes are scored and an optimal set 
of changes is identified, which defines an alignment. The dynamic programming 
approach tabularizes optimal subsolutions in matrix D, where an entry Di,j 
represents the best score for aligning the prefixes a1..i with b1..j.
To better clarify how global alignment works, take a look here: 
http://rna.informatik.unifreiburg.de/Teaching/index.jsp?toolName=Needleman-Wunsch
Then, write a Python program that given two sequences (passed as first and second
argument from command line) and match, mismatch and gap costs (passed as third, 
fourth, fifth argument from command line):
1. Compute matrix D and output it on the terminal, along with the final alignment
   score
2. Output the final alignment (if two sequences have more than one alignment with
   the same score, provide one of them e.g. check website for ‘AACCG’ and ‘AACG’)
3. Check your alignment on Freiburg website

Usage should be something like this:
python global_alignment.py AACCG AACG 1 -1 -2
Output:
Global alignment score: 2.0 
[[ 0.  -2. -4. -6. -8.]
 [-2.   1. -1. -3. -5.]
 [-4.  -1.  2.  0. -2.]
 [-6.  -3.  0.  3.  1.]
 [-8.  -5. -2.  1.  2.]
 [-10. -7. -4. -1.  2.]]
Final alignment: 
AACCG
||| |
AAC-G
"""

import sys
from typing import Tuple
from typing import List


def get_best_alignments(
    dp_table: List[List[int]], row: int, col: int, first: str, second: str
) -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    if row == 0 and col == 0:
        results.append(("", ""))
        return results

    eq_paths: [Tuple[int, int]] = []
    if (
        row > 0
        and col > 0
        and (
            (
                first[row - 1] == second[col - 1]
                and dp_table[row - 1][col - 1] + match == dp_table[row][col]
            )
            or (
                first[row - 1] != second[col - 1]
                and dp_table[row - 1][col - 1] + mismatch == dp_table[row][col]
            )
        )
    ):
        eq_paths.append((row - 1, col - 1))
    if row > 0 and dp_table[row - 1][col] + gap == dp_table[row][col]:
        eq_paths.append((row - 1, col))
    if col > 0 and dp_table[row][col - 1] + gap == dp_table[row][col]:
        eq_paths.append((row, col - 1))

    for path in eq_paths:
        prefix_tuples = get_best_alignments(dp_table, path[0], path[1], first, second)
        for prefix_tuple in prefix_tuples:
            if path[0] == row - 1 and path[1] == col - 1:
                results.append(
                    (
                        prefix_tuple[0] + first[row - 1],
                        prefix_tuple[1] + second[col - 1],
                    )
                )
            elif path[0] == row - 1:
                results.append(
                    (prefix_tuple[0] + first[row - 1], prefix_tuple[1] + "-")
                )
            elif path[1] == col - 1:
                results.append(
                    (prefix_tuple[0] + "-", prefix_tuple[1] + second[col - 1])
                )

    return results


if len(sys.argv) != 6:
    raise Exception("Program needs 5 parameters.")

_, second_str, first_str, match, mismatch, gap = sys.argv

match, mismatch, gap = int(match), int(mismatch), int(gap)

dp: List[List[int]] = [
    [-sys.maxsize for x in range(len(second_str) + 1)]
    for l in range(len(first_str) + 1)
]

dp[0][0] = 0
for i in range(len(dp)):
    for j in range(len(dp[i])):
        if i > 0 and j > 0:
            dp[i][j] = dp[i - 1][j - 1] + (
                match if first_str[i - 1] == second_str[j - 1] else mismatch
            )
        if i > 0:
            dp[i][j] = max(gap + dp[i - 1][j], dp[i][j])
        if j > 0:
            dp[i][j] = max(gap + dp[i][j - 1], dp[i][j])

for i in range(len(dp)):
    for j in range(len(dp[i])):
        print(dp[i][j], end="\t")

    print("")

print(get_best_alignments(dp, len(dp) - 1, len(dp[0]) - 1, first_str, second_str))
