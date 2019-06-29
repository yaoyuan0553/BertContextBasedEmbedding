import sys
import numpy as np

from typing import List, Callable, Optional, Tuple, Sequence
from collections import UserDict
from EmbeddingDictionary import EntryKey, EntryValue, EmbeddingDictionary


class WordSimilarity(object):
    def __init__(self, word: str, similarityScore: float):
        if not isinstance(word, str) or not isinstance(similarityScore, float):
            raise TypeError('WordSimilarity expects (str, float), but got (%s, %s)' % \
                            (type(word), type(similarityScore)))
        self._word = word
        self._similarityScore = similarityScore

    @property
    def word(self):
        return self._word

    @property
    def similarity(self):
        return self._similarityScore * 100

    def __str__(self):
        return "\"%s\": %.2f%%" % (self.word, self.similarity)

    def __repr__(self):
        return "WordSimilarity(%s, %.2f)" % (self.word, self._similarityScore)

    def __lt__(self, other):
        return self.similarity < other.similarity


class WordSimilarityList(np.ndarray):

    def __new__(cls, inputArray):
        obj = np.asarray(inputArray).view(cls)
        return obj

    def sortBySimilarity(self, reverse=False):
        if reverse:
            self[::-1].sort()
        else:
            self.sort()

        return self

    def stringify(self, strFormat: str, start: Optional[int] = None, end: Optional[int] = None):
        """
        stringify the list in given format and range [start, end)
        :param (str) strFormat: format to print each element
        :param (int) start: start index of element to be printed (inclusive)
        :param (int) end: end index of element to be printed (exclusive)
        :return (str): stringified list
        """
        start = 0 if start is None else start
        end = len(self) if end is None else end
        ret = ""
        for i in range(start, start + end):
            if not isinstance(self[i], WordSimilarity):
                raise TypeError('WordSimilarityList expects element type WordSimilarity, '
                                'but got %s' % type(self[i]))
            ret += strFormat % (i+1, self[i])
        ret = ret[:-1]  # ignore the additional ending format
        return ret

    def __str__(self):
        return self.stringify("%d. %s\n")
        # ret = ""
        # for i, ws in enumerate(self):
        #     if not isinstance(ws, WordSimilarity):
        #         raise TypeError('WordSimilarityList expects element type WordSimilarity, '
        #                         'but got %s' % type(ws))
        #     ret += "%d. %s\n" % (i+1, ws)
        # ret = ret[:-1]
        # return ret

    # def __repr__(self):
    #     return 'WordSimilarityList(%s)' % super().__repr__()


class CategorySimilarityDict(UserDict):
    def stringify(self, strFormat):
        ret = ""
        for cat, simList in self.items():
            ret += strFormat % (cat, simList.stringify("\t%d. %s\n"))

        return ret[:-1]

    def __str__(self):
        return self.stringify("%s:\n%s\n")

    def __repr__(self):
        return "CategorySimilarityDict(%s)" % super().__repr__()


class SimilarityDictionary(object):
    def __init__(self, embedDict: EmbeddingDictionary,
                 similarityFunction: Callable[[Sequence, Sequence], float]):
        """
        :param embedDict: a reference to initialized an EmbeddingDictionary object
        :param similarityFunction: function to compute similarity with
        """
        self._embedDict = embedDict
        self._simFunc = similarityFunction
        self._data = dict()

    def __contains__(self, item: EntryKey):
        if not isinstance(item, EntryKey):
            raise TypeError('SimilarityDictionary expects type EntryKey as key, '
                            'but got %s' % type(item))
        if item.isEmpty() or item.word is None:
            raise KeyError("EntryKey.word must be set!")
        if item.category is None:
            return item.word in self._data
        return item.word in self._data and item.category in self._data[item.word]

    def __str__(self):
        ret = ""
        for word in self._data.keys():
            ret += "%s:\n" % word
            for cat, simList in self._data[word].items():
                ret += "\t%s:\n%s\n" % (cat, simList.stringify('\t\t%d. %s\n'))
            # ret += "%s:\n%s\n" % (key, self.data[key].stringify('\t%d. %s\n'))
        return ret[:-1]

    @property
    def embedDict(self):
        return self._embedDict

    @embedDict.setter
    def embedDict(self, newDict: EmbeddingDictionary):
        if self._embedDict is newDict:
            return
        if not isinstance(newDict, EmbeddingDictionary):
            raise TypeError("expects ")
        print("[INFO] SimilarityDictionary dictionary changed, clearing similarity data",
              file=sys.stderr)
        self._data.clear()      # clears data as new dict is used and old data should be nullified
        self._embedDict = newDict

    @property
    def similarityFunction(self):
        return self._simFunc

    @similarityFunction.setter
    def similarityFunction(self, newSimFunc):
        if self._simFunc is newSimFunc:
            return
        print("[INFO] SimilarityDictionary similarity function changed, "
              "clearing similarity data", file=sys.stderr)
        self._data.clear()
        self._simFunc = newSimFunc

    def similarityBetweenWords(self, key1: EntryKey, key2: EntryKey) -> float:
        if not key1.isFull() or not key2.isFull():
            raise ValueError("EntryKeys must be full (both word and category provided)")
        return self._simFunc(self.embedDict[key1].embedding, self.embedDict[key2].embedding)

    def similarityInCategory(self, key: EntryKey, forceUpdate=False) -> WordSimilarityList:
        if not key.isFull():
            raise ValueError("EntryKey must be fully set!")
        # if the similarity for this word in this category is not computed,
        # compute
        if forceUpdate or key not in self:
            val: EntryValue = self.embedDict[key]
            otherVals: List[Tuple[str, EntryValue]] = \
                [(w, v) for w, v in self.embedDict.category[key.category].items()
                 if w != key.word]

            if key.word not in self._data:
                self._data[key.word] = CategorySimilarityDict()
            self._data[key.word][key.category] = WordSimilarityList(
                [WordSimilarity(w, self._simFunc(val.embedding, v.embedding))
                 for w, v in otherVals]
            )
        return self._data[key.word][key.category]

    def similarity(self, key: EntryKey, forceUpdate=False):
        if key.isEmpty() or key.word is None:
            raise ValueError("EntryKey.word must be set!")
        simsByCat = CategorySimilarityDict()
        if key.category is None:
            for cat in self.embedDict[key].keys():
                simsByCat[cat] = self.similarityInCategory(EntryKey(key.word, cat), forceUpdate)
        else:
            simsByCat[key.category] = self.similarityInCategory(key, forceUpdate)
        return simsByCat

    def rankedSimilarity(self, key: EntryKey, top: Optional[int] = None,
                         bottom: Optional[int] = None, forceUpdate=False):
        if key.isEmpty() or key.word is None:
            raise ValueError("EntryKey.word must be set!")
        simsByCat = self.similarity(key, forceUpdate)
        if top is not None and bottom is not None:
            raise ValueError("parameters top and bottom are mutually exclusive")
        for cat in simsByCat.keys():
            if top:
                simsByCat[cat] = simsByCat[cat].sortBySimilarity(reverse=True)[:top]
            elif bottom:
                simsByCat[cat] = simsByCat[cat].sortBySimilarity(reverse=True)[bottom:]
            else:
                simsByCat[cat] = simsByCat[cat].sortBySimilarity(reverse=True)

        return simsByCat
