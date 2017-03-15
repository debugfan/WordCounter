#!/bin/sh

./strip.py "2554/download/Texts" "bnc"

./countwords.py -o output/bnc/words.txt bnc
./lemmatize.py -o output/bnc/lemmas.txt output/bnc/words.txt
