#coding=utf-8
# content 에 태깅한 문자열을 넣은다
#   - 넣을때는 형태소 빼고 품사태그만 넣은다 NNG, NNP 같은거
# title 에는 원문을 넣는다.
# path는 날씨 wt, 음식 fd 이렇게 두가지로 나눈다.
import operator
import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from typing import List, TextIO,Dict
import time
'''__________ CONFIG AREA START __________'''
DATA_DIR: str         = "../WISEKB/data/"
Q_FILE_NAME: str      = "tmpQ.txt" # Q.txt
Q_MORP_FILE_NAME: str = "tmpQ_M.txt" ## Q_MORP.txt
A_FILE_NAME: str      = "A.txt"
A_MORP_FILE_NAME: str = "A_MORP.txt"
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

def extract_morp_str(_morpStr: str) -> str:
    """

    :param _morpStr: morp long string
    :return: 품사만 남은 string
    """
    tmp: str = ""
    splitList = _morpStr.split(' ')
    for morp in splitList:
        try:
            tmp += morp.split('/')[1] + " "
        except:  # 공백인 경우, 형태소분석결과가 없음
            pass
    return tmp.strip()

def get_morp_from_list(_sentece)-> str:
    idx: int = QList.index(_sentece)
    morpStr: str = extract_morp_str(QMList[idx])
    return morpStr

if __name__ == "__main__":
    # Load dataset data
    QList: List[str] = get_data_from_txt(DATA_DIR + Q_FILE_NAME)
    QMList: List[str] = get_data_from_txt(DATA_DIR + Q_MORP_FILE_NAME)
    tuneQMList :List[str] = []
    # Set index directory
    indexdir = './ndx'
    if not os.path.exists(indexdir):
        os.makedirs(indexdir)

    # Set schema
    schema = Schema(title=TEXT(stored=True),
                    path=ID(stored=True),
                    content=NGRAMWORDS(maxsize=2, stored=True),
                    idx=ID(stored=True))
    # create schema
    ix = create_in(indexdir, schema)

    # Define the writer for search Inverted
    writer = ix.writer()

    # Preprocess
    for fori in range(len(QMList)):
        tuneQMList.append(extract_morp_str(QMList[fori]))

    # Build DB
    for fori in range( len(QList) ):
        writer.add_document(title=u"{}".format(QList[fori]),
                            path=u"/wt",
                            content=u"{}".format(tuneQMList[fori]),
                            idx=u"{}".format(fori))
    writer.commit()

    # Search

    f = open('input.txt','r',encoding='utf8')
    querys = f.readlines()
    f.close()
    outF = open('output.txt','w',encoding='utf8')
    '''
    # 데이터 모자른거 채울때 문서수정할때
    for query in querys:
        query = query.strip()
        try:
            queryIdx = QList.index(query)
        except:
            print(query)
    exit(-1)
    '''
    with ix.searcher() as searcher:
        qp = QueryParser("content", ix.schema)
        idx = 1
        # time checking
        start = time.time()
        for query in querys:
            dataDict: Dict[int, int] = {}
            print("{}번째 진행중..".format(idx))
            idx += 1
            query = query.strip()
            queryIdx = QList.index(query)
            morpStr = get_morp_from_list(query)
            splitMorp = morpStr.split(' ')
            for fori in range(len(splitMorp) - 1):
                user_q = qp.parse(u'{}'.format(splitMorp[fori]+" "+splitMorp[fori+1]))
                results = searcher.search(user_q, limit=10)
                for r in results:
                    print(r, r.score, r.rank, r.docnum, r['content'])
                    try:
                        dataDict[r['idx']] += r.score
                    except:
                        dataDict[r['idx']] = r.score
            sortedTmp = sorted(dataDict.items(), key=operator.itemgetter(1), reverse=True)
            while True:
                top = sortedTmp.pop(0)
                if int(top[0]) == queryIdx:
                    pass
                else:
                    outF.write(QList[int(top[0])] + '\n')
                    break
        end = time.time()
        # time checking end
        print(end-start) # 42.87초 200개 = 개당 0.2초
