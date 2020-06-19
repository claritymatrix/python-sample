import requests


def gethtmlText(url):


    try:
         r = requests.get(url,timeout = 30)

         r.raise_for_status()


         r.encoding = r.apparent_encoding

         return r.text
    except:
        return "抛出异常"


if __name__ == "__main__":
    url = "http://www.baidu.com"


    print(gethtmlText(url))
