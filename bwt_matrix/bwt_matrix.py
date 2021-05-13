"""
Assignment: BWT transform

Given a string T from the command-line, compute the BWM(T) (matrix) and output the BWT(T).

Optional 1: implement the algorithm to reconstruct T from BWT(T).
Optional 2: implement the algorithm to build the prefix tree of T. Given a substring G, write the algorithm to align G on T.

"""
import functools
import sys


def get_rotation_view(view: memoryview, rotation: int) -> bytes:
    return bytes(view[-rotation:])


def compare_rotation(l, r):
    lb = get_rotation_view(T_view, l)
    rb = get_rotation_view(T_view, r)
    if lb < rb:
        return -1
    if lb == rb:
        return 0
    else:
        return 1



if len(sys.argv) != 2:
    raise Exception("Program needs 1 options.")

_, T = sys.argv


T += "$"
T = T.encode("utf-8")
T_view = memoryview(T)

rotations = list(range(len(T)))
# Example: T = "ATCGGG$"
#   rotation = 1 -> $ is at position 1 (e.g. "G$...")
#   rotation = 0 -> $ is at position 0 (e.g. "$A...")
rotations.sort(key=functools.cmp_to_key(compare_rotation))


print("Matrix:")
for rotation in rotations:
    print((get_rotation_view(T_view, rotation) + bytes(T_view[0:-rotation])).decode())

BWT = bytearray(b"")
for rotation in rotations:
    if len(T_view[0:-rotation]) > 0:
        BWT.append(T_view[0:-rotation][-1])
    else:
        BWT.append(ord("$"))


print("BWT(T): ", BWT.decode())


