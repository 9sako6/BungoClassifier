import plaidml.keras            # for PlaidML (AMDのGPUを使用している場合に必要)
plaidml.keras.install_backend() # for PlaidML (AMDのGPUを使用している場合に必要)
from keras.models import Sequential
from keras.layers import Flatten, Dense, Embedding
from keras.layers import LSTM
import numpy as np
import MeCab
from gensim import corpora

def text2vec(text, dictionary):
    tagger = MeCab.Tagger("-Owakati")
    text = tagger.parse(text)
    words_list = text.split(' ')
    # 単語列をID列に変換する
    id_list = np.full(50, 88888) # 未知語のIDは88888とする
    for i, word in enumerate(words_list):
        if i >= 50:
            break

        if dictionary.get(word) != None:
            id_list[i] = dictionary[word]
        else:
            continue

    return np.array([id_list])

def vec2text(vec, dictionary):
    words_list = []
    for id in vec:
        word = [k for k, v in dictionary.items() if v == id][0]
        words_list.append(word)

    return ''.join(words_list)

if __name__ == '__main__':
    authors = ['夏目漱石', '芥川龍之介', '森鴎外', '太宰治']
    # 学習済みモデルの読み込み
    model = Sequential()
    model.add(Embedding(90000, 300, input_length=50))
    model.add(LSTM(32))
    model.add(Dense(4, activation='softmax'))
    model.load_weights('./data/pre_trained_model.h5')
    # 辞書の読み込み
    dictionary = corpora.Dictionary.load_from_text('./data/bungo_dict.txt').token2id

    text = input('判定する文章：')
    predictions = model.predict(text2vec(text, dictionary))
    #vec = [1,639,1297,51,13397,47,10,0,693,30,1110,1598,15,334,10,109,2044,9,1,4292,17,0,4092,1094,25908,13,4349,2606,4240,10,3664,8,97,17,91,8,6,0,16932,3545,16,1616,15,0,25908,15,39494,211,10,0]
    #doc = vec2text(vec, dictionary)
    #print(doc)
    # 結果表示
    for i, author in enumerate(authors):
        print('{}度:'.format(author), predictions[0][i])
