import urllib.request
import urllib.error
import urllib.parse
import os
import re

uri = "http://unecha-gazeta.ru/"
name = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
visited = list()
queue = list()
encoding = "cp1251"
dir = "dump"
relink = r'<a href=\"([^\"]*)\".*>'
revalid = r'^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$'


def load_page(url, encoding="utf-8"):
    """
    A safe and simple function loading an Internet page

    :param url: URI of the page
    :param encoding: page encoding
    :return: tuple: a boolean showing success, content of the page (or error message), and http code if available (or 0)
    """
    # TODO: parse percent encoding!
    try:
        req = urllib.request.Request(url, headers={'User-Agent': name})
        with urllib.request.urlopen(req) as r:
            code = r.getcode()
            page = r.read().decode(encoding)
            loaded = True
    except urllib.error.URLError as e:
        page = e.reason
        code = 0
        loaded = False
    except urllib.error.HTTPError as e:
        page = e.reason
        code = e.code
        loaded = False
    except Exception as e:
        page = str(e)
        code = 0
        loaded = False
    return loaded, page, code


def validate_and_fix(links):
    fixed = list()
    for link in links:
        if re.match(revalid, link):
            fixed.append(link)
    return fixed


def spider(queue, visited, loc):
    while queue:
        address = queue[-1]
        print(address)
        loaded, page, code = load_page(address, encoding)
        visited.append(address)
        queue = queue[:-1]
        if loaded:
            filename = urllib.parse.quote(urllib.parse.urlparse(address).path, safe=[])
            filename = (os.path.join(dir, filename)) + ".html"
            print("Dumping: " + address + " to " + filename)
            with open(filename, "w") as f:
                f.write(page)
                links = re.findall(relink, page)
                fixed = validate_and_fix(links)
                for link in fixed:
                    if link not in visited:
                        if link.startswith(loc):
                            queue.append(link)

# получаем локацию, чтобы не выходить за пределы
loc = "http://" + urllib.parse.urlparse(uri).netloc
queue.append(uri)
spider(queue, visited, loc)
