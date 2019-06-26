import math
import BertEmbedder
from EmbeddingDictionaryLoader import EmbeddingDictionaryLoader
from EmbeddingDictionary import EmbeddingDictionary, EntryKey

BertEmbedder.BertEmbedderInit('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')


def cosineSimilarity(v1, v2):
    dotProduct = sum(p * q for p,q in zip(v1, v2))
    magnitude = math.sqrt(sum([val**2 for val in v1])) * math.sqrt(sum([val**2 for val in v2]))
    if not magnitude:
        return 0
    return dotProduct / magnitude


embedDict = EmbeddingDictionary()

loader = EmbeddingDictionaryLoader(embedDict)

loader.load('d_0621.txt')

print(embedDict)

haiKey1 = EntryKey('还', '#11程度深')
haiVal1 = embedDict[haiKey1]
sims = embedDict.getTopNWordSimilarity(10, haiKey1, cosineSimilarity)
print(sims)

