from bs4 import BeautifulSoup
import re
import requests

def spider():
    url = "http://www.lovehhy.net/Joke/Detail/QSBK/25"
    resp = requests.Session().get(url=url)
    html = resp.content.decode("gbk")
    magic_soup = BeautifulSoup(html, "html.parser")
    li = magic_soup.findAll(attrs={'id':'endtext'})
    count = 0
    if li is not None:
        for subli in li:
            print(str(count)+":")
            print(subli)
            count+=1
    else:
        print('None')

if __name__ == "__main__":
    spider()