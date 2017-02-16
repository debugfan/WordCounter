#!/usr/bin/python

import os
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re

def merge_freq(freq1, freq2):
    for (key, value) in freq2.items():
        freq1[key] += value;
    return freq1;

def dump_freq(filename, freq):
    fo = open(filename, "w")
    for (key, value) in freq.items():
        fo.write("%s, %s\n" % (key, value));
    fo.close()
 
def count_text(text):
    fdist = FreqDist();
    wordlist = re.findall(r"[']?[A-Za-z]+", text);
    for word in wordlist:
        fdist[word.lower()] += 1
    return fdist

def count_file(filename):
    fdist = FreqDist();
    infile = open(filename)
    all_text = infile.read()
    fdist = count_text(all_text);
    infile.close()
    return fdist;
    
def count_dir(dirname):
    fdist = FreqDist();
    for dirpath, dirnames, filenames in os.walk(dirname):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            tmp_freq = count_file(fullpath);
            fdist = merge_freq(fdist, tmp_freq);
    return fdist;

def get_lemma(word):
    wnl = WordNetLemmatizer();
    lemma = wnl.lemmatize(word, 'v');
    if(lemma != word):
        return lemma;
    lemma = wnl.lemmatize(word, 'a');
    if(lemma != word):
        return lemma;
    lemma = wnl.lemmatize(word, 'r');
    if(lemma != word):
        return lemma;
    lemma = wnl.lemmatize(word);
    if(lemma != word):
        return lemma;        
    return lemma;

def wordfreq2lemma(freq):
    lemmafreq = FreqDist();
    for (key, value) in freq.items():
        lemma = get_lemma(key);
        lemmafreq[lemma] += value;
    return lemmafreq;

def test():    
    print(get_lemma('dogs'));
    print(get_lemma('thinking'));
    print(get_lemma('further'));
    print(get_lemma('worse'));
    a = count_text("test you. test me. test others.");
    b = count_text("you're right! I'm OK!");
    print(a);
    print(b);
    print(merge_freq(a, b));
    
test();    
freq = count_dir("bible");
dump_freq("output/words.txt", freq);
lemfreq = wordfreq2lemma(freq);
dump_freq("output/lemmas.txt", lemfreq);
