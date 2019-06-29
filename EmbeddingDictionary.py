import sys
import torch

from typing import List, Callable, Optional
import Embedder as eb


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
