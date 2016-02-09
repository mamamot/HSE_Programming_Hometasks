from ComplingTokenizerSplitter import tokenizer

FINAL_PUNCT = [".", "!", "?", "…", "\n"]
ACRONYMS = list()


def load_acronyms(path):
    for ch in "АБВГДЕЖЗИКЛАМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
        ACRONYMS.append(ch)
    f = open("acronyms.txt", "r", encoding="utf-8")
    for line in f:
        ACRONYMS.append(line.strip())
    print(ACRONYMS)


def split(text):
    load_acronyms("")
    text_tokenized = tokenizer.tokenize(text, False, False, False, True)
    print(text_tokenized)
    pos = 0
    sentence_tokens = list()
    sentences = list()
    for token_pos in range(len(text_tokenized)):
        if text_tokenized[token_pos] in FINAL_PUNCT and token_pos > 0:
            if text_tokenized[token_pos - 1] not in ACRONYMS:
                if text_tokenized[token_pos] != "\n":
                    sentence_tokens.append(text_tokenized[token_pos])
                sentences.append("".join(sentence_tokens))
                sentence_tokens = list()
            else:
                sentence_tokens.append(text_tokenized[token_pos])
        else:
            sentence_tokens.append(text_tokenized[token_pos])

        pos += 1
    return sentences

if __name__ == "__main__":
    f = open("tokenizeme.txt", encoding="utf-8")
    print("\n".join(split(f.read())))


