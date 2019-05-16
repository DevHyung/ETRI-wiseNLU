#coding=utf-8
# 05.16 교수요청사항
# 기존의 Search Engine 에서 했던것처럼
# 단어들을 lexical 단위에서 + 형태소 단위에서
# 구조가 아닌 단어들의 이치를 보고 하면 어떻게 되느냐에 대한 코드 작성

import operator
import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from typing import List, TextIO,Dict
import time
'''__________ CONFIG AREA START __________'''
DATA_DIR: str         = "../WISEKB/data/"
Q_FILE_NAME: str      = "tmpQ_WT.txt" # Q.txt
Q_MORP_FILE_NAME: str = "tmpQ_M_WT.txt" ## Q_MORP.txt
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

def tmp_get_morp_from_list(_sentece)-> str:
    idx: int = QList.index(_sentece)
    tmp: str = ""
    splitList = QMList[idx].split(' ')
    for morp in splitList:
        try:
            tmp += morp.strip() + " "
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
    indexdir = './origin_ndx'
    if not os.path.exists(indexdir):
        os.makedirs(indexdir)

    # Set schema
    schema = Schema(title=TEXT(stored=True),
                    path=ID(stored=True),
                    content=NGRAMWORDS(minsize=2, maxsize=3, stored=True),
                    idx=ID(stored=True))
    # create schema
    ix = create_in(indexdir, schema)

    # Define the writer for search Inverted
    writer = ix.writer()

    # Preprocess
    # 1. lexical 단위에서 할꺼면 그냥 문장 그대로 content 에 넣으면 됨.
    # 2. 형태소 단위니까 태그 안 떼고 넣기로함

    #for fori in range(len(QList)):# 1. Lexical
        #tuneQMList.append(QList[fori])# 1. Lexical
    for fori in range(len(QMList)):
        tuneQMList.append(QMList[fori])# 2. g형태소단위

    # Build DB
    for fori in range( len(QList) ):
        writer.add_document(title=u"{}".format(QList[fori]),
                            path=u"/wt",
                            content=u"{}".format(tuneQMList[fori]),
                            idx=u"{}".format(fori))
    writer.commit()


    # create query datas from input file and
    # create output file stream
    f = open('input.txt','r',encoding='utf8')
    querys: List[str] = f.readlines()
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

    # Search
    with ix.searcher() as searcher:
        qp = QueryParser("content", ix.schema)
        idx = 1
        # time checking
        start = time.time()
        for query in querys:
            dataDict: Dict[int, int] = {}
            log('i', "{}번째 검색중..".format(idx))
            idx += 1
            query = query.strip()
            queryIdx = QList.index(query)

            # 1. lexical 단위이기에 필요없음
            #    추가적으로 N-gram 햇던부분도 필요없어서 뺌
            # querySplit = query.split(' ')
            # for q in querySplit:
            #     user_q = qp.parse(u'{}'.format(q))
            #     results = searcher.search(user_q, limit=5)
            #     for r in results:
            #         try:
            #             dataDict[r['idx']] += r.score
            #         except:
            #             dataDict[r['idx']] = r.score
            #
            # sortedTmp = sorted(dataDict.items(), key=operator.itemgetter(1), reverse=True)

            # 2. 형태소 단위이기에 필요없음
            morpStr = tmp_get_morp_from_list(query)
            splitMorp = morpStr.split(' ')
            for q in splitMorp:
                user_q = qp.parse(u'{}'.format(q))
                results = searcher.search(user_q, limit=5)
                for r in results:
                    try:
                        dataDict[r['idx']] += r.score
                    except:
                        dataDict[r['idx']] = r.score

            sortedTmp = sorted(dataDict.items(), key=operator.itemgetter(1), reverse=True)

            #morpStr = get_morp_from_list(query)
            #splitMorp = morpStr.split(' ')

            # # bi-gram weight sum
            # for fori in range(len(splitMorp) - 1):
            #     user_q = qp.parse(u'{}'.format(splitMorp[fori]+" "+splitMorp[fori+1]))
            #     results = searcher.search(user_q, limit=10)
            #     for r in results:
            #         try:
            #             dataDict[r['idx']] += r.score
            #         except:
            #             dataDict[r['idx']] = r.score
            # # Tri-gram weight sum
            # # 여기를 지우면 단순하게 bi-gram 까지만의 weight sum 을 이용
            # for fori in range(len(splitMorp) - 2):
            #     user_q = qp.parse(u'{}'.format(splitMorp[fori]+" "+splitMorp[fori+1]+" "+splitMorp[fori+2]))
            #     results = searcher.search(user_q, limit=10)
            #     for r in results:
            #         try:
            #             dataDict[r['idx']] += r.score
            #         except:
            #             dataDict[r['idx']] = r.score
            # sortedTmp = sorted(dataDict.items(), key=operator.itemgetter(1), reverse=True)
            # Toprank 5개 뽑아야하니까
            cnt = 0
            if len(sortedTmp) < 6:
                for _ in range(5):
                    outF.write('\n')
            else:
                while True:
                    if cnt == 5:
                        break

                    top = sortedTmp.pop(0)

                    if int(top[0]) == queryIdx: # 자기랑 같은 문장은 제외
                        first = False
                        pass
                    else:
                        outF.write(QList[int(top[0])] + '\n')
                        cnt += 1
        end = time.time()
        # time checking end
        print(end-start) # only bi-gram = 42.87초, 개당 0.21초  | include tri-gram 57.36초 개당 0.28초
    outF.close()