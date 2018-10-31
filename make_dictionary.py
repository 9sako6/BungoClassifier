import pandas as pd
import numpy as np
from gensim import corpora
import glob

# 作家名を取得
authors = [r.split('/')[-1] for r in glob.glob('./data/works/*')]

words = []
for author in authors:
    df = pd.read_csv('./data/{}.csv'.format(author))
    for row in df['words']:
        words.append(row.split(' '))

# wordsは行列
dictionary = corpora.Dictionary(words)
dictionary.save_as_text('./data/bungo_dict.txt')
print(dictionary.token2id)