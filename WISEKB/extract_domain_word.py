# -*- coding:utf-8 -*-
from typing import List, TextIO, Dict

'''__________ CONFIG AREA START __________'''
DATA_DIR: str = "data/1차중간점검데이터_음식/"

Q_NER_FILE_NAME: str = "Q_NER.txt"
Q_MORP_FILE_NAME: str = "Q_MORP.txt"

A_NER_FILE_NAME: str = "A_NER.txt"
A_MORP_FILE_NAME: str = "A_MORP.txt"
NER_TAGLIST: List[str] = ['FD_ORIGIN', 'FD_STORE', 'FD_FOOD', 'FD_MATERIAL', 'FD_MEAL','FD_TYPE', 'FD_DRINK', 'FD_EXPRESSION', 'FD_IDIOM']
'''
날씨 
['WT_TYPE', 'WT_ORIGIN', 'WT_OTHERS', 'WT_EXPRESSION', 'WT_IDIOM']
음식
['FD_ORIGIN', 'FD_STORE', 'FD_FOOD', 'FD_MATERIAL', 'FD_MEAL','FD_TYPE', 'FD_DRINK', 'FD_EXPRESSION', 'FD_IDIOM']
'''

'''__________ CONFIG AREA END   __________'''

def log(tag, text) -> None:
    # Info tag
    if (tag == 'i'):
        print("[INFO] " + text)
    # Error tag
    elif (tag == 'e'):
        print("[ERROR] " + text)
    # Success tag
    elif (tag == 's'):
        print("[SUCCESS] " + text)


def get_data_from_txt(_filename) -> List[str]:
    """`

    :return: data List
    """
    dataList: List[str] = []
    f: TextIO = open(file=_filename, mode='r', encoding='utf8')

    for line in f.readlines():
        dataList.append(line.strip())

    f.close()
    log('s', "{} 파일에서 {} 줄 불러옴".format(_filename, len(dataList)))

    return dataList


def get_domain_word(_MList,_NList,_FILENAME):
    m = _MList.copy()
    n = _NList.copy()
    result = ''
    f = open(_FILENAME,'w',encoding='utf8')

    for idx in range(len(_MList)):
        isExistB = False
        mlist = m[idx].split(' ')
        nlist = n[idx].split(' ')
        for tagIdx in range(len(mlist)):
            try:
                biTag,nerTag = nlist[tagIdx].split('-')

                if biTag.strip() == 'B' and nerTag.strip() in NER_TAGLIST:
                    if isExistB: #  새로운게 시작
                        print(result[:-1])
                        f.write(result[:-1] + '\n')
                        result = ''
                        result += nerTag + ':' + mlist[tagIdx] + '+'
                    else:
                        isExistB = True
                        result += nerTag + ':' + mlist[tagIdx] + '+'
                elif biTag.strip() == 'I' and isExistB and nerTag.strip() in NER_TAGLIST:
                    result += mlist[tagIdx] + '+'
            except:
                if isExistB:
                    isExistB = False
                    print(result[:-1])
                    f.write(result[:-1] + '\n')
                    result = ''
                else:
                    pass

    f.close()

if __name__ == "__main__":
    # Make DB
    QNList: List[str] = get_data_from_txt(DATA_DIR + Q_NER_FILE_NAME)
    ANList: List[str] = get_data_from_txt(DATA_DIR + A_NER_FILE_NAME)
    QMList: List[str] = get_data_from_txt(DATA_DIR + Q_MORP_FILE_NAME)
    AMList: List[str] = get_data_from_txt(DATA_DIR + A_MORP_FILE_NAME)

    get_domain_word(QMList,QNList,"DOMAIN_FD.txt")

