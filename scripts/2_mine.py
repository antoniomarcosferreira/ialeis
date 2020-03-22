# Projeto IALEIS
# Author: Antonio M. Ferreira, Feb/2020
# amfcode@gmail.com
#
# Read the laws files from the laws folder,
# Separate information and save to mongodb collections

import laws_ai.mine as mine
import laws_ai.db as db
import sys
import time
import glob
import os
import laws_ai.read_page as read_page


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    limit = 1500
    count = 0

    def mine_pages():
        global count

        os.chdir(path + "/../laws")
        for file in glob.glob("*.htm"):
            law_path = path + "/../laws/" + file

            try:
                law_path_processing = path + "/../laws/processing/" + file
                os.rename(law_path, law_path_processing)

                try:
                    law_path_filtered = path + "/../laws/filtered/" + file
                    law_code = file.split(".htm")[0]
                    mine_law = mine.Mine(law_path_processing, law_code)
                    mine_law.extract_data(True)
                    print(count, "Ok =>", file)
                    os.rename(law_path_processing, law_path_filtered)
                except Exception as _e:
                    print(count, "Erro ->", file)
                    law_path_error = path + "/../laws/errors/" + file
                    os.rename(law_path_processing, law_path_error)

            except Exception as _e:
                print('has already been copied by another process')

            count += 1
            if count >= limit:
                break

    mine_pages()
