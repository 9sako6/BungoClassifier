import pandas as pd
import numpy as np
from gensim import corpora


authors = ['natsume', 'akutagawa', 'mori', 'dazai']
words = []
for author in authors:
    df = pd.read_csv('./data/{}.csv'.format(author))
    for row in df['words']:
        words.append(row.split(' '))


dictionary = corpora.Dictionary(words)
dictionary.save_as_text('./data/bungo_dict.txt')
print(dictionary.token2id)