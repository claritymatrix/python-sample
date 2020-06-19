import requests

from requests.exceptions import RequestException

def get_one_page(url):
;;; 缺少 headers致使被网站认为是爬虫。
    print(url)
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return reponse.text

        return None

    except RequestException:
        return None



def main():
    url = "http://maoyan.cn/board/4"
    html = get_one_page(url)

    print(html)



if __name__ == '__main__':

    main()
