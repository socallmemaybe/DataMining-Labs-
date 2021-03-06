from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from sys import argv
import re
from math import log
from itertools import chain
from pprint import pprint
from matplotlib import pyplot as plt


def count_words_data(words):
    counted_words = {}
    for w in words:
        if w not in counted_words:
            counted_words[w] = 0
        counted_words[w] += 1
    return counted_words


def split_to_docs(words):
    return (words[i:i + 2000] for i in range(0, len(words), 2000))


def is_stop_word(word):
    stop_words = set((
        'the', 'and', 'or', 'of', 'to', 'a', 'was', 'were', 'them', 'their',
        'they', 'all', 'are', 'yes', 'that', 'there', 'this', 'but', 'came',
        'for', 'has', 'had', 'some', 'where', 'when', 'your', 'you', 'been',
        'was', 'were', 'over', 'will', 'shall', 'which', 'with', 'his', 'him',
        'here', 'it', 'not', 'what', 'where', 'who', 'also'
    ))
    return len(word) < 3 or word in stop_words


def normalize_word(word):
    w = word.strip()
    return w[:int(len(w) * 0.8)] if len(w) > 4 else w


def normailized_text(remove_stop_words=True):
    orig_text, text = [], []
    with open(argv[1], 'r') as inp:
        for line in inp:
            words = re.sub('[^a-zA-Z]+', ' ', line).lower().strip().split()
            orig_text.extend([
                w.strip()
                for w in words
                if not is_stop_word(w) or not remove_stop_words
            ])
            text.extend([
                normalize_word(w)
                for w in words
                if not is_stop_word(w) or not remove_stop_words
            ])
    return orig_text, text


def tf(doc):
    tf = {}
    for term in doc:
        tf[term] = tf.get(term, 0) + 1
    tf = {k: v / len(doc) for k, v in tf.iteritems()}

    return tf


def idf(docs, terms):
    idf = {}
    for term in terms:
        idf[term] = len(docs) / sum(1 for doc in docs if term in doc)
        # print(term, idf[term])
    idf = {k: log(v) for k, v in idf.iteritems()}
    return idf


def merge(d1, d2):
    d = {}
    for k in d1:
        d[k] = max(d1[k], d2.get(k, 0.0))
    for k in d2:
        d[k] = max(d1.get(k, 0), d2[k])
    return d


def tfidf(words):
    docs = list(split_to_docs(words))
    words = set(words)
    # docs_tf = dict(chain(*[sorted(tf(doc).items(), key=lambda x: x[1], reverse=True)[:10] for doc in docs]))
    docs_tf = [
        sorted(
            tf(doc).items(), key=lambda x: x[1], reverse=True)[:10]
        for doc in docs
    ]
    # pprint(docs_tf)
    docs_tf_merged = {}
    for dtf in docs_tf:
        docs_tf_merged = merge(docs_tf_merged, dict(dtf))
    docs_tf = docs_tf_merged
    # pprint(docs_tf)
    terms_idf = idf(docs, docs_tf.keys())
    tfidf = {}
    for term, term_tf in docs_tf.iteritems():
        tfidf[term] = term_tf * terms_idf[term]
    return tfidf


orig_text, text = normailized_text(remove_stop_words=True)
print('Total {} words'.format(len(orig_text)))
res = sorted(tfidf(text).items(), key=lambda x: x[1], reverse=True)
for word, v in res:
    w = '{}[{}]'.format(orig_text[text.index(word)], word)
    print('{:>20}: {:<20}'.format(w, v))
# sorted(tfidf(text).items(), key=lambda x: x[1], reverse=True)
