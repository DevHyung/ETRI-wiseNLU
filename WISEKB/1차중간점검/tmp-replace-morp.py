# -*- coding:utf-8 -*-
'''
This file is script that simply replace morp
1. align 된거에서 원본쿼리의 형태소를찾고
2. SQ 의 답변에대한 형태소를 찾고
3. NNG / VV만을 치환
'''
from typing import List, TextIO, Dict

'''__________ CONFIG AREA START __________'''
DATA_DIR: str = "../data/"
Q_FILE_NAME: str = "align_Q_WT.txt"
SQ_FILE_NAME: str = "align_SQ_WT.txt"

Q_MORP_FILE_NAME: str = "Q_MORP.txt"
A_MORP_FILE_NAME: str = "A_MORP.txt"


MOPR_TAGET: List[str] = ['NNG','VV']

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
    """
    :return: data List
    """
    dataList: List[str] = []
    f: TextIO = open(file=_filename, mode='r', encoding='utf8')

    for line in f.readlines():
        dataList.append(line.strip())

    f.close()
    log('s', "{} 파일에서 {} 줄 불러옴".format(_filename, len(dataList)))

    return dataList

def search_index(_sentence, _targetList) -> int:
    """

    :param _sentence: input sentece
    :param _targetList: target list for search
    :return: index
    """
    idx = 0
    isExist = False
    for sentence in _targetList:
        if _sentence == sentence:
            isExist = True
            break
        else:
            idx += 1
    if isExist:
        return idx
    else:
        log('e', "{} 문장을 찾지 못하였습니다.".format(_sentence))
        return -1
def select_sentence()-> List[str]:
    # Make DB
    originQList: List[str] = get_data_from_txt(DATA_DIR + "Q.txt")
    QList: List[str] = get_data_from_txt(DATA_DIR + Q_FILE_NAME)
    SQList: List[str] = get_data_from_txt(DATA_DIR + SQ_FILE_NAME)

    QMList: List[str] = get_data_from_txt(DATA_DIR + Q_MORP_FILE_NAME)
    AMList: List[str] = get_data_from_txt(DATA_DIR + A_MORP_FILE_NAME)

    QNERList: List[str] = get_data_from_txt(DATA_DIR + "Q_NER.txt")
    ANERList: List[str] = get_data_from_txt(DATA_DIR + "A_NER.txt")

    # Process
    resultList = []
    resultSList = []

    # 질문 100개 선정
    # 질의응답큐에서 최대한 NER 태깅된거 100개 필요
    # QList 에서 -> originQList 에서 인덱스를 가져와서
    # Q_NER 에서 그 인덱스가 비어있는지 확인
    cnt = 0
    for i in range(len(QList)):
        q = QList[i]
        sq = SQList[i]
        try:
            idx = originQList.index(q)  # 원본 질문에서 INDEX가져와서
            sidx = originQList.index(sq)  # 원본 질문에서 INDEX가져와서
            # morp 결과가 비었는지보자
            if QNERList[idx] != '-' and ANERList[idx] != '-' and QNERList[sidx] != '-' and ANERList[sidx] != '-':
                if len(QNERList[idx])==0 or len(ANERList[idx])==0:
                    pass
                else:
                    resultList.append(q)
                    resultSList.append(sq)
                    cnt += 1
            if cnt == 100:
                break

        except:  # 없는거
            pass

    for sentece in resultList:
        print(sentece)
    print("@@@유사문장@@@")
    for sentece in resultSList:
        print(sentece)
    return resultList


if __name__ == "__main__":

    # Make DB
    originQList: List[str] = get_data_from_txt(DATA_DIR + "Q.txt")
    QList: List[str] = get_data_from_txt(DATA_DIR + Q_FILE_NAME)
    SQList: List[str] = get_data_from_txt(DATA_DIR + SQ_FILE_NAME)

    QMList: List[str] = get_data_from_txt(DATA_DIR + Q_MORP_FILE_NAME)
    AMList: List[str] = get_data_from_txt(DATA_DIR + A_MORP_FILE_NAME)

    QNERList: List[str] = get_data_from_txt(DATA_DIR + "Q_NER.txt")
    ANERList: List[str] = get_data_from_txt(DATA_DIR + "A_NER.txt")

    # 형태소 단위 명동사만으로 변환하는거
    for i in range(len(QList)):
        # i는 QLIST의 순번 idx 는 원래 orgin QLIST의 번호
        input_idx = originQList.index(QList[i]) # input문장의 idx
        sinput_idx = originQList.index(SQList[i]) # input문장의 유사문장의 idx
        sAnswer_morp = AMList[sinput_idx]  # input문장의 유사문장의 답변의 idx
        # Print
        #print('_' * 30)
        #print("원래질문      :", QList[i])
        #print("원래질문 형태소:", QMList[input_idx])
        #print("유사질문      :", SQList[i])
        #print("유사질문 답변형:", sAnswer_morp)


        # insertion word
        iresult: Dict[str, List[int]] = {}
        loopIdx = 0
        for tag in QMList[input_idx].split(' '):
            if tag.split('/')[-1] in MOPR_TAGET:
                try:
                    iresult[tag.split('/')[-1]].append(loopIdx)
                except:
                    iresult[tag.split('/')[-1]] = [loopIdx]
            loopIdx += 1

        # Deletion word
        dresult: Dict[str, List[int]] = {}
        loopIdx = 0
        for tag in sAnswer_morp.split(' '):
            if tag.split('/')[-1] in MOPR_TAGET:
                try:
                    dresult[tag.split('/')[-1]].append(loopIdx)
                except:
                    dresult[tag.split('/')[-1]] = [loopIdx]
            loopIdx += 1
        #print (iresult)
        #print (dresult)

        qm: List[str] = QMList[input_idx].split(' ')
        Sam: List[str] = sAnswer_morp.split(' ')
        result = list(Sam)

        for ikey in iresult.keys():
            try:  # 두 개 겹침
                dWordList = dresult[ikey]
                iWordList = iresult[ikey]
                minIdx = min(len(dWordList), len(iWordList))

                for i in range(0, minIdx):
                    result[dWordList[i]] = qm[iWordList[i]]
            except:  # 없는키
                pass
        #print(' '.join(result))
        tmpStr = ''
        for r in result:
            tmpStr += r.split('/')[0] + ' '
        print(tmpStr)

