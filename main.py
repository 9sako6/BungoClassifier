# coding:utf-8
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
    WORD_SIZE = len(dictionary) + 2
    # 単語列をID列に変換する
    id_list = np.full(50, WORD_SIZE - 1) # 空文字のIDはWORD_SIZE - 1とする
    for i, word in enumerate(words_list):
        if i >= 50:
            break

        if dictionary.get(word) != None:
            id_list[i] = dictionary[word]
        else:
            id_list[i] = WORD_SIZE # 未知語のIDはWORD_SIZEとする

    return np.array([id_list])

def vec2text(vec, dictionary):
    words_list = []
    for id in vec:
        word = [k for k, v in dictionary.items() if v == id][0]
        words_list.append(word)

    return ''.join(words_list)

if __name__ == '__main__':
    import glob
    
    # 作家名を取得
    authors = ['森鴎外', '小川未明', '岡本かの子', '与謝野晶子', '夏目漱石', '折口信夫', '太宰治', '泉鏡花', '芥川龍之介']
    AUTHOR_NUM = len(authors)
    # 辞書の読み込み
    dictionary = corpora.Dictionary.load_from_text('./data/bungo_dict.txt').token2id
    WORD_SIZE = len(dictionary) + 2
    # 学習済みモデルの読み込み
    model = Sequential()
    model.add(Embedding(WORD_SIZE, 512, input_length=50))
    model.add(LSTM(32))
    model.add(Dense(len(authors), activation='softmax'))
    model.load_weights('./data/pre_trained_model.h5')


    text = input('判定する文章：')
    predictions = model.predict(text2vec(text, dictionary))
    # 結果表示
    for i, author in enumerate(authors):
        print('{}度:\t'.format(author), round(predictions[0][i], 3))
