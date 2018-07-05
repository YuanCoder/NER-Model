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
    #PER = get_PER_entity(tag_seq, char_seq)
    STATE = get_state_entity(tag_seq, char_seq) #获取描述性知识
    PROCESS = get_process_entity(tag_seq, char_seq) #获取过程性知识
    ORG = get_Organization_entity(tag_seq, char_seq) #获取组织
    return STATE, PROCESS, ORG


def get_PER_entity(tag_seq, char_seq):
    length = len(char_seq)
    PER = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-PER':
            if 'per' in locals().keys():
                PER.append(per)
                del per
            per = char
            if i+1 == length:
                PER.append(per)
        if tag == 'I-PER':
            per += char
            if i+1 == length:
                PER.append(per)
        if tag not in ['I-PER', 'B-PER']:
            if 'per' in locals().keys():
                PER.append(per)
                del per
            continue
    return PER

# 获取描述知识实体
def get_state_entity(tag_seq, char_seq):
    length = len(char_seq)
    STATE = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-State':
            if 'state' in locals().keys():
                STATE.append(state)
                del state
            state = char
            if i + 1 == length:
                STATE.append(state)
        if tag == 'M-State':
            if 'state' not in locals().keys():
                state=char
            else:
                state += char
            if i + 1 == length:
                STATE.append(state)
        if tag == 'E-State':
            if 'state' not in locals().keys():
                state = char
            else:
                state += char
            if i + 1 == length:
                STATE.append(state)
        if tag not in ['B-State', 'M-State', 'E-State']:
            if 'state' in locals().keys():
                STATE.append(state)
                del state
            continue
    return STATE


def get_LOC_entity(tag_seq, char_seq):
    length = len(char_seq)
    LOC = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-LOC':
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            loc = char
            if i+1 == length:
                LOC.append(loc)
        if tag == 'I-LOC':
            loc += char
            if i+1 == length:
                LOC.append(loc)
        if tag not in ['I-LOC', 'B-LOC']:
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            continue
    return LOC

# 获取过程性知识实体
def get_process_entity(tag_seq, char_seq):
    length = len(char_seq)
    PROCESS = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-Process':
            if 'process' in locals().keys():
                PROCESS.append(process)
                del process
            process = char
            if i+1 == length:
                PROCESS.append(process)
        if tag == 'M-Process':
            if 'process' not in locals().keys():
                process=char
            else:
                process += char
            if i+1 == length:
                PROCESS.append(process)
        if tag == 'E-Process':
            process += char
            if i+1 == length:
                PROCESS.append(process)
        if tag not in ['B-Process', 'M-Process', 'E-Process']:
            if 'process' in locals().keys():
                PROCESS.append(process)
                del process
            continue
    return PROCESS


def get_ORG_entity(tag_seq, char_seq):
    length = len(char_seq)
    ORG = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-ORG':
            if 'org' in locals().keys():
                ORG.append(org)
                del org
            org = char
            if i+1 == length:
                ORG.append(org)
        if tag == 'I-ORG':
            org += char
            if i+1 == length:
                ORG.append(org)
        if tag not in ['I-ORG', 'B-ORG']:
            if 'org' in locals().keys():
                ORG.append(org)
                del org
            continue
    return ORG

# 获取组织实体
def get_Organization_entity(tag_seq, char_seq):
    length = len(char_seq)
    ORG = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-Organization':
            if 'organization' in locals().keys():
                ORG.append(org)
                del org
            org = char
            if i+1 == length:
                ORG.append(org)
        if tag == 'M-Organization':
            if 'process' not in locals().keys():
                process=char
            else:
                org += char
            if i+1 == length:
                ORG.append(org)
        if tag == 'E-Organization':
            org += char
            if i+1 == length:
                ORG.append(org)
        if tag not in ['B-Organization', 'M-Organization', 'E-Organization']:
            if 'organization' in locals().keys():
                ORG.append(org)
                del org
            continue
    return ORG

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