# Projeto IALEIS
# Author: Antonio M. Ferreira, Feb/2020
# amfcode@gmail.com
#
# Crawling
# This script creates links from the main government pages.
# Just map links and save.
# Currently maps only Decrees, Complementary Laws and Ordinary Laws

import laws_ai.db as db
import sys
import datetime
import laws_ai.read_page as read_page
import laws_ai.read_links as read_links

import time


def find(url_base):
    _ok, data, url = read_page.open_url(url_base)
    links = read_links.extract(data, url)
    for i in links:
        links = read_links.links_in_link(i)
        print(i, "- ", len(links), " links")
        for link in links:
            db.add_link(link, '', 0)

        time.sleep(0.5)

    print("__END__")


if __name__ == "__main__":

    # Apenas decretos e leis ordinárias.
    base_urls = [
        "http://www.planalto.gov.br/CCIVIL_03/decreto/_Dec_ano.htm",
        "http://www.planalto.gov.br/ccivil_03/LEIS/_Lei-Ordinaria.htm"
        "http://www.planalto.gov.br/ccivil_03/LEIS/LCP/Quadro_Lcp.htm"
    ]

    for i in base_urls:
        find(i)
