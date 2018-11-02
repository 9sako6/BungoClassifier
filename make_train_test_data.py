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
    import glob
    from tqdm import tqdm

    TRAIN_DATA_SIZE = 90000
    TEST_DATA_SIZE = 10000
    
    # 作家名を取得
    authors = [r.split('/')[-1] for r in glob.glob('./data/works/*')]

    # 辞書の読み込み
    dictionary = corpora.Dictionary.load_from_text('./data/bungo_dict.txt').token2id

    all_data = [] # 全作家の文章を入れる配列
    for author_label, author in enumerate(authors):
        print('{}...'.format(author))
        # csvファイル読み込み
        df = pd.read_csv('./data/{}.csv'.format(author))
        df.columns = ['words', 'author']
        for row in tqdm(df['words']):
            if len(row.split(' ')) != 50:
                continue
            id_row = np.array([], dtype = 'int32')
            for word in row.split(' '):
                id_row = np.append(id_row, dictionary[word])
            # csvの最後の列を正解ラベルとする
            id_row = np.append(id_row, author_label)
            all_data.append(id_row)

    # データをランダムに入れ替える
    all_data = shuffle_detaset(all_data)

    with open('./data/all_data.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(all_data)

    # train data
    print('saving train.csv...')
    train_data = all_data[:TRAIN_DATA_SIZE]
    with open('./data/train.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(train_data)

    # test data
    print('saving test.csv...')
    test_data = all_data[TRAIN_DATA_SIZE:TRAIN_DATA_SIZE + TEST_DATA_SIZE]
    with open('./data/test.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(test_data)
