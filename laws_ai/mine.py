import re
from datetime import datetime
import laws_ai.read_page as read_page
import laws_ai.helpers as helpers
import laws_ai.db as db
import laws_ai.find_authors as find_authors
import os
import json

path = os.path.dirname(os.path.abspath('app'))


class Mine:
    def __init__(self, path, law_code, log=True, save=True):
        self.pattern = re.compile(
            "\d{1,2} (jan(eiro)?|fev(ereiro)?|mar(ço)?|abr(il)?|mai(o)|jun(ho)?|jul(ho)?|ago(sto)?|set(embro)?|out(ubro)?|nov(embro)?|dez(embro)?) \d{4}")
        self.months = {'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04',
                       'mai': '05', 'jun': '06', 'jul': '07', 'ago': '08',
                       'set': '09', 'out': '10', 'nov': '11', 'dez': '12'}
        self.path = path
        self.law_code = law_code
        self.save = save
        self.log = log
        self.current_published_at = ''
        self.current_law_id = ''
        link = db.link_by_law_code(law_code)
        self.current_link_id = link["_id"]
        self.current_text_id = ''
        self.current_table_id = ''

        self.preamble = ""
        self.description = ""

        self.published_at = None

    def clean_text(self, text):
        text = " ".join(text.split()).lower()
        text = re.sub('<[^>]+>', '', text)
        text = text.split("(function")[0]
        return text

    def set_preamble(self, text):
        ret = ''
        text = self.clean_text(text)
        text = text.replace("decreta:", ":")
        text = text.replace("decreto:", ":")
        text = text.split(":")[0]
        text_splited = text.split("presidente da república")
        if len(text_splited) > 1:
            ret = "presidente da república" + text_splited[1]
        return ret

    def set_description(self, text):
        ret = ''
        text = self.clean_text(text)
        text = text.replace(" no ", " nº ")
        text = text.split(" nº ")[1:-1]
        text = " nº ".join(text)
        text = text.split()[7:-1]
        text = " ".join(text)
        #text = " ".join(" ".join(text[1:-1]).split()[6:-2])
        text_splited = text.split("presidente da república")
        text_splited = ".".join(text_splited[0].split(".")[0:-1])
        if len(text_splited) > 0:
            ret = text_splited
        return ret

    def law_type_date_scope(self, text):
        scope = ''
        text = self.clean_text(text)
        text = text.replace(" no ", " nº ")
        text = text.split(" nº ")
        if 'presidência da república' in text[0]:
            scope = 'federal'

        law_type = text[0].split()[-1]
        date = text[1]
        date = date.replace("º", "")
        date = date.replace(" de ", " ").split()
        date = helpers.only_numbers(
            date[3]) + '-' + self.months[date[2][:3]] + '-' + date[1]

        return law_type, date, scope

    def extract_tables(self, all_data, indent=None):
        tables = all_data.find_all("table")

        all_tables = []

        for table in tables:
            rows = table.find_all("tr")
            headers = {}

            thead = table.find("thead")
            if thead:
                thead = thead.find_all("th")
                for i in range(len(thead)):
                    headers[i] = thead[i].text.strip().lower()
            data = []
            for row in rows:
                cells = row.find_all("td")
                if thead:
                    items = {}
                    for index in headers:
                        items[headers[index]] = cells[index].text
                else:
                    items = []
                    for index in cells:
                        text = index.text.strip()
                        text = text.replace("\n", " ")
                        text = " ".join(text.split())
                        items.append(text)
                data.append(items)
            tb_data = json.dumps(data, indent=indent, ensure_ascii=False)
            all_tables.append(tb_data)

        return all_tables

    def law_texts(self, itens, save=False):
        article = 0
        last_article = 0
        chapter = ''
        last_chapter = ''
        paragraph = ''
        last_paragraph = ''
        item = ''
        last_item = ''
        point = ''
        last_point = ''

        for p in itens:
            if p == "" or p == "*" or len(p) < 15:
                continue

            extinct = False
            if re.findall('revogado', p.lower()):
                extinct = True

            # -- Find the chapter
            if(re.findall('CAPÍTULO*...........', p)):
                chapter = re.findall(
                    'CAPÍTULO*...........', p)[0].split(" ")[1]
                if(last_chapter != chapter):
                    last_chapter = chapter
                    article = article + 1
                    last_article = ''
                    last_paragraph = ''
                    last_item = ''
                    last_point = ''

            # -- Find the article
            if(re.findall("Art", p)):
                i = re.findall(r'\d+', p)
                if i:
                    article = int(i[0])
                    if(last_article != article):
                        last_article = article
                        last_paragraph = ''
                        last_item = ''
                        last_point = ''

            # -- define paragraphs
            if(re.findall('§ *...........', p)):
                paragraph = int(re.findall(r'\d+', p)[0])
                if(last_paragraph != paragraph):
                    last_paragraph = paragraph
                    last_item = ''
                    last_point = ''

            # -- define items
            if(re.findall(r"[MDCLXVI] -", p)):
                item = p.split(" - ")[0]
                item = item.replace("(Vigência) ", "")
                item = item.split(" ")[0]
                if(last_item != item):
                    last_item = item
                    last_point = ''

            # -- define alínea
            if(re.findall(r"[)] ", p[0:8])):
                point = p[0:8].split(") ")[0]
                if(last_point != point):
                    last_point = point

            if len(p) < 75 or p.lower() == self.description.lower() or p.lower == self.preamble.lower():
                continue

            data_text = {
                'law_code': self.law_code, 'published_at': self.published_at,
                'chapter': chapter, 'article': article,
                'paragraph': paragraph, 'item': item,
                'point': point, 'text': p, 'extinct': extinct
            }

            current_text_id = ''

            if save:
                current_text_id = db.add_text(data_text)

                # -- Add item form Fact
                fact = {
                    'law': self.current_law_id,
                    'link': self.current_link_id,
                    'text': current_text_id,
                    'date': self.current_published_at,
                    'table': self.current_table_id
                }
                db.add_published_fact(fact)

    def extract_data(self, save=False):
        scope = ""
        effective_at = None
        scope = ""

        data = read_page.open_htm_file(self.path)

        for strike in data.findAll("strike"):
            strike.extract()

        law_type, self.published_at, scope = self.law_type_date_scope(
            data.text)

        all_tables = self.extract_tables(data)
        self.description = self.set_description(data.text)
        self.preamble = self.set_preamble(data.text)

        # LIMPEZA
        for table in data.findAll("table"):
            table.extract()

        for footer in data.findAll("footer"):
            footer.extract()

        for br in data.find_all("br"):
            br.replace_with("\n")

        text = data.text
        text = text.split("(function")[0]

        authors = find_authors.authors(text)

        # filters
        if len(authors) == 0 or len(authors[0]) < 5 or len(authors[0]) > 60:
            raise 'Erro na identificação do author'

        if len(self.preamble) < 20 or len(self.preamble) > 500:
            raise 'Erro na identificação do preamble'

        if len(self.description) < 20 or len(self.description) > 500:
            raise 'Erro na identificação do descrição'
       
        text = text.replace("\xa0", " ")
        text = text.replace("\n\n\n", "|")
        text = text.replace("\n\n", "|")
        text = text.replace("Art. ", "|Art. ")
        text = text.replace("\n", " ")
        text = " ".join(text.split())

        reduce_text = text.split("República")
        reduce_text = reduce_text[:-1]
        text = " ".join(reduce_text) + " República"

        items = helpers.clean_list(text.split("|"))

        cleaned_items = []
        for i in items:
            if '<!--' in i:
                continue

            cleaned_items.append(i)

        items = cleaned_items

        if effective_at == None:
            effective_at = self.published_at

        published_at_arr = self.published_at.split("-")

        law_date = {
            "_id": self.published_at,
            'year': int(published_at_arr[0]),
            'month': int(published_at_arr[1]),
            'day': int(published_at_arr[2]),
            'date': datetime.strptime(self.published_at, "%Y-%m-%d")
        }

        law = {
            'law_code': self.law_code, 'published_at': self.published_at,
            'effective_at': effective_at, 'law_type': law_type,
            'scope': scope, 'description': self.description,
            'preamble': self.preamble, 'authors': authors
        }

        if save:
            self.current_published_at = db.add_date(law_date)
            self.current_law_id = db.add_law(law)
            if len(all_tables) > 0:
                data_table = {
                    'law_code': self.law_code,
                    'tables': all_tables
                }
                self.current_table_id = db.add_tables(data_table)

        self.law_texts(items, save)

        return law
