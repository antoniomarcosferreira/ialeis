import laws_ai.read_page as read_page
import laws_ai.db as db
import laws_ai.error as error
import laws_ai.read_links as read_links

import os
import time


def get_page(url):
    start_time = time.time()
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        ok, data, url = read_page.open_url(url, True)
        law_code = db.link_to_law_code(url)

        if not ok:
            db.link_readed_with_error(url, "Cant read law")
            return ['error', "Cant read law"] 

        # Separate links
        links = read_links.extract(data, url)

        path_file = path + "/../laws/" + law_code + ".htm"

        f = open(path_file, "w+")
        f.write(str(data))
        f.close

        time_used = (time.time() - start_time)

        db.link_readed(url, law_code, time_used)

        for link in links:
            db.add_link(link, law_code, 0)

        return ["ok", path_file]

    except Exception as e:
        db.link_readed_with_error(url, str(e))
        return ['error', str(e)]
