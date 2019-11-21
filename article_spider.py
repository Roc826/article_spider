import requests_html
import html2text
import os
import json
from urlparser import urlparser
from module.Printer import printer
SITE_CONFIG_PATH = './config/website/{}.json'
BASE_CONFIG_PATH = './config/base.json'

url = input(printer.prompt("请输入URL:"))
netloc = urlparser.urlparse(url)[1]
site = netloc.split(".")[-2]
siteConfigExist = 'n'
baseConfigExist = 'n'

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

session = requests_html.HTMLSession()
headers = {
    "cookie": siteConfig["cookie"]
}
request = session.get(url, headers=headers)
a = request.html.find(siteConfig["selector"],first=True).html
markdown = html2text.html2text(a)+"\n文章来源："+request.url

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
