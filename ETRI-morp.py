# -*- coding:utf-8 -*-
'''
reference :
    http://aiopen.etri.re.kr/guide_wiseNLU.php
'''
import urllib3
import json
from typing import List, TextIO
from CONFIG import *

'''__________ CONFIG AREA START __________ '''
openApiURL :str = "http://aiopen.etri.re.kr:8000/WiseNLU"
analysisCode :str = "morp" #형태소 분석
requestJson = {
    "access_key": ACCESSKEY, # from CONFIG file
    "argument": {
        "text": '',
        "analysis_code": analysisCode
    }
}
'''__________ CONFIG AREA END   __________ '''

if __name__ == "__main__":
    ### Var
    textList: List[str] = [] #input txt string list
    result: str = ''
    outputF : TextIO = open("output.txt","w",encoding='utf8') #저장할 파일 file output stream

    ### file read
    try:
        f = open("input.txt", 'r', encoding='utf8')
    except OSError:
        print('cannot open')
    else:
        for line in f.readlines():
            textList.append(line.strip())
        print("[INFO] Input file has", len(textList), 'lines')
        f.close()

    ### Make http pool & request
    http = urllib3.PoolManager()
    for text in textList:
        requestJson['argument']['text'] = text
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
        )
        # Parsing & save
        print("[responseCode] " + str(response.status))
        print("[Query Text ] ",text.strip())

        jsonStr = json.loads(str(response.data, "utf-8"))
        for morp in jsonStr['return_object']['sentence']:
            for m in morp['morp']:
                result += "{}/{} ".format(m['lemma'],m['type'])
        print("[Result Text] ",result)
        outputF.write(result+'\n')
        result = ''
    outputF.close()
    print("[INFO] complete save at output.txt")




