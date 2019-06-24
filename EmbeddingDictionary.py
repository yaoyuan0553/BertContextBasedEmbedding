from typing import List


class EntryValue(object):
    def __init__(self, nCats: int, exp: str, egs: List[str]):
        self.nCategory = nCats
        self.explanation = exp
        self.examples = egs

    def __repr__(self):
        return f"(\"{self.nCategory}\", \"{self.explanation}\", \"{self.examples}\""

    def __str__(self):
        return f"(\"{self.nCategory}\", \"{self.explanation}\", \"{self.examples}\""


class Entry(object):
    def __init__(self, word: str, category: str, entryValue: EntryValue):
        self.word = word
        self.category = category
        self.entryValue = entryValue


class EmbeddingDictionary(object):
    def __init__(self):
        self.wordEntries = dict()
        self.categoryEntries = dict()

    def add(self, entry: Entry):
        """
        Adds vocab entry to the dictionary
        :param (Entry) entry: vocab entry to be added to the dictionary
        """
        if entry.category not in self.categoryEntries.keys():
            self.categoryEntries[entry.category] = dict()
        if entry.word not in self.wordEntries.keys():
            self.wordEntries[entry.word] = dict()

        self.categoryEntries[entry.category][entry.word] = entry.entryValue
        self.wordEntries[entry.word][entry.category] = entry.entryValue
