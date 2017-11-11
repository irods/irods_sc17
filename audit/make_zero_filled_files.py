#!/usr/bin/env python
import sys
import os
import math
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('directory', help='path of directory to create')
parser.add_argument('dirsize', help='how many files', type=int, default=1, nargs='?')
parser.add_argument('filesize', help='file size in KB', type=int, default=1, nargs='?')


args = parser.parse_args()

# sanity checks
if args.dirsize < 1:
    parser.error('dirsize must be 1 or greater')

if args.filesize > 1073741824:
    parser.error('filesize over 1TB')


def digits(n):
    '''
    Returns the number of digits in a positive integer
    '''
    if n == 0:
        return 1

    # fast solution before rounding errors kick in
    # https://stackoverflow.com/questions/2189800/length-of-an-integer-in-python
    if n <= 999999999999997:
        return int(math.log10(n)) + 1

    return len(str(n))


# make test directory
os.makedirs(args.directory)


# make zero filled files in directory
for i in range(1, args.dirsize + 1):
    # pad file name suffix with zeroes
    suffix_len = digits(args.dirsize)
    file_name = 'test_{i:0>{suffix_len}}.txt'.format(**locals())
    file_path = os.path.join(args.directory, file_name)

    with open(file_path, 'wb') as binfile:
        binfile.write(b'\x00' * args.filesize * 1024)

sys.exit(0)

