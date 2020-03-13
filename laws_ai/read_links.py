import laws_ai.read_page as read_page
import laws_ai.helpers as helpers
import re

def extract(data, url, condIn=''):
    # Separate links
    url_base = url.replace("http://", "")
    url_base = url_base.split("/")
    url_base.pop()

    # Remove the strike texts
    for d in data.find_all('strike'):
        d.extract()

    # Format referenced links
    links = []
    for a in data.find_all('a'):
        try:
            href = a['href']
            if 'Constituicao' in href:
                continue

            if 'ccivil' in href:
                continue

            if ('\VEP' in href) or ('/VEP' in href):
                continue

            if not re.search(r'\d', href):
                continue

            if condIn:
                if not condIn in href:
                    continue

            if not ('.htm' in href):
                continue

            if '?OpenDocument' in href:
                continue

            if not ("http" in href):
                href = helpers.apply_path_url(url_base, href)

            href = href.split("#")[0]
            links.append(href)
        except:
            continue

    links = list(filter(None, links))
    links = list(dict.fromkeys(links))

    return links


def links_in_link(link):
    _ok, data, url = read_page.open_url(link)
    return extract(data, url)
