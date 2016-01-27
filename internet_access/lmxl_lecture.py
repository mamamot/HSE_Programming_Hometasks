import lxml.html
from internet_access import access

text = access.load_page("http://izvestia.ru/news/602697", "utf-8")[1]
tree = lxml.html.fromstring(text)
# получаем атрибут тега
date = tree.xpath('.//time[@itemprop="datePublished"]')[0].get('datetime')
# получаем тект внутри тега
author = tree.xpath('.//a[@itemprop="author"]/text()')[0]
# получаем все ссылки
for a in tree.iter('a'):
    print(a.get('href'))
print(date)
print(author)
