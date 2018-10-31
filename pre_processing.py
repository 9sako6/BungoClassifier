# coding:utf-8
import subprocess
import re
import regex # 正規表現で漢字を扱うために必要
import MeCab
import numpy as np

def clean_text(text):
    # ルビなどの削除、置換
    text = re.sub('《[^》]*》', '', text)
    text = re.sub('｜', '', text)
    text = re.sub('［[^］]*］', '', text)
    text = re.sub('／＼', '々', text)
    text = re.sub('／″＼', '々', text)
    text = re.sub('々+', '々', text)
    # ヘッダーの削除
    text = re.split('-{55}[\s\S\n]*-{55}', text)[1]
    # フッターの削除
    text = re.split('底本：',text)[0]
    # 章番号の削除
    text = regex.sub('　*[\p{Han}]+\n', '', text)
    # タブ、全角スペースの削除
    text = re.sub('[\t　]', '', text)
    # 単語の正規化
    text = re.sub('\d+', '0', text)
    text = re.sub('○+', '○', text)
    text = re.sub('[\(（]', '（', text)
    text = re.sub('[\)）]', '）', text)
    text = re.sub('[【『]', '「', text)
    text = re.sub('[】』]', '」', text)
    text = re.sub('[…+\n]', '\n', text)
    text = re.sub('[…+]', '…', text)
    text = re.sub('[\?]', '？', text)
    text = re.sub('[\!]', '！', text)
    # その他記号の削除
    text = re.sub('[※＊×—,\.:：/&□△◇☆><;\'〕│┌├└┘┬┤]', '', text)

    return text

def text2csv(text, author, column_size=50):
    words_list = text.split(' ')
    words_size = len(words_list)
    # 1行あたりcolumn_size語になるよう調整
    words_list += [''] * (column_size - words_size%column_size)
    reshaped_list = []
    for i in np.arange(int(words_size / column_size) - 1):
        reshaped_list.append(words_list[i * column_size:(i+1) * column_size])

    # 教師データの作成
    result_text = 'words,author\n'
    for row in reshaped_list:
        result_text += ' '.join(row) + ',{}\n'.format(author)

    return result_text

if __name__ == '__main__':
    import glob
    
    # 作家名を取得
    authors = [r.split('/')[-1] for r in glob.glob('./data/works/*')]
    print(authors)

    #authors = ['natsume', 'akutagawa', 'mori', 'dazai']
    for author in authors:
        # ある作家のディレクトリ内のすべてのテキストファイル
        text_files = glob.glob('./data/works/{}/*.txt'.format(author))
        for text_file in text_files:
            try:
                # 文字コードをutf-8に変換
                cmd = "nkf -w --overwrite {}".format(text_file)
                subprocess.call(cmd, shell=True)
                with open(text_file) as file:
                    text = file.read()
                    # テキスト前処理
                    text = clean_text(text)
                    # 形態素解析
                    tagger = MeCab.Tagger("-Owakati")
                    text = tagger.parse(text)
                    # 改行の削除
                    text = re.sub('\n', '', text)
                    # データセットの作成
                    text = text2csv(text, author)
                    # csvとして保存
                    with open('./data/{}.csv'.format(author), 'a') as savefile:
                        savefile.write(text)
            except (UnicodeDecodeError, IndexError):
                print('Error')
