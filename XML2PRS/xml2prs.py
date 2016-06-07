from lxml import etree

def xml2prs(xml_filename, prs_filename):
    with open(xml_filename, encoding="utf-8") as f:
        tree = etree.fromstring(f.read())
        sentence_count = 0
        for sentence in tree.iter('se'):
            sentence_count += 1
            for word in sentence.iter('w'):
                print(word)
                for ana in word.iter('ana'):
                    print(ana.get('lex'))

if __name__ == "__main__":
    xml2prs("example_corpus.xml", 2)