import BertEmbedder
from SimilarityDictionary import *

BertEmbedder.BertEmbedderInit('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')

# 还-6-表示在某种程度之上有所增加或在某个范围之外有所补充-
# 今天比昨天还冷。
# +场上的麦子堆得比小山还高。
# +他比他哥哥还壮。
# +新车间比旧车间还大一百平方米。
# +那种微型电池比这个纽扣还小一些。
# +他比你还小好几岁呢。
examples = [
    "今天比昨天还冷。",
    "场上的麦子堆得比小山还高。",
    "他比他哥哥还壮。",
    "新车间比旧车间还大一百平方米。",
    "那种微型电池比这个纽扣还小一些。",
    "他比你还小好几岁呢。"
]

entryValue1 = EntryValue("还", 6, "表示在某种程度之上有所增加或在某个范围之外有所补充", examples)
entryKey1 = EntryKey("还", "#11程度深")
entry1 = Entry(entryKey1, entryValue1)

embedDict = SimilarityDictionary()
embedDict.add(entry1)

print(entry1)
print(embedDict)
print(entryKey1.isFull(), entryKey1.isEmpty())
