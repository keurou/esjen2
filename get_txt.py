import json
from traceback import print_exc
from time import sleep
import requests
from bs4 import BeautifulSoup

samplelist = ['https://www.onecareer.jp//companies/275/experiences/2022/735/510357','https://www.onecareer.jp//companies/275/experiences/2022/735/515016','https://www.onecareer.jp//companies/275/experiences/2022/735/484570']

def get_txt(samplelist):
    url_list = []
    for url in samplelist:
        #try:
        html = requests.get(url)
        html.encoding = "UTF-8"  # 日本語があってもいいよってやつ
        soup = BeautifulSoup(html.text, "html.parser")  # HTMLをとってきてsoupに入れる
        text_list = []
        for (i,j) in zip(soup.find("div", attrs={"class": "v2-curriculum-item-body__content"}).find_all("h3"),soup.find("div", attrs={"class": "v2-curriculum-item-body__content"}).find_all("p")):
            text_list.append([i,j])
        #print(text_list)
        url_list.append(text_list)
        #except:
        #    pass
    return url_list

t = get_txt(samplelist)
tmp = ""
for i in t:
    for j in i:
        #print(type(str(j[0])))
        tmp+= str(j[0]) + ","
        tmp+= str(j[1]) + "¥n"
tmp = tmp.replace('<h3>', "").replace("</h3>", "").replace("<p>", "").replace("</p>", "").replace("<br/>", "")

print(tmp)

with open("sample.txt", mode="a") as f:
    f.write(tmp)
    print("end")