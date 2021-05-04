"""
Assignment: Local alignment
A local alignment approach tries to identify the most similar subsequences that maximize the scoring
of their matching parts and the changes needed to transfer one subsequence into the other.

The dynamic programming approach tabularizes optimal subsolutions in matrix S, where an entry Si,j
represents the maximal similarity score for any local alignment of the (sub)prefixes ax..i with by..j,
where x,y>0 are so far unknown and have to be identified via traceback.

To better clarify how local alignment works, take a look here:
http://rna.informatik.uni-freiburg.de/Teaching/index.jsp?toolName=Smith-Waterman

Then, write a Python program that given two sequences (passed as first and second argument from
command line) and match, mismatch and gap cost (passed as third, fourth, fifth argument from command
line).
1. Compute matrix D and output it on the terminal, along with the final alignment score (remember
   that the minimum value you can have in the matrix is 0!!)
2. Output the final alignment (if two sequences have more than one alignment with the same score,
   provide one of them)
3. Check your alignment on Freiburg website
4. Local alignment has a lot of concepts similar to global alignment, so you can reuse a lot of code
   you have previously written for global alignment!

Usage should be something like this:
python local_alignment.py AATCG AACG 1 -1 -2
Output:
Local alignment score: 2.0
[[0. 0. 0. 0. 0.]
 [0. 1. 1. 0. 0.]
 [0. 1. 2. 0. 0.]
 [0. 0. 0. 1. 0.]
 [0. 0. 0. 1. 0.]
 [0. 0. 0. 0. 2.]]
  Final alignment:
  AA
  ||
  AA
"""
import sys
from typing import Tuple
from typing import List


def print_dp(
    dp_table: List[List[int]], row: int, col: int, first: str, second: str
) -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    if dp_table[row][col] == 0:
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
        prefix_tuples = print_dp(dp_table, path[0], path[1], first, second)
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
    [0 for x in range(len(second_str) + 1)] for l in range(len(first_str) + 1)
]

dp[0][0] = 0
for i in range(len(dp)):
    for j in range(len(dp[i])):
        if i > 0 and j > 0:
            dp[i][j] = max(
                dp[i - 1][j - 1]
                + (match if first_str[i - 1] == second_str[j - 1] else mismatch),
                dp[i][j],
            )
        if i > 0:
            dp[i][j] = max(gap + dp[i - 1][j], dp[i][j])
        if j > 0:
            dp[i][j] = max(gap + dp[i][j - 1], dp[i][j])


max_score = 0
max_score_cells = []
for i in range(len(dp)):
    for j in range(len(dp[i])):
        print(dp[i][j], end="\t")
        if dp[i][j] > max_score:
            max_score = dp[i][j]
            max_score_cells.clear()
        if dp[i][j] == max_score:
            max_score_cells.append((i, j))
    print("")

print("Local alignment score:", max_score)
print("Final alignments:")
for max_score_cell in max_score_cells:
    print(print_dp(dp, max_score_cell[0], max_score_cell[1], first_str, second_str))
