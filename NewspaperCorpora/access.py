import urllib.request
import urllib.error
import urllib.parse
import os
import re
import lxml.html

uri = "http://unecha-gazeta.ru/"
agent_name = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
queue = list()
encoding = "cp1251"
dir = "dump"
relink = r'<a href=\"([^\"]*)\".*>'
revalid = r'^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$'
dump_path = "./dump/"
meta_path = "info.csv"
mystem_path = "mystem.exe"
# список разделов унеченской газеты
topics = ['main', 'vlast', 'ludi', 'kultura', 'nashi_intervu',
          'shkola', 'zdorove', 'iz_pochti', 'aktualno', 'sport', 'misc']
csv_header = "path,author,sex,birthday,header,created,sphere,genre_fi,type," \
             "topic,chronotop,style,audience_age,audience_level,audience_size,source," \
             "publication,publisher,publ_year,medium,country,region,language"

text_header = "@au Noname\n" \
              "@ti {0}\n" \
              "@da {1}\n" \
              "@topic {2}\n" \
              "@url {3}\n\n"


def classify_and_name(link):
    """
    Определить, к какому разделу относится данная статья и присвоить ей имя
    :param link:
    :return: кортеж
    """
    link = link.lstrip("http://")
    parts = link.split("/")
    if len(parts) >= 3 and parts[1] in topics:
        topic = parts[1]
    else:
        topic = 'misc'
    if parts[-1].endswith(('.html', '.htm')):
        name = urllib.parse.quote(parts[-1], safe=[])
    else:
        name = urllib.parse.quote(link, safe=[]) + '.html'
    return topic, name


def get_date(page):
    """
    Извлечь дату публикации статьи, если возможно
    :param page: текст страницы в виде строки
    :return: строка вида xx-xx-xxx
    """
    date_re = r"Добавлено: \((\d?\d-\d\d-\d\d\d\d), \d\d:\d\d\)"
    if re.search(date_re, page):
        return re.findall(date_re, page)[0]
    else:
        return "00-00-0000"


def get_header(tree):
    """
    Получить заголовок статьи.
    :param tree: lxml-дерево страницы
    :return: строка заголовка
    """
    try:
        # title = tree.xpath('.//title/text()')[0]
        # return title.split("»")[0].strip("«»")
        title = tree.xpath('.//h2/text()')[1]
        return str(title)
    except:
        return "Заголовок недоступен"


def morphanalysis(filename):
    print("Morphological analysis started: " + filename)
    os.system("{0} {1} {2} {3}".format(mystem_path, filename, filename + "_m.txt", "-e cp1251 -d -c -i"))
    os.system("{0} {1} {2} {3}".format(mystem_path, filename, filename + "_m.xml", "-e cp1251 -d -c -i --format xml"))


def load_page(url, encoding="cp1251"):
    """
    Простая функция для загрузки страницы с сайта

    :param url: URI of the page
    :param encoding: page encoding
    :return: tuple: a boolean showing success, content of the page (or error message), and http code if available (or 0)
    """
    try:
        req = urllib.request.Request(urllib.parse.quote(url, safe=":/&=?"), headers={'User-Agent': agent_name})
        with urllib.request.urlopen(req) as r:
            code = r.getcode()
            page = r.read().decode(encoding)
            loaded = True
    except urllib.error.HTTPError as e:
        page = e.reason
        code = e.code
        loaded = False
    except urllib.error.URLError as e:
        page = e.reason
        code = 0
        loaded = False
    except Exception as e:
        page = str(e)
        code = 0
        loaded = False
    return loaded, page, code


def validate_and_fix(links):
    """

    :param links:
    :return:
    """
    fixed = list()
    for link in links:
        if re.search(revalid, link):
            fixed.append(link)
    return fixed


def extract_links(tree):
    links = list()
    for a in tree.iter('a'):
        link_url = a.get('href')
        if link_url not in ["#", None]:
            links.append(a.get('href'))
    return links


def is_article(link):
    """
    Все страницы со статьями в этой газете заканчиваются на .html
    :param link:
    :return:
    """
    return link.endswith(".html")


def get_article_text(tree):
    try:
        text = tree.xpath('.//p[@class="a"]/span/text()')
        return "\n".join(text)
    except Exception as e:
        return "Текст недоступен"


def spider(queue, loc, path):
    """
    Dumps the text content of the page into a directory.

    Эта функция принимает список начальных ссылок и кортеж доменов, за пределы которых нельзя выходить, а также
    директорию, в которую помещаются скачанные html-страницы.
    :param queue: initial queue content as a list
    :param loc: a tuple of domains outside of which the spider will not dump pages
    :param path: the path to dump pages to
    :return: the number of pages dumped
    """
    csv_writer = open(os.path.join(path, meta_path), "w")
    csv_writer.write(csv_header)
    visited = list()
    visited_counter = 0
    saved_counter = 0
    while queue:
        address = queue[-1]
        print("{}. Accessing: {}".format(visited_counter + 1, address))
        loaded, page, code = load_page(address, encoding)
        visited.append(address)
        queue = queue[:-1]
        if loaded:
            tree = lxml.html.fromstring(page)
            visited_counter += 1
            topic, filename = classify_and_name(address)
            if len(filename) > 150:
                filename = filename[0:150]
            # filename = os.path.join(path, filename)
            print(classify_and_name(address))
            if is_article(address):
                article_text = get_article_text(tree)
                if article_text != "Текст недоступен":
                    date = get_date(page).split("-")
                    print("-".join(date))
                    savepath = os.path.join(path, date[2], date[1])
                    filename = os.path.join(savepath, filename) + ".txt"
                    if not os.path.exists(savepath):
                        os.makedirs(savepath)
                    with open(filename, "w", encoding="cp1251") as f:
                        print("Dumping: " + address + " to " + filename)
                        title = get_header(tree)
                        f.write(article_text)
                        saved_counter += 1
                        csv_line = '{0},,,,"{1}",{2},публицистика,,,{3},,нейтральный,н-возраст,н-уровень,районная,{4},'\
                                   '"Унечская газета",,{5},газета,Россия,ru\n'.format(filename, title, ".".join(date),
                                                                                      topic, address, date[2])
                        print(csv_line)
                        csv_writer.write(csv_line)
                        csv_writer.flush()
                    morphanalysis(filename)
                    with open(filename, "w", encoding="cp1251") as f:
                        f.write(text_header.format(title, ".".join(date), topic, address))
                        f.write(article_text)
            links = extract_links(tree)
            fixed = validate_and_fix(links)
            for link in fixed:
                if link not in visited and link not in queue:
                    if link.startswith(loc):
                        queue.append(link)
        else:
            print("Error loading page: {}: {}".format(code, page))
    csv_writer.close()
    return visited_counter, saved_counter

if __name__ == "__main__":
    # получаем локацию, чтобы не выходить за пределы
    loc = ("http://" + urllib.parse.urlparse(uri).netloc,)
    queue.append(uri)
    print("{} pages successfully dumped".format(spider(queue, loc, dump_path)))

