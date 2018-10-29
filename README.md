# BungoClassifier

入力文の文体が、どの文豪の文体に近いか判定します。

![demo](./samples/demo1.gif)

- 対応している文豪
  - 夏目漱石、芥川龍之介、森鴎外、太宰治

# Requirements
## To Predict
- NumPy
- TensorFlow
- Keras
- Gensim
- mecab-python3

If you use the AMD GPU:
- PlaidML

## To Train
- NumPy
- Pandas
- TensorFlow
- Keras
- Gensim
- regex

If you use the AMD GPU:
- PlaidML



# How to Train


## データセットの作成
夏目漱石、芥川龍之介、森鴎外、太宰治の場合を例にして、データセット作成手順を説明します。

### 作品のダウンロード
- [青空文庫 作家別一括ダウンロード](http://keison.sakura.ne.jp/)

上記のサイトから、夏目漱石、芥川龍之介、森鴎外、太宰治の作品をダウンロードし、解凍します。`data`ディレクトリを作成し、解凍したフォルダをそれぞれ`natsume`, `akutagawa`, `mori`, `dazai`という名前で保存します。

### テキストの前処理
ルビ、注釈、ヘッダー、フッターや記号などを削除し、テキストを分かち書きにします。

```
$ python3 pre_processing.py
```

実行すると、`data/natsume.csv`、`data/akutagawa.csv`、`data/mori.csv`、`data/dazai.csv`が作成されます。このCSVファイルは51列あり、はじめの50列には単語が1語ずつ、最後の1列には正解ラベルが書かれています。

### 辞書の作成
各単語に固有のIDを振るための辞書を作ります。

```
$ python3 make_dictionary.py
```

実行すると、`data/bungo_dict.txt`が作成されます。

### 訓練データ＆テストデータの作成

```
$ python3 make_train_test_data.py
```

実行すると、`data/all_data.csv`、`data/train.csv`、`data/test.csv`が作成されます。
これらのCSVファイルは51列あり、はじめの50列の数字は各単語のID、最後の1列の数字は正解ラベルを意味しています。
`data/train.csv`は60,000行、`data/test.csv`は10,000行あります。
`data/train.csv`を用いて訓練、`data/test.csv`を用いて評価を行います。

### モデルの訓練
[`pred_author.ipynb`](https://github.com/9sako6/BungoClassifier/blob/master/pred_author.ipynb)を参考にしてください。モデルの訓練にはGPUが必要です。
ちなみに、筆者は[Google Colab](https://colab.research.google.com/)で訓練を行いました。
無料でGPUを使えるのでとてもよいです（2018/10/29現在）。

- Google Colabを用いるためには、Googleアカウントが必要です。

- Google Colabを用いて訓練を行う場合は、`data/train.csv`、`data/test.csv`、`data/bungo_dict.txt`をGoogle Colab上にアップロードする必要があります。


訓練が完了すると、`pre_trained_model.h5`が作成されます。これを`data`ディレクトリ内に保存します。このファイルは学習済みのモデルの重みを記録したものです。実行時にはこの重みを使い、推論を行います。

### ディレクトリ構造
最終的に、以下のような構造になります。

```
.
├── README.md
├── data
│   ├── bungo_dict.txt
│   ├── pre_trained_model.h5
│   ├── natsume.csv
│   ├── akutagawa.csv
│   ├── mori.csv
│   ├── dazai.csv
│   ├── all_data.csv
│   ├── test.csv
│   └── train.csv
├── main.py
├── make_dictionary.py
├── make_train_test_data.py
├── pre_processing.py
├── pred_author.ipynb
└── samples
    └── demo1.gif
```

# How to Predict

`data`ディレクトリに`pre_trained_mode.h5`、`bungo_dict.txt`があることを確認してください。

`main.py`を実行すれば冒頭のデモのように推論を行う事ができます。

```
$ python3 main.py
```

もしAMDのGPUを使っている場合は、`main.py`の先頭に以下の2行を加えてください。

```
import plaidml.keras            # for PlaidML (AMDのGPUを使用している場合に必要)
plaidml.keras.install_backend() # for PlaidML (AMDのGPUを使用している場合に必要)
```


# 参考
- [LSTMを使ってテキストの多クラス分類をする](https://blog.codingecho.com/2018/03/25/lstm%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%81%AE%E5%A4%9A%E3%82%AF%E3%83%A9%E3%82%B9%E5%88%86%E9%A1%9E%E3%82%92%E3%81%99%E3%82%8B/)

- [PythonとKerasによるディープラーニング. Francois Chollet (著), 巣籠悠輔（翻訳）, 株式会社クイープ（翻訳）. マイナビ出版 (2018/5/28). pp.78-86 ](https://www.amazon.co.jp/Python%E3%81%A8Keras%E3%81%AB%E3%82%88%E3%82%8B%E3%83%87%E3%82%A3%E3%83%BC%E3%83%97%E3%83%A9%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0-Francois-Chollet-ebook/dp/B07D498RJK)
