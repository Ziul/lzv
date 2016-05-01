# -*- coding: utf-8 -*-

"""
Lempel-Ziv algorithm.

Used to encode/decode files, as
create table from a file.
"""

import json
import struct
from heapq import heappush, heappop, heapify
from collections import defaultdict
from lzargs import _parser
from writebits import Bitset
from bitarray import bitarray
from time import sleep
from random import choice
from sys import stdout

(_options, _args) = _parser.parse_args()


class LempelZiv(object):
    """docstring for LempelZiv"""

    def __init__(self, filename, verbose=True, table=[]):
        super(LempelZiv, self).__init__()
        self.filename = filename
        self.verbose = verbose
        self.bitarray = Bitset()
        self.bitarray.verbose = self.verbose
        self.table = table

        if self.filename:
            with open(self.filename, 'rb') as file:
                self.bitarray.fromfile(file)
                self.bitarray = self.bitarray.to01()
        else:
            self.bitarray = _options.text

    def encode(self):
        position = 0
        offset = 1
        output = ''
        self.table = list(set(self.bitarray))
        self.table.sort()
        while position + offset <= len(self.bitarray):
            buff = self.bitarray[position:position + offset]
            if not buff in self.table:
                self.table.append(buff)
                output += str(self.table.index(
                    self.bitarray[position:position + offset - 1]))
                position += offset - 1
                offset = 1
            else:
                offset += 1
        output += str(self.table.index(
            self.bitarray[position:position + offset]))
        print(self.table)
        return output

    def decode(self):
        pass

    def __str__(self):
        return self.bitarray


def main():
    if (not _options.filename) and (not _options.text):
        if _args:
            _options.filename = _args[0]
        else:
            _parser.print_help()
            return

    lzv = LempelZiv(_options.filename)
    if _options.encode:
        print(lzv.encode())
    else:
        lzv.decode()

    print(lzv)

if __name__ == '__main__':
    main()
