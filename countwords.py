#!/usr/bin/python

import os
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
import argparse

def fdist_add(fdist, word, count):
    key = word.lower();
    if fdist.has_key(key):
        fdist[key]['sum'] += count;
    else:
        fdist[key] = {};
        fdist[key]['sum'] = count;
        fdist[key]['items'] = {};
    if(fdist[key]['items'].has_key(word)):
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
    fdist = {};
    if 'unescape' in options and options['unescape']:
        text = text.replace("\\r", " ");
        text = text.replace("\\n", " ");
        text = text.replace("\\t", " ");
    wordlist = re.findall(r"[A-Za-z]+", text);
    for word in wordlist:
        fdist = fdist_add(fdist, word, 1);
    return fdist

def count_file(filename, options):
    fdist = {};
    infile = open(filename)
    all_text = infile.read()
    fdist = count_text(all_text, options);
    infile.close()
    return fdist;
    
def count_dir(dirname, options):
    fdist = {};
    for dirpath, dirnames, filenames in os.walk(dirname):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            tmp_freq = count_file(fullpath, options);
            fdist = merge_fdist(fdist, tmp_freq);
    return fdist;

def count_path_list(path_list, options):
    fdist = {};
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
    
def get_synset_lemma(word, syn):
    wnl = WordNetLemmatizer();
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
    
def get_lemma(word):
    syns = wordnet.synsets(word);
    syns = sorted(syns, key=get_synset_priority);
    for syn in syns:
        lemma = get_synset_lemma(word, syn);
        if(lemma.lower() != word.lower()):
            return lemma;
    return word;

def dump_flist(filename, flist):
    fo = open(filename, "w")
    for item in flist:
        fo.write("%s, %s\n" % (item[0], item[1]));
    fo.close()
    
def unify_fdist(fdist):
    unifed = {};
    for (k, v) in fdist.items():
        if (len(v['items'])) == 1:
            for word in v['items']:
                unifed[word] = v['sum'];
        else:
            unifed[k] = v['sum'];
    return sorted(unifed.items(), key=lambda x: x[1], reverse=True);      
    
def wordlist2lemma(flist):
    fdist = {};
    for word in flist:
        lemma = get_lemma(word[0]);
        if lemma.lower() == word[0].lower():
            lemmaflist = fdist_add(fdist, word[0], word[1]);
        else:
            lemmaflist = fdist_add(fdist, lemma, word[1]);
    return fdist;

def test():
    print(get_lemma('Worst'));    
    print(get_lemma('dogs'));
    print(get_lemma('thinking'));
    print(get_lemma('further'));
    print(get_lemma('worst'));
    print(get_lemma('was'));
    print(get_lemma('lest'));
    print(get_lemma('balabalabala'));
    print(get_lemma('Weeeeeeeeeeeeeeeeeee'));
    print(get_lemma('iPad'));
    a = count_text("Test you, test me, and test others.", {});
    b = count_text("you're right! I'm not right!", {});
    c = count_text("I did\tnot\\tfinish\\nI do\\tfinish.", {'unescape': True});
    print(unify_fdist(a));
    print(unify_fdist(b));
    print(unify_fdist(merge_fdist(a, b)));
    print(c);
    print(unify_fdist(c));
    print(unify_fdist(wordlist2lemma(unify_fdist(c))));

def main():    
    parser = argparse.ArgumentParser();
    parser.add_argument("-o", "--output", default="output");
    parser.add_argument("-p", "--prefix", default="");
    parser.add_argument("-v", "--verbose", action="store_true");
    parser.add_argument("-t", "--test", action="store_true");
    parser.add_argument("-e", "--unescape", action="store_true");
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
    print("Output directory: %s." % args.output);
    if not os.path.exists(args.output):
        os.makedirs(args.output);        
    word_file = args.output + "/" + args.prefix + "words.txt";
    lemma_file = args.output + "/" + args.prefix + "lemmas.txt";
    flist = unify_fdist(freq);
    dump_flist(word_file, flist);
    lemma_fdist = wordlist2lemma(flist);
    lemma_flist = unify_fdist(lemma_fdist);
    dump_flist(lemma_file, lemma_flist);
    
main();
