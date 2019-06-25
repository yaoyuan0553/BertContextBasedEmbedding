import BertEmbedder
from EmbeddingDictionaryLoader import EmbeddingDictionaryLoader
from EmbeddingDictionary import EmbeddingDictionary

BertEmbedder.BertEmbedderInit('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')

embedDict = EmbeddingDictionary()

loader = EmbeddingDictionaryLoader(embedDict)

loader.load('d_0621.txt')

print(embedDict)
