# -*- coding: utf-8 -*-
import os
import requests
from lxml import html

# 请求头文件
headers = {
    'Host':
    'www.zhihu.com',
    'Accept-Language':
    'zh-CN,zh;q=0.8,en;q=0.6',
    # 2017.12 经网友提醒，知乎更新后启用了网页压缩，所以不能再采用该压缩头部
    # !!!注意, 请求头部里使用gzip, 响应的网页内容不一定被压缩，这得看目标网站是否压缩网页
    # 'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Connection':
    'keep-alive',
    'Pragma':
    'no-cache',
    'Cache-Control':
    'no-cache',
    'Upgrade-Insecure-Requests':
    '1',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}


# 记录保存信息
def savetext(text):
    filename = 'temp.txt'
    file = open(filename, 'r')
    string = file.read()
    string = string + '\n'
    print(type(string.encode("utf-8")))
    # # 打开文件
    fd = os.open(filename, os.O_RDWR | os.O_CREAT)
    # 写入字符串
    os.write(fd, text + string.encode("utf-8"))
    # 关闭文件
    os.close(fd)


# 文件保存
def save(text, filename, path='download'):
    #获取path与filename组合后的路径
    fpath = os.path.join(path, filename)
    # 打开文件
    with open(fpath, 'wb') as f:
        # 打印 保存图片路径
        print('output:', fpath)
        # 写入
        f.write(text)


# 保存图片路径 调用保存函数
def save_image(image_url):
    resp = requests.get(image_url)
    page = resp.content
    filename = image_url.split('zhimg.com/')[-1]
    save(page, filename)
    savetext(image_url.encode('utf-8'))
    print(type(image_url.encode('utf-8')))


def crawl(url):
    # 请求
    resp = requests.get(url, headers=headers)
    # 获取 返回内容
    page = resp.content
    root = html.fromstring(page)
    image_urls = root.xpath('//img[@data-original]/@data-original')
    # 遍历urls
    for image_url in image_urls:
        save_image(image_url)


if __name__ == '__main__':
    url = 'https://www.zhihu.com/question/30062423'  # 有哪些「一张照片，就是一个故事」的照片？
    crawl(url)