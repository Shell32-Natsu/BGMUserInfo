# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import xlwt

user_id = "sample"

class animation_item:
    url = ""  # page url
    ch_name = ""  # chinese name
    jp_name = ""  # japanese_name
    score = 0.0  # score in bgm
    director = ""  # animation's director
    company = ""

    def __init__(self, u, cn):
        self.url = u
        self.ch_name = cn


def get_url_content(url):
    response = requests.get(url)
    print("URL: " + response.url)
    response.encoding = "utf-8"
    return response.text

def get_animation_info(animation):
    html_parsed = BeautifulSoup(get_url_content(animation.url), "html.parser")
    animation.score = get_animation_score(html_parsed)
    animation.director = get_animation_director(html_parsed)
    animation.company = get_animation_company(html_parsed)

def get_animation_score(html_parsed):
    return float(html_parsed.find("div", class_ = "global_score").find("span", class_ = "number").string)

def get_animation_director(html_parsed):
    return get_info_from_infobox(html_parsed, "导演")

def get_animation_company(html_parsed):
    return get_info_from_infobox(html_parsed, "动画制作")

def get_info_from_infobox(html_parsed, key_word):
    ret = ""
    tmp = html_parsed.find(id = "infobox").find("span", text = re.compile(key_word)).parent
    if tmp and tmp.string:
        ret += (tmp.string + " ")
    for i in html_parsed.find(id = "infobox").find("span", text = re.compile(key_word)).next_siblings:
        ret += i.string
    return ret

def print_animation_item_list(animation_item_list):
    n = 1
    for animation in animation_item_list:
        print(str(n) + ": ")

        print("\tURL: " + animation.url)
        print("\tCN NAME: " + animation.ch_name)
        print("\tJP NAME: " + animation.jp_name)
        print("\tSCORE: " + str(animation.score))
        print("\tDIRECTOR: " + animation.director)

        n += 1

def get_animation_item_list_info(animation_item_list):
    for animation in animation_item_list:
        get_animation_info(animation)

    # get_animation_info(animation_item_list[0])

def write_list_to_file(animation_item_list):
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Sheet1")
    # write header
    ws.write(0, 0, "BGM地址")
    ws.write(0, 1, "名称")
    ws.write(0, 2, "原名")
    ws.write(0, 3, "评分")
    ws.write(0, 4, "监督")
    ws.write(0, 5, "制作公司")

    # write data
    row = 1
    for animation in animation_item_list:
        ws.write(row, 0, animation.url)
        ws.write(row, 1, animation.ch_name)
        ws.write(row, 2, animation.jp_name)
        ws.write(row, 3, str(animation.score))
        ws.write(row, 4, animation.director)
        ws.write(row, 5, animation.company)
        row += 1
    wb.save("out.xls")



if __name__ == "__main__":
    print("ID: " + user_id)
    html_parsed = BeautifulSoup(get_url_content("http://bgm.tv/anime/list/" + user_id + "/collect"), "html.parser")
    # print("TITLE: " + html_parsed.title.string)
    item_list = []
    item_list += html_parsed.find_all("li", class_ = "item")
    pages = html_parsed.find(id = "multipage")
    pages_set = set()
    for page in pages.find_all("a"):
        pages_set.add("http://bgm.tv" + page['href'])
    # print(pages_set)

    for url in pages_set:
        html_parsed = BeautifulSoup(get_url_content(url), "html.parser")
        item_list += html_parsed.find_all("li", class_ = "item")

    animation_item_list = []
    for item in item_list:
        animation = animation_item("http://bgm.tv" + item.h3.a["href"], item.h3.a.string)
        if item.h3.small:
            animation.jp_name = item.h3.small.string
        animation_item_list.append(animation)

    print(len(animation_item_list))
    get_animation_item_list_info(animation_item_list)
    # print_animation_item_list(animation_item_list)
    write_list_to_file(animation_item_list)