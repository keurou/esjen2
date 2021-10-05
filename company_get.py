import json
from traceback import print_exc
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import unquote


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
        company_experience_es_url = "https://www.onecareer.jp/companies/business_categories/1"
        while True:
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



if __name__ == '__main__':

    base_url = 'https://www.onecareer.jp'
    # 業界のURL
    kind_url = "https://www.onecareer.jp/companies/business_categories/1?utm_campaign=top_search&utm_medium=コンサル・シンクタンク&utm_source=oc"

    with open('config.json', mode='r') as f:
        config = json.load(f)
    urls = get_company(config, kind_url=kind_url)
    from pprint import pp
    pp(urls)


