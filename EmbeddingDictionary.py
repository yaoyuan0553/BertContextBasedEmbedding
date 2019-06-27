import torch
import sys

from typing import List, Callable, Optional, Tuple, Sequence
from collections import UserDict, UserList
import Embedder as eb
from BertEmbedder import BertEmbedder


class EmbeddingConfig(object):
    """
    configuration variables for embedding and pooling in EntryValue;
    must be modified before initializing an EntryValue
    """
    WordPoolingMethod: Callable = torch.mean
    SentencePoolingMethod: Callable = torch.mean
    DefaultEmbedder: eb.Embedder = eb.Embedder()


def PoolWord(t: torch.Tensor, dim: int):
    """
    Method to aggregate embeddings of a multi-character word into one
    :param (torch.Tensor) t: torch tensor containing embeddings of characters
    :param (int) dim: dimension of characters to be pooled over
    :return torch.Tensor: aggregated embedding of the word (character dimension will be discarded)
    """
    return EmbeddingConfig.WordPoolingMethod(t, dim=dim)


def PoolSentence(t: torch.Tensor, dim):
    """
    Method to aggregate embeddings of a given word within multiple sentences
    :param (torch.Tensor) t: torch tensor containing embeddings of characters
    :param (int) dim: dimension of characters to be pooled over
    :return torch.Tensor: aggregated embedding of the word (character dimension will be discarded)
    """
    return EmbeddingConfig.SentencePoolingMethod(t, dim=dim)


class EntryValue(object):
    """
    class containing properties of a given word of a specific category (including embedding)
    """
    def __init__(self, word: str, nCats: int, exp: str, egs: List[str], prop: Optional[str] = None):
        """
        constructs an EntryValue object
        :param (str) word: word of the entry
        :param (int) nCats: number of categories the word belongs to (polysemy)
        :param (str) exp: explanation of the word
        :param (List[str]) egs: sample sentences that belong to this sense of the word
        :param (Optional[str]) prop: property (part of speech) of the word
        """
        self.nCategory = nCats
        self.explanation = exp
        self.examples = egs
        self.property = prop
        self.embedding: torch.Tensor = PoolSentence(
            PoolWord(EmbeddingConfig.DefaultEmbedder.embed(egs, word), dim=1), dim=0)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "EntryValue(%s, \"%s\", %s, %s)" % \
               (str(self.nCategory), self.explanation, self.examples, self.embedding.shape)


class EntryKey(object):
    def __init__(self, word: Optional[str] = None, category: Optional[str] = None):
        """
        constructs an EntryKey object
        :param (Optional[str]) word: word to be stored & indexed with
        :param (Optional[str]) category: category to be stored & indexed with
        """
        self.word = word
        self.category = category

    def isEmpty(self):
        """
        :return (bool): True if both fields are None, False otherwise
        """
        return self.word is None and self.category is None

    def isFull(self):
        """
        :return (bool): True if both fields are filled, False otherwise
        """
        return self.word is not None and self.category is not None

    def __str__(self):
        return "EntryKey(word: %s, category: %s)" % (self.word, self.category)

    def __repr__(self):
        return str(self)


class Entry(object):
    def __init__(self, entryKey: EntryKey, entryValue: EntryValue):
        """
        constructs an Entry object
        :param (EntryKey) entryKey: entry key
        :param (EntryValue) entryValue: entry value
        """
        self.key = entryKey
        self.value = entryValue

    def __str__(self):
        return "Entry[%s] = %s" % (self.key, self.value)


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


class WordSimilarityList(UserList):
    def __init__(self, data: Optional[Sequence] = None):
        super().__init__(data)

    def sortBySimilarity(self, reverse=False) -> None:
        self.data = sorted(self.data, key=lambda e: e.similarity, reverse=reverse)

    def sortByWord(self, reverse=False):
        self.data = sorted(self.data, key=lambda e: e.word, reverse=reverse)

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
        return self.stringify("%d. %s")
        # ret = ""
        # for i, ws in enumerate(self):
        #     if not isinstance(ws, WordSimilarity):
        #         raise TypeError('WordSimilarityList expects element type WordSimilarity, '
        #                         'but got %s' % type(ws))
        #     ret += "%d. %s\n" % (i+1, ws)
        # ret = ret[:-1]
        # return ret

    def __repr__(self):
        return 'WordSimilarityList(%s)' % super().__repr__()


class SimilarityRankingDict(UserDict):
    def __setitem__(self, key: str, value: WordSimilarityList):
        if not isinstance(key, str) or not isinstance(value, WordSimilarityList):
            raise TypeError('SimilarityRanking expects (key, value) type: '
                            '(str, WordSimilarityList), '
                            'but got type: (%s, %s)' % (type(key), type(value)))
        super().__setitem__(key, value)

    def __str__(self):
        ret = ""
        for key in self.keys():
            # ret += "%s:\n\t%s\n" % (key, '\n\t'.join(str(self[key]).splitlines()))
            ret += "%s:\n%s\n" % (key, self[key].stringify('\t%d. %s\n'))
        return ret[:-1]


class EmbeddingDictionary(object):
    def __init__(self):
        """
        initializes an EmbeddingDictionary
        """
        self.wordEntries = dict()
        self.categoryEntries = dict()

    def add(self, entry: Entry):
        """
        Adds vocab entry to the dictionary
        :param (Entry) entry: vocab entry to be added to the dictionary
        """
        if entry.key in self:
            print('Duplicate key [%s]' % entry.key, file=sys.stderr)
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
        """
        :param (EntryKey) item: lookup with key and returns an EntryValue
        :return (Union[EntryValue, Dict[str, EntryValue]]): returns a single EntryValue
            if it's a full-lookup (EntryKey is fully filled). Otherwise, returns a dictionary
            of either category or word as keys and EntryValue as values
        """
        if item.isEmpty():
            raise KeyError("EntryKey cannot be empty!")
        if item.category is None:
            return self.word[item.word]
        if item.word is None:
            return self.category[item.category]
        if item not in self:
            raise KeyError('%s not found!' % item)
        return self.category[item.category][item.word]

    def __repr__(self):
        return "EmbeddingDictionary(%d words, %d categories)" % \
               (len(self.word.keys()), len(self.category.keys()))

    def __contains__(self, item: EntryKey):
        """
        check whether not an EntryKey exists within the dictionary
        :param (EntryKey) item: item to be checked
        :return (bool): True or False
        """
        if item.isEmpty():
            raise KeyError("EntryKey cannot be empty!")
        if item.category is None:
            return item.word in self.word
        if item.word is None:
            return item.category in self.category
        return item.word in self.word and item.category in self.word[item.word]

    @property
    def category(self):
        """
        name alias for categoryEntries
        :return:
        """
        return self.categoryEntries

    @property
    def word(self):
        """
        name alias for wordEntries
        :return:
        """
        return self.wordEntries

    def similarity(self, key1: EntryKey, key2: EntryKey, similarityFunc: Callable):
        """
        computes similarity score of two entries
        :param (EntryKey) key1:
        :param (EntryKey) key2:
        :param Callable similarityFunc:
        :return (Container[float]): similarity score
        """
        if not key1.isFull() or not key2.isFull():
            raise KeyError("EntryKeys must be full (both word and category provided)")

        return similarityFunc(self[key1].embedding, self[key2].embedding)

    def getWordSimilarityInCategory(self, key: EntryKey, similarityFunc: Callable):
        """
        computes similarity score between given key.word and all other words within
        the same category
        :param (EntryKey) key:
        :param (Callable) similarityFunc:
        :return (List[Container[float]]): list of similarity scores
        """
        if not key.isFull():
            raise KeyError("EntryKey must be fully set!")
        val: EntryValue = self[key]
        otherVals: List[Tuple[str, EntryValue]] = \
            [(w, v) for w, v in self.category[key.category].items() if w != key.word]
        return WordSimilarityList(
            [WordSimilarity(w, similarityFunc(val.embedding, v.embedding).item())
                for w, v in otherVals])

    def getWordSimilarity(self, key: EntryKey, similarityFunc: Callable):
        """
        computes similarity score between key.word and all other words spanning all
        categories that key.word is in
        :param (EntryKey) key:
        :param (Callable) similarityFunc:
        :return (Dict[str, List[Container[float]]]):
        """
        if key.word is None:
            raise KeyError("EntryKey.word value must be set!")
        simsByCategory: SimilarityRankingDict = SimilarityRankingDict()
        if key.category:
            simsByCategory[key.category] = self.getWordSimilarityInCategory(key, similarityFunc)
        else:
            categories = self[key]
            for cat in categories.keys():
                simsByCategory[cat] = \
                    self.getWordSimilarityInCategory(EntryKey(key.word, cat), similarityFunc)
        return simsByCategory

    def getOrderedSimilarityForWord(self, key: EntryKey, similarityFunc: Callable):
        """
        computes similarity score with getWordSimilarity function and pick the top N
        words with the highest similarity score
        :param (int) n:
        :param (EntryKey) key:
        :param (Callable) similarityFunc:
        :return (Dict[str, List[Container[float]]]): sorted top N words with
            high similarity score for each category
        """
        simsByCategory: SimilarityRankingDict = self.getWordSimilarity(key, similarityFunc)
        for sims in simsByCategory.values():
            sims.sortBySimilarity(reverse=True)
            # simsByCategory[cat] = sorted(sims, key=lambda e: e[1], reverse=True)[:n]

        return simsByCategory

