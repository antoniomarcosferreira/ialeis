# Lê os arquivos de leis da pasta laws,
# Separa as informações e salva em coleções no mongodb

import laws_ai.mine as mine
import laws_ai.db as db
import sys
import time 
import glob, os
import laws_ai.read_page as read_page



##########################
if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    limit = 1000
    count = 0

    def mine_pages():
        global count

        os.chdir(path + "/laws")
        for file in glob.glob("*.htm"):

            law_path = path + "/laws/" + file
            try:
                law_path_filtered = path + "/laws/filtered/" + file
                law_code = file.split(".htm")[0]
                mine_law = mine.Mine(law_path, law_code)
                ret = mine_law.extract_data(True)
                print(count, "Ok =>", file)
                os.rename(law_path, law_path_filtered)
            except Exception as e:
                print(count, "Erro ->", file)
                law_path_error = path + "/laws/errors/" + file
                os.rename(law_path, law_path_error)  

            count  += 1
            if count >= limit:
                break

    mine_pages()
  