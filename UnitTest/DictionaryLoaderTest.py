import math
from BertEmbedder import BertEmbedder
from DictionaryLoader import DictionaryLoader
from EmbeddingDictionary import *
import numpy as np

# BertEmbedder.BertEmbedderInit('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')

# EmbeddingConfig.DefaultEmbedder = BertEmbedder('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')

def cosineSimilarity(v1, v2):
    dotProduct = sum(p * q for p,q in zip(v1, v2))
    magnitude = math.sqrt(sum([val**2 for val in v1])) * math.sqrt(sum([val**2 for val in v2]))
    if not magnitude:
        return 0
    return dotProduct / magnitude


# embedDict = EmbeddingDictionary()
#
# loader = DictionaryLoader(embedDict)
#
# loader.load('d_0626.txt')
#
# print(embedDict)
#
# haiKey1 = EntryKey('还', )
# haiVal1 = embedDict[haiKey1]
# sims = embedDict.getTopNWordSimilarity(10, haiKey1, cosineSimilarity)
# print(sims)

ws1 = WordSimilarity('哈哈', 0.75)
ws2 = WordSimilarity('嘿嘿', 0.3)
print(ws1)
print(ws2)

wsl = WordSimilarityList()
# wsl.append(ws1)
wsl = np.append(wsl, ws1)

wsl = np.append(wsl, ws2)

rankDict = SimilarityDictionary()
rankDict['blah'] = wsl
print(rankDict)
