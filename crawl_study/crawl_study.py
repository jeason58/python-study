# -*- coding: utf-8 -*-

'''
    爬取豆瓣影评——《影》的所有短评
    date: 2018年9月30日18:05:03
'''

import requests
from lxml import etree
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# 影评信息类
class CommentInfo:
    def __init__(self, username=None, vote=0, comment_time=None, content=None):
        self.username = username
        self.vote = vote
        self.comment_time = comment_time
        self.content = content
        pass

    def __str__(self):
        return "username: {}\t vote: {}\t comment_time: {}\ncontent: {}\n\n"\
            .format(self.username, self.vote, self.comment_time, self.content)


# 获取看过的总人数
def get_watched_num(url=None):
    if url is None:
        return 0
    html = requests.get(url).content
    selector = etree.HTML(html)
    div = "".join(selector.xpath("//ul[@class='fleft CommentTabs']//li[1]/span/text()"))
    num_str = "".join(re.findall("\.*\d\.*", div))
    # 看过的总人数
    return int(num_str)


def get_comment_list_by_page(url):
    html = requests.get(url).content
    selector = etree.HTML(html)
    comment_item_divs = selector.xpath("//div[@class='mod-bd']/div[@class='comment-item']")
    comment_list = []
    for item_div in comment_item_divs:
        vote = "".join(item_div.xpath("./div[@class='comment']//span[@class='votes']/text()"))
        username = "".join(item_div.xpath("./div[@class='comment']/h3/span[@class='comment-info']/a[1]/text()"))
        comment_time = "".join(item_div.xpath("./div[@class='comment']/h3//span[@class='comment-time ']/text()"))
        comment_time = str.strip(comment_time)
        content = "".join(item_div.xpath("./div[@class='comment']//span[@class='short']/text()"))
        comment_info = CommentInfo(username=username, vote=vote, comment_time=comment_time, content=content)
        comment_list.append(comment_info)
        pass
    return comment_list


# 获取全部影评列表
def get_comment_list_of_all():
    base_url = "https://movie.douban.com/subject/4864908/comments?start={}&limit={}&sort=new_score&status=P&percent_type="
    start, limit = 0, 20
    start_url = base_url.format(start, limit)
    total_num = get_watched_num(start_url)
    list_of_all = []
    while start < total_num:
        url = base_url.format(start, limit)
        list = get_comment_list_by_page(url=url)
        if len(list) == 0:
            print("访问页面已达到限制页，总爬取影评数：{}".format(len(list_of_all)))
            break
        for item in list:
            list_of_all.append(item)
        # start自增20——下一页
        start += limit
    return list_of_all


# 主程序入口
if __name__ == '__main__':
    list = get_comment_list_of_all()
    filename = "./files/comments_of_ying.txt"
    with open(filename, "w+") as f:
        for info in list:
            f.write(info.__str__())
            pass
        pass
    print("crawl finished!")


