

class EntryValue(object):
    def __init__(self, nCats, exp, eg):
        self.nCategory = nCats
        self.explanation = exp
        self.example = eg

    def __repr__(self):
        return f"(\"{self.nCategory}\", \"{self.explanation}\", \"{self.example}\""

    def __str__(self):
        return f"(\"{self.nCategory}\", \"{self.explanation}\", \"{self.example}\""


class EmbeddingDictionary(object):
    def __init__(self):
        self.wordEntries = dict()
        self.categoryEntries = dict()
