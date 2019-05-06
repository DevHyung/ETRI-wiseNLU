# -*- coding:utf-8 -*-
'''
This file is Skeleton-Dialogue-Generation Guide by IR (modifed alignment alg.)

function flow:
    - make DB( dict type pre-trained data )
    -
data descriotion:
    All file seperated '\n'
    - Q.txt  # Question sentences
    - Qm.txt # Morp of question sentences
    - A.txt  # Answer sentences
    - Am.txt # Morp of Answer senetences
'''
from typing import List, TextIO

'''__________ CONFIG AREA START __________'''
DATA_DIR: str         = "data/"
Q_FILE_NAME: str      = "Q.txt"
Q_NER_FILE_NAME: str  = "Q_NER.txt"
Q_MORP_FILE_NAME: str = "Q_MORP.txt"
A_FILE_NAME: str      = "A.txt"
A_NER_FILE_NAME: str  = "A_NER.txt"
A_MORP_FILE_NAME: str = "A_MORP.txt"
'''__________ CONFIG AREA END   __________'''


def log(tag, text):
    # Info tag
    if (tag == 'i'):
        print("[INFO] " + text)
    # Error tag
    elif (tag == 'e'):
        print("[ERROR] " + text)
    # Success tag
    elif (tag == 's'):
        print("[SUCCESS] " + text)

def get_data_from_txt(_filename):
    """`

    :return: data List
    """
    dataList :List[str] = []
    f : TextIO = open(file=_filename, mode='r', encoding='utf8')

    for line in f.readlines():
        dataList.append(line.strip())

    f.close()
    log('s', "{} 파일에서 {} 줄 불러오기".format(_filename, len(dataList)))

    return dataList

def print_QA_by_index(_index):
    QMstr, QNstr = _make_print_width(QMList[_index], QNList[_index])
    AMstr, ANstr = _make_print_width(AMList[_index], ANList[_index])
    print("__________" * 3)
    print("입력발화     : {}".format(QList[_index]))
    print("입력발화 MORP: {}개-> {}".format(len(QMList[_index].split(' ')), QMstr))
    print("입력발화 NER : {}개-> {}".format(len(QNList[_index].split(' ')), QNstr))
    print("   답변     : {}".format(AList[_index]))
    print("   답변 MORP: {}개-> {}".format(len(AMList[_index].split(' ')), AMstr))
    print("   답변 NER : {}개-> {}".format(len(ANList[_index].split(' ')), ANstr))
    print("__________" * 3)
def _make_print_width(_a,_b):
    aSplit = _a.split(' ')
    bSplit = _b.split(' ')
    resultA = ""
    resultB = ""
    for i in range(len(aSplit)):
        width = max(len(aSplit[i].encode('utf-8')), len(bSplit[i].encode('utf-8')))
        utf8CntA = len(aSplit[i].encode('utf-8')) - len(aSplit[i])
        utfPlusB = 0
        if len(bSplit[i].encode('utf-8')) == 1 and utf8CntA == 2:
            utfPlusB = 1

        if _isOdd(utf8CntA):
            utf8CntA = int((utf8CntA + 1) / 2)
        else:
            utf8CntA = int((utf8CntA) / 2)
        if utf8CntA != 0:
            utf8CntA -= 1
        resultA += aSplit[i].ljust(width - utf8CntA, ' ') + ' '
        resultB += bSplit[i].ljust(width + utfPlusB, ' ') + ' '
    return resultA, resultB

def _isOdd(_number):
    return _number % 2 == 1
if __name__ == "__main__":
    # Make DB
    QList : List[str] = get_data_from_txt(DATA_DIR + Q_FILE_NAME)
    AList : List[str] = get_data_from_txt(DATA_DIR + A_FILE_NAME)
    QNList: List[str] = get_data_from_txt(DATA_DIR + Q_NER_FILE_NAME)
    ANList: List[str] = get_data_from_txt(DATA_DIR + A_NER_FILE_NAME)
    QMList: List[str] = get_data_from_txt(DATA_DIR + Q_MORP_FILE_NAME)
    AMList: List[str] = get_data_from_txt(DATA_DIR + A_MORP_FILE_NAME)

    # TEST
    print_QA_by_index(1)
