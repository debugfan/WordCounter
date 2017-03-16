#!/usr/bin/python

import os
import sys
import re

def load_file(filename):
    album = set();
    infile = open(filename)
    content = infile.readlines();
    for line in content:
        tokens = re.split(', ', line.strip());
        if len(tokens) >= 1:
            album.add(tokens[0]);
    infile.close();
    return album;
    
def subtract(minuend_file, subtrahend_file):
    diff = [];
    minuend_list = load_file(minuend_file);
    subtrahend_list = load_file(subtrahend_file);
    for item in minuend_list:
        if item not in subtrahend_list:
            diff.append(item);
    return diff;
        
def dump_list(album):
    for item in album:
        print "%s" % item;
            
def main():
    if len(sys.argv) < 3:
        return;
    minuend_file = sys.argv[1];
    print "minuend file: %s" % minuend_file;
    subtrahend_file = sys.argv[2];
    print "subtrahend file: %s" % subtrahend_file;
    diff = subtract(minuend_file, subtrahend_file);
    print "total diff: %d" % len(diff);
    dump_list(diff);

main();
