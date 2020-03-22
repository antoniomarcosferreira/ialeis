# Projeto IALEIS
# Author: Antonio M. Ferreira, Feb/2020
# amfcode@gmail.com

import re


def only_numbers(text):
    return ''.join(re.findall('\d+', text))


def clean_text(text):
    text = text.translate(text.maketrans("\n\t\r", "   "))
    return " ".join(text.split())


def apply_path_url(path, url):
    url_arr = url.split("../")
    new_path = []
    max_i = len(path) - (len(url_arr)-1)
    count_i = 0
    for i in path:
        if count_i < max_i:
            new_path.append(i)
        count_i = count_i + 1
    new_path = "/".join(new_path)
    new_path = "http://" + new_path + "/" + url_arr[-1]
    return new_path


def clean_list(items):
    items = list(filter(None, items))
    return list(dict.fromkeys(items))
