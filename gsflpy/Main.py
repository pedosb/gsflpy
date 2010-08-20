#! /usr/bin/env python
import sys
from ReadLattice import ReadLattice

if __name__ == "__main__":
    read = ReadLattice()
    lattice = read.parse(sys.argv[1])
    lattice.search_sentences()
