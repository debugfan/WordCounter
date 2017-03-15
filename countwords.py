#!/usr/bin/python

import os
import string
import re
import argparse
import collections

def fdist_add(fdist, word, count):
    key = word.lower();
    if key in fdist:
        fdist[key]['sum'] += count;
    else:
        fdist[key] = {};
        fdist[key]['sum'] = count;
        fdist[key]['items'] = {};
    if word in fdist[key]['items']:
        fdist[key]['items'][word] += count;
    else:
        fdist[key]['items'][word] = count;
    return fdist;

def merge_fdist(fdist1, fdist2):
    merged = fdist1;
    for (key, value) in fdist2.items():
        words = value['items'];
        for (word, count) in words.items():
            merged = fdist_add(merged, word, count);
    return merged;
 
def count_text(text, options):
    fdist = collections.OrderedDict();
    if 'unescape' in options and options['unescape']:
        text = text.replace("\\r", " ");
        text = text.replace("\\n", " ");
        text = text.replace("\\t", " ");
    wordlist = re.findall(r"[A-Za-z]+", text);
    for word in wordlist:
        fdist = fdist_add(fdist, word, 1);
    return fdist

def count_file(filename, options):
    infile = open(filename)
    all_text = infile.read()
    fdist = count_text(all_text, options);
    infile.close()
    return fdist;
    
def count_dir(dirname, options):
    fdist = collections.OrderedDict();
    for dirpath, dirnames, filenames in os.walk(dirname):
        for file in filenames:
            fullpath = os.path.join(dirpath, file);
            print("Count words of file: %s" % fullpath);
            tmp_freq = count_file(fullpath, options);
            fdist = merge_fdist(fdist, tmp_freq);
    return fdist;

def count_path_list(path_list, options):
    fdist = collections.OrderedDict();
    for item in path_list:
        if os.path.isdir(item):
            print("Input directory: %s" % item);
            tmp = count_dir(item, options);
        elif os.path.isfile(item):
            print("Input file: %s" % item);
            tmp = count_file(item, options);
        else:
            print("Input file or directory not exists: %s" % item);
            tmp = {};
        fdist = merge_fdist(fdist, tmp);
    return fdist;
    
def dump_flist(filename, flist):
    fo = open(filename, "w")
    for item in flist:
        fo.write("%s, %s\n" % (item[0], item[1]));
    fo.close()
    
def unify_fdist(fdist):
    unifed = collections.OrderedDict();
    for (k, v) in fdist.items():
        basic_form = k.upper();
        for word in v['items']:
            basic_form = max(basic_form, word);
        unifed[basic_form] = v['sum'];
    return sorted(unifed.items(), key=lambda x: x[1], reverse=True);      

def test():
    a = count_text("Test you, test me, and test others.", {});
    b = count_text("you're right! I'm not right!", {});
    c = count_text("I did\tnot\\tfinish\\nI do\\tfinish.", {'unescape': True});
    print(unify_fdist(a));
    print(unify_fdist(b));
    print(unify_fdist(merge_fdist(a, b)));
    print(c);
    print(unify_fdist(c));
    
def main():    
    parser = argparse.ArgumentParser();
    parser.add_argument("-o", "--output", default="output");
    parser.add_argument("-v", "--verbose", action="store_true");
    parser.add_argument("-e", "--unescape", action="store_true");
    parser.add_argument("-t", "--test", action="store_true");
    parser.add_argument("input", nargs='*');
    args = parser.parse_args();
    opts = {};
    if args.unescape:
        opts['unescape'] = True;
    else:
        opts['unescape'] = False;
    if args.test:
        print("Run testing.");
        test();
        return;
    if len(args.input) == 0:
        print("No input files or directories.");
        return;
    print("Unescape option: %s" % opts['unescape']);
    freq = count_path_list(args.input, opts);
    print("Output file: %s." % args.output);
    outdir = os.path.dirname(args.output);
    if not os.path.exists(outdir):
        os.makedirs(outdir); 
    flist = unify_fdist(freq);
    dump_flist(args.output, flist);
    
main();
