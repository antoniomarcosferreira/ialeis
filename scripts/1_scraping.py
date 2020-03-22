# Projeto IALEIS
# Author: Antonio M. Ferreira, Feb/2020
# amfcode@gmail.com
#
# Scraping
# Download hml files according to the links
#  downloaded in the 0_crawling.py script
# Save the pages in the laws folder
# It also maps links within downloaded pages.

import laws_ai.copy as copy
import laws_ai.db as db
import sys
import time

if __name__ == "__main__":
    limit = 100
    count = 0

    def getLinks():
        global count

        links = db.unread_links(limit)

        for link in links:
            count = count + 1
            res = copy.get_page(link["url"])
            print(count, res, link["url"])
            time.sleep(0.5)

    getLinks() 
