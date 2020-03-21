# Baixa arquivos hml conforme os links baixados no script 0_find_links.py
# Salva as páginas na pasta laws
# Também mapea links dentro das páginas baixadas.

import laws_ai.copy as copy
import laws_ai.db as db
import sys
import time

if __name__ == "__main__":
    limit = 500
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
