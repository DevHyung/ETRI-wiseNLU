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

Issue:
    - 관용어구 같은경우 질의발화, 답변발화의 B-I 쌍이 안맞을 경우 어떻게 치환을 해야할까 ?
    - Insertion, Deletion words 끼리의 짝이 안맞을경우 ...
    - 그리고 관용어구 경우 I 태깅같은 경우 무조건적으로 치환을 해야하는거인가
    - 생성된 response는 기존 유사질문에 대한 답변찾은것보다 길이를 길어질수가없다 , 이거 유동적으로 ?

'''
from typing import List, TextIO, Dict

'''__________ CONFIG AREA START __________'''
DATA_DIR: str         = "data/"
Q_FILE_NAME: str      = "Q.txt"
Q_NER_FILE_NAME: str  = "Q_NER.txt"
Q_MORP_FILE_NAME: str = "Q_MORP.txt"
A_FILE_NAME: str      = "A.txt"
A_NER_FILE_NAME: str  = "A_NER.txt"
A_MORP_FILE_NAME: str = "A_MORP.txt"
NER_TAGLIST: List[str] = ['WT_TYPE', 'WT_ORIGIN', 'WT_OTHERS', 'WT_EXPRESSION', 'WT_IDIOM',
                      'FD_ORIGIN', 'FD_STORE', 'FD_FOOD', 'FD_MATERIAL', 'FD_MEAL',
                      'FD_TYPE', 'FD_DRINK', 'FD_EXPRESSION', 'FD_IDIOM', 'TI_CURRENT',
                      'TI_FUTURE', 'TI_PAST', 'TI_DURATION', 'DT_DURATION', 'DT_DAY',
                      'TI_OTHERS', 'DT_OTHERS', 'LC_OTHERS'] # total 23.

'''__________ CONFIG AREA END   __________'''

def log(tag, text)-> None:
    # Info tag
    if (tag == 'i'):
        print("[INFO] " + text)
    # Error tag
    elif (tag == 'e'):
        print("[ERROR] " + text)
    # Success tag
    elif (tag == 's'):
        print("[SUCCESS] " + text)

def get_data_from_txt(_filename)-> List[str]:
    """`

    :return: data List
    """
    dataList :List[str] = []
    f : TextIO = open(file=_filename, mode='r', encoding='utf8')

    for line in f.readlines():
        dataList.append(line.strip())

    f.close()
    log('s', "{} 파일에서 {} 줄 불러옴".format(_filename, len(dataList)))

    return dataList

def print_QA_by_index(_index)-> None:
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
def _make_print_width(_a,_b)-> [str,str]:
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

def _isOdd(_number)-> bool:
    return _number % 2 == 1

def generate_response(_query,_Squery)-> str:
    """

    :param _query: input query
    :param _Squery:유사하다고 걸린 query
    :return:
    """

    # return int, Dict[str,List[int]]
    qIdx, insertionWords = _extract_insertion_words_idx(_query)
    SqIdx, deletionWords = _extract_deletion_words_idx(_Squery)
    result = _replace_words(qIdx,insertionWords,SqIdx, deletionWords)

def _replace_words(_qIdx,_iWords,_SqIdx,_dWords)-> str:
    qm : List[str] = QMList[_qIdx].split(' ')
    Sam: List[str] = AMList[_SqIdx].split(' ')
    result = list(Sam)

    for ikey in _iWords.keys():
        try: # 두 개 겹침
            dWordList = _dWords[ikey]
            iWordList = _iWords[ikey]
            minIdx = min(len(dWordList),len(iWordList))

            for i in range(0,minIdx):
                result[dWordList[i]] = " * " + qm[dWordList[i]] + " * "
        except: # 없는키
            pass

    log('i', "원래 질문 : {}".format(qm))
    log('i', "Insertion Word:{}\n".format(_iWords))
    log('i', "원래 답변 : {}".format(Sam))
    log('i', "Deletion  Word:{}\n".format(_dWords))
    log('i', "최종 답변 : {}".format(result))

def _extract_insertion_words_idx(_sentence)-> [int, Dict[str,List[int]]]:
    """

    :param _sentence: input sentence
    :return: insertion words index list
    """
    result: Dict[str,List[int]] = {}
    idx = __search_index(_sentence,QList)

    print_QA_by_index(idx)

    loopIdx = 0
    for tag in QNList[idx].split(' '):
        if tag.split('-')[-1] in NER_TAGLIST:
            try:
                result[tag]
                result[tag].append(loopIdx)
            except:
                result[tag] = [loopIdx]
        loopIdx += 1
    return idx, result

def _extract_deletion_words_idx(_sentence)->  [int, Dict[str,List[int]]]:
    """

    :param _sentence: input sentence
    :return: insertion words index list
    """
    result: Dict[str,List[int]] = {}
    idx = __search_index(_sentence,QList)

    print_QA_by_index(idx)

    loopIdx = 0
    for tag in ANList[idx].split(' '):
        if tag.split('-')[-1] in NER_TAGLIST:
            try:
                result[tag]
                result[tag].append(loopIdx)
            except:
                result[tag] = [loopIdx]
        loopIdx += 1
    return idx, result


def __search_index(_sentence,_targetList)-> int:
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
        log('e',"{} 문장을 찾지 못하였습니다.".format(_sentence))
        return -1



if __name__ == "__main__":
    # Make DB
    QList : List[str] = get_data_from_txt(DATA_DIR + Q_FILE_NAME)
    AList : List[str] = get_data_from_txt(DATA_DIR + A_FILE_NAME)
    QNList: List[str] = get_data_from_txt(DATA_DIR + Q_NER_FILE_NAME)
    ANList: List[str] = get_data_from_txt(DATA_DIR + A_NER_FILE_NAME)
    QMList: List[str] = get_data_from_txt(DATA_DIR + Q_MORP_FILE_NAME)
    AMList: List[str] = get_data_from_txt(DATA_DIR + A_MORP_FILE_NAME)

    # TEST
    # 4, 8이 유사하게 잡혔다고 생각
    #print_QA_by_index(4)
    #print_QA_by_index(8)

    # 여기에 비슷한 문장을 찾는게 있어야함
    # 발화문장, 유사문장을 같이넣으면
    generate_response('미세먼지 때문에 창밖에 아무것도 안 보여.','출근해야 되는데 밖에 눈 많이 쌓여서 걱정이야.')
