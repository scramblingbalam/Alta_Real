# -*- coding: utf-8 -*-
"""

Created on Thu Mar 02 17:07:02 2017

@author: Colin Drayton
"""
import sys
import nltk
import unicodedata as uniD
import re
# This modul uses python 3.5
# a function that turns tweets into one line tokenized strings
# I wrote this for Doc2vec training but could be useful besides
# the goal is that after y

def compiler(UNI_CATs=['So','Po','Pi'],URL=True,ATs=True,HASHs=True):
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    words = '\w+'
    at_tags = '@\w+'
    hash_tags = '#\w+' 
    words_plus ='[^\w\s]+'

    expr = []
    if URL:
        expr.append(url_regex)
    expr.append(words)
    if ATs:
        expr.append(at_tags)
    if HASHs:
        expr.append(hash_tags)
    if UNI_CATs:
        uni_cats = UNI_CATs
        uni_cats_chars = [c for c in map(chr, range(sys.maxunicode + 1)) if uniD.category(c) in uni_cats]
        uni_cats_expr = '[\\' + '\\'.join(uni_cats_chars)+"]"
        expr.append(uni_cats_expr)
    expr.append(words_plus)
    return re.compile("|".join(expr))

def ize(string,regex=compiler()):
    tokenizer = nltk.RegexpTokenizer(regex)
    return tokenizer.tokenize(string)

