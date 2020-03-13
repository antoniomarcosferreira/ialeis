# import python libs
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request

# laws_ai libs
import laws_ai.db as db


def try_open(url, one_time=True):
    if one_time and db.link_visited(url):
        print("OBS.: The link was visited: (%s)" % url)
        return 1

    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req)
        return data
    except:
        return 0


# Return Status[T/F], Data(BeautifulSoup object), Url(String)
def open_url(url, one_time=True):
    resp = try_open(url, one_time)
    if(resp == 0):
        url = url.replace("compilado.htm", '.htm')
        resp = try_open(url, one_time)

    if(resp == 0 or resp == 1):
        return False, '',  url

    data = BeautifulSoup(resp.read(), "html.parser")

    return True, data, url

def open_htm_file(path):
    return BeautifulSoup(open(path, 'r'), "html.parser")