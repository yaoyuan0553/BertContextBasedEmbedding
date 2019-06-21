import torch
import math
from torch.optim import Adam
from pytorch_pretrained_bert import BertTokenizer, BertConfig, BertEmbeddings
from pytorch_pretrained_bert import BertPreTrainedModel
from pytorch_pretrained_bert import BertForTokenClassification, BertAdam
from tqdm import tqdm
from typing import List


def cosineSimilarity(v1, v2):
    dotProduct = sum(p*q for p,q in zip(v1, v2))
    magnitude = math.sqrt(sum([val**2 for val in v1])) * math.sqrt(sum([val**2 for val in v2]))
    if not magnitude:
        return 0
    return dotProduct/magnitude


origWordSents = [
    "今天比昨天还冷。",
    "那条蛇比碗口还粗。",
    "屋子不大，收拾得倒还干净。",
    "半夜了，他还在工作。",
    "劳动力还不够，必须再调一部分人过来。",
    "都十二点了，你还说早？",
    "想不到还有这等事！",
    "（这学期）他比你跑得还快了。",
]


class BertPreTrainedEmbeddings(BertPreTrainedModel):
    def __init__(self, config: BertConfig):
        super().__init__(config)
        self.embeddings = BertEmbeddings(config)

    def forward(self, inputIds: List[List[int]]):
        """
        :param (List[List[int]]) inputIds: list of sentences containing
            word ids of dim [batchSize, sequenceLength]
        :return (List[List[int]]): list of sentences of words of embeddings
            of size [batchSize, sequenceLength, embeddingSize]
        """
        maxLen = len(inputIds[0])
        paddedInputIds = [sent + [0] * (maxLen - len(sent)) for sent in inputIds]
        paddedInputIds = torch.tensor(paddedInputIds)
        return self.embeddings(paddedInputIds)


tokenizer = BertTokenizer.from_pretrained('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')
model = BertPreTrainedEmbeddings.from_pretrained('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')

sortedWordSents = sorted(origWordSents, key=lambda e: len(e), reverse=True)
print(sortedWordSents)

tokenizedSents = [tokenizer.tokenize(sent) for sent in sortedWordSents]
targetedWordIdxs = [sent.find('还') for sent in sortedWordSents]
wordIdxs = [tokenizer.convert_tokens_to_ids(sent) for sent in tokenizedSents]
sentsEmbeds = model(wordIdxs)
print(targetedWordIdxs)
# print([wordIdxs[i][j] for i, j in enumerate(targetedWordIdxs)])
print(sortedWordSents[0])
print(tokenizedSents[0])
# print(sentsEmbeds[-1][targetedWordIdxs[-1]])
# print(sentsEmbeds[-3][targetedWordIdxs[-3]])

v1 = 2
v2 = -2
print(sortedWordSents[v1])
print(sortedWordSents[v2])
print(cosineSimilarity(
    sentsEmbeds[v1][targetedWordIdxs[v1]],
    sentsEmbeds[v2][targetedWordIdxs[v2]]))
# print(tokenized_texts[0])


# if __name__ == "__main__":
#     main()
