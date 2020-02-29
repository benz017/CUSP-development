from .models import Events
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer as Detok


def para_splitter(para):
    tokenizer = word_tokenize(para)
    siz = int(len(tokenizer)/2)
    while tokenizer[siz-1] != '.':
        siz += 1
    detokenizer = Detok()
    para1 = detokenizer.detokenize(tokenizer[:siz])
    para2 = detokenizer.detokenize(tokenizer[siz:])
    return para1,para2
