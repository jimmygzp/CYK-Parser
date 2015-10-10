#!/usr/bin/python

import sys
import pcfg



freq = pcfg.Freq(open(sys.argv[1]))
tree = pcfg.ParseTree(sys.argv[2], freq)
tree.clean()



