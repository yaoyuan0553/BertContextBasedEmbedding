import torch
import sys

from typing import List, Callable, Optional
import BertEmbedder as be


class EntryValue(object):
    """
    class containing properties of a given word of a specific category (including embedding)
    """
    def __init__(self, word: str, nCats: int, exp: str, egs: List[str]):
        """
        constructs an EntryValue object
        :param word: word of the entry
        :param nCats: number of categories the word belongs to (polysemy)
        :param exp: explanation of the word
        :param egs: sample sentences that belong to this sense of the word
        """
        self.nCategory = nCats
        self.explanation = exp
        self.examples = egs
        self.embedding: torch.Tensor = be.bertEmbedder.embed(egs, word)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "EntryValue(%d, \"%s\", %s, %s)" % \
               (self.nCategory, self.explanation, self.examples, self.embedding.shape)


class EntryKey(object):
    def __init__(self, word: Optional[str] = None, category: Optional[str] = None):
        self.word = word
        self.category = category

    def isPartial(self):
        return self.word or self.category

    def isFull(self):
        return self.word and self.category

    def __str__(self):
        return "EntryKey(word: %s, category: %s)" % (self.word, self.category)

    def __repr__(self):
        return str(self)


class Entry(object):
    def __init__(self, entryKey: EntryKey, entryValue: EntryValue):
        self.key = entryKey
        self.value = entryValue

    def __str__(self):
        return "Entry[%s] = %s" % (self.key, self.value)


class EmbeddingDictionary(object):
    def __init__(self):
        self.wordEntries = dict()
        self.categoryEntries = dict()

    def add(self, entry: Entry):
        """
        Adds vocab entry to the dictionary
        :param (Entry) entry: vocab entry to be added to the dictionary
        """
        if entry.key in self:
            print('Duplicate key [%s]', entry.key, file=sys.stderr)
            return

        if entry.key.category not in self.categoryEntries.keys():
            self.categoryEntries[entry.key.category] = dict()
        if entry.key.word not in self.wordEntries.keys():
            self.wordEntries[entry.key.word] = dict()

        self.categoryEntries[entry.key.category][entry.key.word] = entry.value
        self.wordEntries[entry.key.word][entry.key.category] = entry.value

    def __setitem__(self, key, value):
        raise ValueError('forbidden to change existing entries!')

    def __getitem__(self, item: EntryKey):
        if item.category is None and item.word is None:
            raise KeyError("EntryKey cannot be None!")
        if item.category is None:
            return self.word[item.word]
        if item.word is None:
            return self.category[item.category]
        return self.category[item.category][item.word]

    def __repr__(self):
        return "EmbeddingDictionary(%d words, %d categories)" % \
               (len(self.word.keys()), len(self.category.keys()))

    def __contains__(self, item: EntryKey):
        if item.category is None and item.word is None:
            raise KeyError("EntryKey cannot be None!")
        if item.category is None:
            return item.word in self.word
        if item.word is None:
            return item.category in self.category
        return item.word in self.word and item.category in self.category

    @property
    def category(self):
        return self.categoryEntries

    @property
    def word(self):
        return self.wordEntries

    def similarity(self, key1: EntryKey, key2: EntryKey, similarityFunc: Callable):
        return similarityFunc(self.word[key1.word][key1.category].embedding,
                              self.word[key2.word][key2.category].embedding)

    def topNsimilarity(self, n: int, key: EntryKey, similarityFunc: Callable):
        if key.word is None:
            raise KeyError("EntryKey.word value must be set!")
        sims = []
