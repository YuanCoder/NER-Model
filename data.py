import sys, pickle, os, random
import numpy as np

## tags, BIO
# tag2label = {"O": 0,
#              "B-PER": 1, "I-PER": 2,
#              "B-LOC": 3, "I-LOC": 4,
#              "B-ORG": 5, "I-ORG": 6
#              }

tag2label = {"O": 0,
             "B-Acc": 1, "M-Acc": 2,"E-Acc": 3
             }


def read_corpus(corpus_path):
    """
    read corpus and return the list of samples
    :param corpus_path:
    :return: data
    """
    data = []
    with open(corpus_path, encoding='utf-8') as fr:
        lines = fr.readlines()
    sent_, tag_ = [], []
    index=0;
    for line in lines:
        index = index + 1;
        if line != '\n':
            line = line.lstrip()
            # print("line={},行数={},长度={}".format(line ,index ,line.__len__()))
            if line.__len__() == 6 or line.__len__() == 2 : continue
            [char, label] = line.strip().split()
            sent_.append(char)
            tag_.append(label)
        else:
            data.append((sent_, tag_))
            sent_, tag_ = [], []

    return data


def vocab_build(vocab_path, corpus_path, min_count):
    """
    生成 pkl
    :param vocab_path:  pkl 保存地址
    :param corpus_path: 语料地址
    :param min_count:
    :return:
    """
    data = read_corpus(corpus_path)
    word2id = {}
    for sent_, tag_ in data:
        for word in sent_:
            if word.isdigit():
                word = '<NUM>'
            elif ('\u0041' <= word <='\u005a') or ('\u0061' <= word <='\u007a'):
                word = '<ENG>'
            if word not in word2id:
                word2id[word] = [len(word2id)+1, 1]
            else:
                word2id[word][1] += 1
    low_freq_words = []
    for word, [word_id, word_freq] in word2id.items():
        if word_freq < min_count and word != '<NUM>' and word != '<ENG>':
            low_freq_words.append(word)
    for word in low_freq_words:
        del word2id[word]

    new_id = 1
    for word in word2id.keys():
        word2id[word] = new_id
        new_id += 1
    word2id['<UNK>'] = new_id
    word2id['<PAD>'] = 0

    print(len(word2id))
    with open(vocab_path, 'wb') as fw:
        pickle.dump(word2id, fw)

# 将输入文本转换成字符index
def sentence2id(sent, word2id):
    """
    用字的Index来表示sentence
    :param sent: 句子
    :param word2id: 词典
    :return: 返回 字或词对应的 id数字
    """
    sentence_id = []
    for word in sent:
        if word.isdigit():#是否为数字
            word = '<NUM>'
        elif ('\u0041' <= word <= '\u005a') or ('\u0061' <= word <= '\u007a'):  #\u0041 - \u005a   A-Z   \u0061 - \u007a  a-z
            word = '<ENG>'
        if word not in word2id:
            word = '<UNK>'
        sentence_id.append(word2id[word])
    return sentence_id

    # 读词典
def read_dictionary(vocab_path):
    """
     加载已生成的Word2id字典
    :param vocab_path:
    :return:
    """
    vocab_path = os.path.join(vocab_path)
    with open(vocab_path, 'rb') as fr:
        word2id = pickle.load(fr)
    print('vocab_size:', len(word2id))
    return word2id


def random_embedding(vocab, embedding_dim):
    """
    这里没有预先训练词向量，而是直接对词向量进行随机初始化
    :param vocab:
    :param embedding_dim:
    :return:
    """
    embedding_mat = np.random.uniform(-0.25, 0.25, (len(vocab), embedding_dim))
    embedding_mat = np.float32(embedding_mat)
    return embedding_mat

# 语句的填充
def pad_sequences(sequences, pad_mark=0):
    """
    对小于sequence长度的句子进行padding
    :param sequences:
    :param pad_mark:
    :return:
    """
    max_len = max(map(lambda x : len(x), sequences))
    seq_list, seq_len_list = [], []
    for seq in sequences:
        seq = list(seq)
        seq_ = seq[:max_len] + [pad_mark] * max(max_len - len(seq), 0)
        seq_list.append(seq_)
        seq_len_list.append(min(len(seq), max_len))
    return seq_list, seq_len_list


# 生成器  将输入文本转换成模型的输入
def batch_yield(data, batch_size, vocab, tag2label, shuffle=False):
    """
     产生批训练的数据
    :param data: 标记的训练数据
    :param batch_size: 批次大小
    :param vocab:   字典
    :param tag2label:
    :param shuffle: 是否随机
    :return: 词对应的数字  标签对应的数字
    """
    if shuffle:
        random.shuffle(data)    #随机排序

    seqs, labels = [], []
    for (sent_, tag_) in data: # sent_ 字或词 ，tag_ 标签
        sent_ = sentence2id(sent_, vocab)   # 词对应的数字
        label_ = [tag2label[tag] for tag in tag_]   # 标签对应的数字

        if len(seqs) == batch_size:
            yield seqs, labels      #yield 是一个类似 return 的关键字，迭代一次遇到yield时就返回yield后面的值。重点是：下一次迭代时，从上一次迭代遇到的yield后面的代码开始执行。
            seqs, labels = [], []

        seqs.append(sent_)
        labels.append(label_)

    if len(seqs) != 0:
        yield seqs, labels