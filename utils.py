import logging, sys, argparse
#-*- coding:utf-8 _*-

# 将肯定或者否定回答转成bool型
def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# 获取不同的实体
def get_entity(tag_seq, char_seq):
    return get_acc_entity(tag_seq, char_seq) # 获取会计知识实体


# 获取会计知识实体
def get_acc_entity(tag_seq, char_seq):
    length = len(char_seq)
    ACC = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-Acc':
            if 'acc' in locals().keys():
                ACC.append(acc)
                del acc
            acc = char
            if i + 1 == length:
                ACC.append(acc)
        if tag == 'M-Acc':
            if 'acc' not in locals().keys():
                acc=char
            else:
                acc += char
            if i + 1 == length:
                ACC.append(acc)
        if tag == 'E-Acc':
            if 'acc' not in locals().keys():
                acc = char
            else:
                acc += char
            if i + 1 == length:
                ACC.append(acc)
        if tag not in ['B-Acc', 'M-Acc', 'E-Acc']:
            if 'acc' in locals().keys():
                ACC.append(acc)
                del acc
            continue
    return ACC

#词条数据读取 返回
def readword(file_url):
    wordList = [] #词条列表
    with open(file_url, "r+",encoding='utf-8') as f:
        text =f.read()
    return text

#写请求接口失败/正常的 词条
def write_word(file_url, text):
    with open(file_url, "a+",encoding='utf-8') as f:
        f.write(text+'\n')
# 分句
def cut_sentences(sentence):
    puns = frozenset(u'。！？')
    tmp = []
    for ch in sentence:
        tmp.append(ch)
        if puns.__contains__(ch):
            yield ''.join(tmp)
            tmp = []
    yield ''.join(tmp)

#日志函数
def get_logger(filename):
    # 输出格式
    __fmt = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(__fmt))
    logging.getLogger().addHandler(handler)
    return logger

