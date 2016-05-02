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
        self.bitarray.name = self.filename + '.lzv'
        self.table = table

        if self.filename:
            with open(self.filename, 'rb') as file:
                self.bitarray.fromfile(file)
                self.data = self.bitarray.to01()
        else:
            self.data = _options.text

    def encode(self):
        position = 0
        offset = 1
        output = ''
        self.table = list(set(self.data))
        self.table.sort()
        while position + offset <= len(self.data):
            print('\r{:0.2f}  '.format(
                100 * (position + offset) / len(self.data)), end='')
            buff = self.data[position:position + offset]
            if not buff in self.table:
                self.table.append(buff)
                output += str(self.table.index(
                    self.data[position:position + offset - 1]))
                position += offset - 1
                offset = 1
            else:
                offset += 1
        output += str(self.table.index(
            self.data[position:position + offset]))
        print(self.table)

        with open(self.filename + '.table', "w") as f:
            json.dump(self.table, f)

        self.bitarray.push(output)
        self.bitarray.to_file()
        self.data = output

        return output

    def decode(self):
        table_file = self.filename.split('.')[:-1]
        table_file = '.'.join(table_file) + '.table'

        with open(table_file) as json_file:
            self.dict_table = json.load(json_file)

        with open(table_file.replace('.table', '.lzv'), 'rb') as file:
            self.bitarray.fromfile(file)
            self.bitarray = self.bitarray.to01()

    def __str__(self):
        return self.data


def main():
    if (not _options.filename) and (not _options.text):
        if _args:
            _options.filename = _args[0]
        else:
            _parser.print_help()
            return

    lzv = LempelZiv(_options.filename)
    if _options.encode:
        lzv.encode()
    else:
        lzv.decode()

    print(lzv)

if __name__ == '__main__':
    main()
