#!/usr/bin/python

import os
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
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
     
def load_file(filename):
    fdist = collections.OrderedDict();
    infile = open(filename)
    content = infile.readlines();
    for line in content:
        tokens = re.split(', ', line.strip());
        if len(tokens) >= 2:
            word = tokens[0];
            count = int(tokens[1]);
            fdist = fdist_add(fdist, word, count);
    infile.close();
    return fdist;
    
def load_dir(dirname):
    fdist = collections.OrderedDict();
    for dirpath, dirnames, filenames in os.walk(dirname):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            tmp_freq = load_file(fullpath);
            fdist = merge_fdist(fdist, tmp_freq);
    return fdist;

def load_path_list(path_list):
    fdist = collections.OrderedDict();
    for item in path_list:
        if os.path.isdir(item):
            print("Input directory: %s" % item);
            tmp = load_dir(item);
        elif os.path.isfile(item):
            print("Input file: %s" % item);
            tmp = load_file(item);
        else:
            print("Input file or directory not exists: %s" % item);
            tmp = {};
        fdist = merge_fdist(fdist, tmp);
    return fdist;

def get_synset_priority(syn):
    if syn.pos == 'v':
        return 0;
    elif syn.pos == 'a':
        return 1;
    elif syn.pos == 'r':
        return 2;
    elif syn.pos == 'n':
        return 3;
    else:
        return 4;
    
def get_synset_lemma(wnl, word, syn):
    if(syn.pos != 'v'
        and syn.pos != 'a'
        and syn.pos != 'r'
        and syn.pos != 'n'):
        return word;
    lemma = wnl.lemmatize(word, syn.pos);
    if(lemma.lower() == word.lower()):
        lemma = wnl.lemmatize(word.lower(), syn.pos);
        if(lemma.lower() == word.lower()):
            return word;
    cands = syn.lemma_names;
    for cand in cands:
        if(lemma.lower() == cand.lower()):
            return lemma;
    return word;
    
def get_lemma(wnl, word):
    syns = wordnet.synsets(word);
    syns = sorted(syns, key=get_synset_priority);
    for syn in syns:
        lemma = get_synset_lemma(wnl, word, syn);
        if(lemma.lower() != word.lower()):
            return lemma;
    return word;

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
    
def wordlist2lemma(flist):
    fdist = collections.OrderedDict();
    wnl = WordNetLemmatizer();
    total = len(flist);
    lemma_set = set();
    inflections = {};
    milestone = 0;
    done = 0;
    for word in flist:
        lemma = get_lemma(wnl, word[0]);
        if lemma.lower() != word[0].lower():
            lemma_set.add(lemma.lower());
            inflections[word[0].lower()] = lemma;
        done += 1;
        if done*100/total >= milestone:
            milestone += 1;
            print "preprocessing status: %d/%d = %d%%" % (done, total, int(done*100/total));
            
    milestone = 0;
    done = 0;
    for word in flist:
        if word[0].lower() in lemma_set:
            lemmaflist = fdist_add(fdist, word[0].lower(), word[1]);
        elif word[0].lower() in inflections:
            lemmaflist = fdist_add(fdist, inflections[word[0].lower()], word[1]);
        else:
            lemmaflist = fdist_add(fdist, word[0], word[1]);
        done += 1;
        if done*100/total >= milestone:
            milestone += 1;
            print "processing status: %d/%d = %d%%" % (done, total, int(done*100/total));
    
    return fdist;

def test():
    wnl = WordNetLemmatizer();
    print(get_lemma(wnl, 'cutlass'));
    print(get_lemma(wnl, 'cutlas'));
    print(get_lemma(wnl, 'puss'));
    print(get_lemma(wnl, 'pus'));
    print(get_lemma(wnl, 'doss'));
    print(get_lemma(wnl, 'ass'));
    print(get_lemma(wnl, 'as'));
    print(get_lemma(wnl, 'hath'));
    print(get_lemma(wnl, 'saith'));
    print(get_lemma(wnl, 'Worst'));    
    print(get_lemma(wnl, 'dogs'));
    print(get_lemma(wnl, 'thinking'));
    print(get_lemma(wnl, 'further'));
    print(get_lemma(wnl, 'worst'));
    print(get_lemma(wnl, 'was'));
    print(get_lemma(wnl, 'lest'));
    print(get_lemma(wnl, 'balabalabala'));
    print(get_lemma(wnl, 'Weeeeeeeeeeeeeeeeeee'));
    print(get_lemma(wnl, 'iPad'));

def main():    
    parser = argparse.ArgumentParser();
    parser.add_argument("-o", "--output", default="output");
    parser.add_argument("-v", "--verbose", action="store_true");
    parser.add_argument("-t", "--test", action="store_true");
    parser.add_argument("input", nargs='*');
    args = parser.parse_args();
    opts = {};
    if args.test:
        print("Run testing.");
        test();
        return;
    if len(args.input) == 0:
        print("No input files or directories.");
        return;
    print("Output file: %s." % args.output);
    outdir = os.path.dirname(args.output);
    if not os.path.exists(outdir):
        os.makedirs(outdir); 
    lemma_file = args.output;    
    print "loading words from files...";
    freq = load_path_list(args.input);
    flist = unify_fdist(freq);
    print "words to lemmas...";
    lemma_fdist = wordlist2lemma(flist);
    lemma_flist = unify_fdist(lemma_fdist);
    print "write lemmas to file...";
    dump_flist(lemma_file, lemma_flist);
    
main();
