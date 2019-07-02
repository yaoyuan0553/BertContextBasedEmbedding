from EmbeddingDictionary import EntryKey, EntryValue
from SimilarityDictionary import WordSimilarity, WordSimilarityList, CategorySimilarityDict
from Jsonifiable import JsonifiableEncoder


ws1 = WordSimilarity("哈", 0.6)
ws2 = WordSimilarity("黑", 0.3)

wsl = WordSimilarityList([ws1, ws2])

csd = CategorySimilarityDict()
csd['还'] = wsl

requestedData = dict(n=5, word="还", category="null")

ek1 = EntryKey.fromJSON(requestedData)
print(ek1)

print(ws1.toJSON())

print(wsl.tolist())
print(wsl.toJSON())

print(csd.toJSON())
