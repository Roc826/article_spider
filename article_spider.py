'''
Modified by @Galaxyzeta
1.把库换成爬虫常见库，如requests+bs4组合
2.能爬多个被选择的html部分，如糗事百科一页上的所有笑话
3.selector样例：selector={'class':'123', 'id':'haha'}
4.测试样例: http://www.lovehhy.net/Joke/Detail/QSBK/25, {"selector": "{'id':'endtext'}", "cookie": "none"}
'''
import requests
import html2text
import os
import json
import bs4
from urlparser import urlparser
from module.Printer import printer

SITE_CONFIG_PATH = './config/website/{}.json'
BASE_CONFIG_PATH = './config/base.json'

url = input(printer.prompt("请输入URL:"))
netloc = urlparser.urlparse(url)[1]
site = netloc.split(".")[-2]
siteConfigExist = 'n'
baseConfigExist = 'n'
siteConfig={
    "selector": None,
    "cookie": None
}
baseConfig={
    "path": None
}

if os.path.isfile(SITE_CONFIG_PATH.format(site)):
    siteConfigExist = input(printer.info("{}配置已存在,是否使用该配置(y/n):".format(site))).lower()
    while siteConfigExist not in ["n","y",""]:
            print(printer.error("输入错误,请重新输入"))
            siteConfigExist = input(printer.info("{}配置已存在,是否使用该配置(y/n):".format(site))).lower()
    if siteConfigExist == "" or siteConfigExist == "y":
        with open(SITE_CONFIG_PATH.format(site), "r") as file:
            siteConfig = json.load(file)

if siteConfigExist == 'n':
    selector = input(printer.prompt("请输入选择器:"))
    cookie = input(printer.prompt("请输入cookie:"))
    siteConfig={
        "selector": selector,
        "cookie": cookie
    }
    with open(SITE_CONFIG_PATH.format(site),"w") as file:
        json.dump(siteConfig, file)

session = requests.Session()
headers = {
    "cookie": siteConfig["cookie"]
}
html = session.get(url, headers=headers).content.decode("gbk")
soup = bs4.BeautifulSoup(html, "html.parser")
li = soup.findAll(attrs=eval(str(siteConfig["selector"])))
stringbuilder = ""
for i in range(len(li)):
    stringbuilder += str(li[i])

markdown = html2text.html2text(stringbuilder)

if os.path.isfile(BASE_CONFIG_PATH):
    baseConfigExist = input(printer.info("路径配置已存在,是否使用该配置(y/n):".format(site))).lower()
    while baseConfigExist not in ["n","y",""]:
            print(printer.error("输入错误,请重新输入"))
            baseConfigExist = input(printer.info("路径配置已存在,是否使用该配置(y/n):".format(site))).lower()
    if baseConfigExist == "" or baseConfigExist == "y":
        with open(BASE_CONFIG_PATH.format(site), "r") as file:
            baseConfig = json.load(file)

if baseConfigExist == "n":
    path = input(printer.prompt("请输入保存路径:")).strip("/") + "/"
    baseConfig = {
        "path": path
    }
    with open(BASE_CONFIG_PATH,"w") as file:
        json.dump(baseConfig, file)

name = input(printer.prompt("请输入保存文件名:"))
with open(baseConfig["path"]+name,"w") as file:
    file.write(markdown)

print(markdown)
