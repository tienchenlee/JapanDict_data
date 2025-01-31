#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import requests
from bs4 import BeautifulSoup

def main(category_url):
    """
    從目標頁面遍歷每一頁，爬取指定詞性類別的單字資訊，並整理為字典格式放入列表，輸出 JSON 檔案。

    參數:
        category_url (str): 詞性類別的網址，例如 https://www.japandict.com/lists/pos/adj。

    回傳:
        list[dict]: 包含單字資訊字典的列表，每個元素格式如下：
            {
                "kanji": str,     # 漢字
                "haragana": str,  # 平假名
                "romanji": str,   # 羅馬拼音
                "tag": list[str]  # 詞性標籤列表
            }
    """
    #resultDICT = {"kanji": "", "haragana": "", "romanji": "", "tag": []}
    last_pageINT = get_page(category_url)   #拿到每個類別的最後一頁
    
    for i in range(1, last_pageINT + 1):    #從第一頁～最後一頁
        page_url = category_url + f"?page={i}"  #拿到每頁網址爬蟲
        response = requests.get(page_url, headers=headers)    
        htmlSTR = response.text
        soup = BeautifulSoup(htmlSTR, "lxml")
        
        resultLIST = []
        
        wordLIST = soup.find_all("a", class_="list-group-item list-group-item-action my-2 mdshadow-1")
        for w in wordLIST:  #根據每個字找到所需資訊
            kanjiTag = w.find("span", class_="xlarge text-normal me-4")
            kanjiSTR = kanjiTag.get_text()
            print(f"kanji:{kanjiSTR}")
            
            haraganaTag = w.find("span", class_="text-muted me-4")
            haraganaSTR = haraganaTag.get_text()
            print(f"haragana:{haraganaSTR}")
            
            romanjiTag = w.find("i", class_="text-muted xsmall")
            romanjiSTR = romanjiTag.get_text()
            print(f"romanji:{romanjiSTR}")
            
            tagLIST = w.find_all("span", attrs={"data-toggle": "tooltip"})
            tag_l = [t.get_text() for t in tagLIST if tagLIST]
            print(f"tags:{tag_l}")
            print(f"------------------------------------")
            
            resultDICT = {"kanji": kanjiSTR, "haragana": haraganaSTR, "romanji": romanjiSTR, "tag": tag_l}
            resultLIST.append(resultDICT)
            
        try:    #待改
            with open(jsonFILE, "r", encoding="utf-8") as f:
                existing_LIST = json.load(f)
                
                
        except (FileNotFoundError, json.JSONDecodeError):
            existing_LIST = []

        # 合併新數據
        existing_LIST.extend(resultLIST)

        # 寫回 JSON 檔案
        with open(jsonFILE, "w", encoding="utf-8") as f:
            json.dump(existing_LIST, f, ensure_ascii=False, indent=4)
            
    return None

def get_page(category_url):
    """
    從每個詞性類別的網址，拿到總頁數。
    
    參數 (str): 拿到詞性類別的網址。
    
    回傳 (int): 拿到該詞性類別的總頁數。
    
    """
    response = requests.get(category_url, headers=headers)    
    htmlSTR = response.text
    soup = BeautifulSoup(htmlSTR, "lxml")
    word_numTag = soup.find("div", class_="flex-grow-1")    
    word_numSTR = ((word_numTag.find_all("strong"))[1]).get_text()  #找到總共幾筆單字
    last_pageINT = (int(word_numSTR) // 10) + (1 if int(word_numSTR) % 10 != 0 else 0)  #每頁10個單字，算出總頁數
    print(f"total pages in this category:{last_pageINT}")
    return last_pageINT

if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    resultLIST = []
    jsonFILE = "./japandict.json"
    categoryLIST = ["adj", "adv", "v1", "v5"]   #要抓取的詞性類別
    
    if os.path.exists(jsonFILE):
        with open(jsonFILE, "r", encoding="utf-8") as f:
            resultLIST = json.load(f)
    
    for c in categoryLIST:
        print(f"processing in '{c.upper()}' now...")
        category_url = f"https://www.japandict.com/lists/pos/{c}"
        main(category_url)
    
    #[
        #{"kanji": "安全", "haragana": "あんぜん", "romanji": "anzen", "tag": ["JLPTN4", "noun", "adjective",...]},
        #...
    #]    