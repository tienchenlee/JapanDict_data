#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import random
import requests
from bs4 import BeautifulSoup
from time import sleep
from pprint import pprint

def main(url):
    """
    先從首頁取得每個標題的網址，然後抓取對應的四字成語（漢字與平假名）。
    參數：
        url (str): 首頁網址。
    
    回傳：
        resultLIST (list): 包含四字成語的列表，每個元素為一個字典，格式如下：
            [
                {
                    "kanji": "哀哀父母",
                    "hiragana": "あいあいふぼ"
                },
                ...
            ]
    """
    
    response = requests.get(url, headers=headers)    
    htmlSTR = response.text
    soup = BeautifulSoup(htmlSTR, "lxml")
    
    resultLIST = []
    lv1LIST = soup.find_all("li", class_="lv1")
    
    #拿到 href 標籤內的 link
    hrefLIST = [l.find("a").get("href") for l in lv1LIST]
    #標題完整 link
    title_urlLIST = [f"https://dictionary.goo.ne.jp" + h for h in hrefLIST]
    
    for t in title_urlLIST:
        print(f"processing '{t}'")
        response = requests.get(t, headers=headers)
        sleep(random.randrange(1, 10))        
        htmlSTR = response.text
        soup = BeautifulSoup(htmlSTR, "lxml")
        
        titleTag_l = soup.find_all("p", class_="title")
        titleLIST = [t.get_text().strip() for t in titleTag_l]
        
        for t in titleLIST:
            idiomLIST = t.split("【")
            idiomLIST = [i.replace("】", "").replace("-", "") for i in idiomLIST]
            print(idiomLIST)
            print(f"---------------------")
        
            resultDICT = {"kanji": idiomLIST[1], "hiragana": idiomLIST[0]}
            resultLIST.append(resultDICT)
    pprint(resultLIST)

    return resultLIST



if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    url = f"https://dictionary.goo.ne.jp/idiom/"
    resultLIST = main(url)
    
    data_folder = "../data"
    os.makedirs(data_folder, exist_ok=True)
    jsonFILE = f"{data_folder}/goo_idiom.json"
    with open(jsonFILE, "w", encoding="utf-8") as f:
        json.dump(resultLIST, f, ensure_ascii=False, indent=4)