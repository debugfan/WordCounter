#!/usr/bin/python

import os
import sys

def arrange(inname, outname):
    infile = open(inname)
    content = infile.readlines();
    infile.close();
    if len(content) > 0:
        content.sort();
        outfile = open(outname, "w")
        outfile.writelines(content);
        outfile.close()

def main():
    if len(sys.argv) < 3:
        return;
    input = sys.argv[1];
    print "input file: %s" % input;
    output = sys.argv[2];
    print "output file: %s" % output;
    arrange(input, output);

main();
