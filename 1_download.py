# Baixa arquivos hml conforme os links baixados no script 0_find_links.py
# Salva as páginas na pasta laws
# Também mapea links dentro das páginas baixadas.

import laws_ai.copy as copy
import laws_ai.db as db
import sys
import time


##########################
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

    # db.reset_links()
    getLinks()

    # itens = [
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0555.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del1685.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del1682.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/_Ato2019-2022/2019/Decreto/D10102.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/_Ato2019-2022/2019/Decreto/D10179.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/Del0278.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/Del0073.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0164.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0208impressao.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0067.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0055impressao.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0456.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del1295.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del1554.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/Del0900.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/Del0799.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0561.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0376.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0355.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1937-1946/Del0300impresssao.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0055.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0244.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0398.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del1106.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0414.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/Del0509.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0456.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0398.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/Del0200.htm'
    # ]

    # for i in itens:
    #     copy.get_page(i)

    # res = copy.get_page(i)
    # print(res)

    # i = "http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del1871.htm"
    # db.reset_link(i)
    # res = copy.get_page(i)
    # print(res)
