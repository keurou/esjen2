import json
from traceback import print_exc
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
from pprint import pp
from tqdm import tqdm

def get_company(config: dict, kind_url: str) -> list:
    driver = webdriver.Chrome('./chromedriver')
    try:
        driver.get(f'{base_url}/users/sign_in')

        for k, v in config.items():
            driver.find_element_by_id(f'user_{k}').send_keys(v)

        # ログイン
        driver.find_element_by_xpath('//*[@id="new_user"]/input[2]').click()

        if input('start?: [(y/)n]').lower() == 'n': return
        driver.get(kind_url)
        #
        # # ES・体験談
        # es_url = driver.find_element_by_xpath('//*[@id="company-nav"]/div[3]/a').get_attribute('href')
        # driver.get(es_url)
        #
        # base_xpath_format = '//*[@id="body"]/div[1]/div[6]/div/div[1]/form/div/div[{}]/label[{}]'.format
        # # 本選考
        # driver.find_element_by_xpath(base_xpath_format(1, 2)).click()
        # # ES
        # driver.find_element_by_xpath(base_xpath_format(3, 1)).click()
        # # 絞り込む
        # driver.find_element_by_xpath('//*[@id="body"]/div[1]/div[6]/div/div[1]/form/div/input').click()
        urls = []
        page = 0
        company_experience_es_url = kind_url
        while page < 2:
            page += 1
            sleep(1)

            # print("=" * 30)
            # print(f"{company_experience_es_url}" + "?page=" f"{page}")
            # print("=" * 30)

            driver.get(f"{company_experience_es_url}" + "?page=" f"{page}")
            # print(f'{unquote(driver.current_url)=}')
            print(f'{len(urls)=}')

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            experiences = soup.find_all('li', class_='v2-companies__item')
            # print(experiences)
            # print(urls)
            if len(experiences) > 0:
                urls += [
                        f'{base_url}/{tmp.find("a")["href"]}'
                        for tmp in experiences
                    ]
            else:
                break

        driver.quit()

    except:
        driver.quit()
        print_exc()

        return []

    else:
        return urls

def get_all_urls(config: dict, company_url_list) -> list:
    driver = webdriver.Chrome('./chromedriver')
    urls2 = []
    try:
        driver.get(f'{base_url}/users/sign_in')

        for k, v in config.items():
            driver.find_element_by_id(f'user_{k}').send_keys(v)
        # ログイン
        driver.find_element_by_xpath('//*[@id="new_user"]/input[2]').click()

        # if input('start?: [(y/)n]').lower() == 'n': return
        for company_url in tqdm(company_url_list):
            driver.get(company_url)
            # ES・体験談
            es_url = driver.find_element_by_xpath('//*[@id="company-nav"]/div[3]/a').get_attribute('href')
            driver.get(es_url)

            base_xpath_format = '//*[@id="body"]/div[1]/div[6]/div/div[1]/form/div/div[{}]/label[{}]'.format
            # 本選考
            driver.find_element_by_xpath(base_xpath_format(1, 2)).click()
            # ES
            driver.find_element_by_xpath(base_xpath_format(3, 1)).click()
            # 絞り込む
            driver.find_element_by_xpath('//*[@id="body"]/div[1]/div[6]/div/div[1]/form/div/input').click()

            page = 0
            company_experience_es_url = driver.current_url
            while True:
                page += 1
                sleep(1)
                driver.get(f'{company_experience_es_url}&page={page}')
                # print(f'{unquote(driver.current_url)=}')
                # print(f'{len(urls)=}')

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                experiences = soup.find_all('div', class_='v2-experience')
                # print(len(experiences))
                if len(experiences) > 0:
                    urls2 += [
                            f'{base_url}/{div.find("a")["href"]}'
                            for div in experiences
                        ]
                else:
                    break

        driver.quit()

    except:
        driver.quit()
        print_exc()

        return []

    else:
        return urls2

def get_txt(samplelist):
    url_list = []
    for url in tqdm(samplelist):
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

if __name__ == '__main__':

    base_url = 'https://www.onecareer.jp'

    with open('config.json', mode='r') as f:
        config = json.load(f)

    # 業界のURL 1がコンサルで２が．．．
    kind_url = "https://www.onecareer.jp/companies/business_categories/1"
    urls = get_company(config, kind_url=kind_url)

    pp("=" * 50)
    pp(urls)
    pp("=" * 50)

    urls2 = get_all_urls(config, urls)

    pp("="*50)
    print("all_urls")
    pp(urls2)
    pp("=" * 50)

    # urls2 = ['https://www.onecareer.jp//companies/275/experiences/2022/735/510357',
    #               'https://www.onecareer.jp//companies/275/experiences/2022/735/515016',
    #               'https://www.onecareer.jp//companies/275/experiences/2022/735/484570']

    t = get_txt(urls2)
    tmp = ""
    for i in tqdm(t):
        for j in i:
            # print(type(str(j[0])))
            # tmp += str(j[0]) + ","
            tmp += str(j[1]) + "\n"
    tmp = tmp.replace('<h3>', "").replace("</h3>", "").replace("<p>", "").replace("</p>", "").replace("<br/>", "")
    #print(tmp)
    with open("sample3.txt", mode="a") as f:
        f.write(tmp)
        print("end")