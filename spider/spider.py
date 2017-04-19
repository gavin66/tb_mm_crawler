#! /usr/bin/env python3.6
# -*- coding: UTF-8 -*-

import urllib.request
import urllib.response
import re
import os


class Spider:
    # 页面初始化
    def __init__(self):
        self.SiteUrl = 'https://mm.taobao.com/json/request_top_list.htm'

    # 获取索引页面
    def get_page(self, page_index):
        url = self.SiteUrl + '?page=' + str(page_index)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        return response.read().decode('gbk')

    # 获取索引页所有人的信息，list 格式
    def get_contents(self, page_index):
        page = self.get_page(page_index)
        pattern = re.compile(
            '<div class="list-item".*?pic-word.*?<img src="(.*?)".*?'
            '<a class="lady-name" href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',
            re.DOTALL)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            image_url = ('http:' + item[0]).replace('_60x60.jpg', '')
            contents.append([image_url, 'http:' + item[1], item[2], item[3], item[4]])
        return contents

    # 保存头像
    def save_icon(self, icon_url, name):
        split_path = icon_url.split('.')
        f_tail = split_path.pop()
        file_name = 'image/' + name + "." + f_tail
        self.save_image(icon_url, file_name)

    # 传入图片地址，文件名，保存单张图片
    def save_image(self, image_url, file_name):
        u = urllib.request.urlopen(image_url)
        data = u.read()
        f = open(file_name, 'wb')
        f.write(data)
        f.close()

    # 创建新目录
    def mkdir(self, path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        is_exists = os.path.exists(path)
        # 判断结果
        if not is_exists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            return False

    # 将一页淘宝MM的信息保存起来
    def save_page_info(self, page_index):
        # 获取第一页淘宝MM列表
        contents = self.get_contents(page_index)
        self.mkdir('image')
        for item in contents:
            # item[0]头像URL,item[1]个人详情URL,item[2]姓名,item[3]年龄,item[4]居住地
            print(u"姓名", item[2], u"年龄", item[3], u",居住地", item[4])
            print(u"个人地址", item[1])
            print(u"头像地址", item[0])
            # 保存头像
            self.save_icon(item[0], item[2])

    def save_pages_info(self, start, end):
        for i in range(start, end + 1):
            self.save_page_info(i)


# 传入起止页码即可，在此传入了1,5,表示抓取第1到5页的MM
spider = Spider()
spider.save_pages_info(1, 5)
