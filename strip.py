#!/usr/bin/python

import os
import sys

def handle_file(filename, outname):
    outname += ".txt";
    if not os.path.exists(outname):
        print "%s -> %s" % (filename, outname);
        os.system("xsltproc 2554/download/XML/Scripts/justTheWords.xsl %s > %s" % (filename, outname));
    
def traverse_dir(dirname, outdir):
    (dirpath, dirnames, filenames) = next(os.walk(dirname));
    for file in filenames:
        handle_file(dirname + "/" + file, outdir + "/" + file);
    for dir in dirnames:
        newdir = outdir + "/" + dir;
        if not os.path.exists(newdir):
            os.makedirs(newdir);
        traverse_dir(dirname + "/" + dir, newdir);
            
def main():
    if len(sys.argv) < 3:
        return;
    input = sys.argv[1];
    print "input directory: %s" % input;
    output = sys.argv[2];
    print "out directory: %s" % output;
    if not os.path.exists(output):
        os.makedirs(output);
    traverse_dir(input, output);

main();
