# coding:utf-8
import pandas as pd
import numpy as np
from gensim import corpora
import csv

def shuffle_detaset(data):
    import random
    print('shuffling...')
    shuffled_data = random.sample(data, len(data))
    return shuffled_data


if __name__ == '__main__':
    authors = ['natsume', 'akutagawa', 'mori', 'dazai']
    author_labels ={'natsume':0, 'akutagawa':1, 'mori':2, 'dazai':3}

    # 辞書の読み込み
    dictionary = corpora.Dictionary.load_from_text('./data/bungo_dict.txt').token2id

    all_data = [] # 全作家の文章を入れる配列
    for author in authors:
        df = pd.read_csv('./data/{}.csv'.format(author))
        for row in df['words']:
            if len(row.split(' ')) != 50:
                continue
            id_row = np.array([], dtype = 'int32')
            for word in row.split(' '):
                id_row = np.append(id_row, dictionary[word])
            # csvの最後の列を正解ラベルとする
            id_row = np.append(id_row, author_labels[author])
            all_data.append(id_row)
            print(id_row)

    # データをランダムに入れ替える
    all_data = shuffle_detaset(all_data)

    with open('./data/all_data.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(all_data)

    # train data
    train_data = all_data[:60000]
    with open('./data/train.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(train_data)

    # test data
    test_data = all_data[60000:70000]
    with open('./data/test.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(test_data)
