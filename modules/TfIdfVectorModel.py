import math
from modules import InverseIndexTree as tree
from modules.PageRank import LinkProcessor


class VectorModel(LinkProcessor):
    def __init__(self):
        self.clear()

    def clear(self):
        self.documents = dict()
        self.root = tree.TernarySearchTree()

    def add(self, href, terms):
        href = self.link_processor(str(href))
        self.documents[href] = terms
        for el in terms:
            self.root.insert(el.term, href)

    def search(self, terms):
        docs = set()
        answer = {}
        term_idf = {}
        for term in terms:
            result = self.root.__contains__(term)
            if isinstance(result, list):
                term_idf[term] = math.log10(len(self.documents) / len(result))
                for el in result:
                    docs.add(el)
            else:
                term_idf[term] = 0

        for doc in docs:
            answer[doc] = list()
            for el in self.documents[doc]:
                for term in terms:
                    if el.term == term:
                        tfidf = el.tf * term_idf[term]
                        answer[doc].append([el.term, tfidf])
                        break
        ranks = []
        for doc in docs:
            sample = 0
            for el in answer[doc]:
                for term in terms:
                    if term == el[0]:
                        sample += el[1]
            ranks.append([doc, sample])
        ranks.sort(key=lambda x: x[1])
        return ranks