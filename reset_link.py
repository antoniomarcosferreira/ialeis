import laws_ai.db as db
import sys


##########################
if __name__ == "__main__":


    # clear_lins = [ 
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0456.htm',
    #     'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/1965-1988/Del0398.htm'
    # ]

    # for i in clear_lins:
    #     db.reset_link(i)


    ## Reset all links
    #db.reset_links()

    db.reset_reads()
    
    print("Done")