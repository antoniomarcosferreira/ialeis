# Projeto IALEIS
# Author: Antonio M. Ferreira, Feb/2020
# amfcode@gmail.com
#
# This script is used to reset processes
import laws_ai.db as db
import sys


##########################
if __name__ == "__main__":

    clear_lins = [ 
        'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/Del0200.htm',
        'http://www.planalto.gov.br/CCIVIL_03/Decreto-Lei/Del0200compilado.htm'
    ]

    for i in clear_lins:
        db.reset_link(i)

    ## Reset all links
    #db.reset_links()

    #db.reset_reads()
    
    print("Done")