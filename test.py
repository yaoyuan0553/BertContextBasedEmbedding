import torch
import math
from pytorch_pretrained_bert import BertTokenizer, BertConfig, BertEmbeddings
from pytorch_pretrained_bert import BertPreTrainedModel, BertModel
from flair.embeddings import BertEmbeddings as FlBertEmbeddings
from flair.data import Sentence
from typing import List


def cosineSimilarity(v1, v2):
    dotProduct = sum(p * q for p,q in zip(v1, v2))
    magnitude = math.sqrt(sum([val**2 for val in v1])) * math.sqrt(sum([val**2 for val in v2]))
    if not magnitude:
        return 0
    return dotProduct / magnitude


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

sortedWordSents = sorted(origWordSents, key=lambda e: len(e), reverse=True)


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


def customEmbeddingTest():
    global sortedWordSents

    bertModel = BertModel.from_pretrained('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')
    bertModel.eval()

    # sortedWordSents = sorted(origWordSents, key=lambda e: len(e), reverse=True)
    # print(sortedWordSents)
    # wordsSents = ["[CLS]" + sent + "[SEP]" for sent in origWordSents]
    # print(wordsSents)

    tokenizedSents = [tokenizer.tokenize(sent) for sent in origWordSents]
    origSentsLens = [len(sent) for sent in tokenizedSents]
    tokenizedSents = [["[CLS]"] + sent + ["[SEP]"] for sent in tokenizedSents]
    targetedWordIdxs = [sent.index('还') for sent in tokenizedSents]
    wordIdxs = [tokenizer.convert_tokens_to_ids(sent) for sent in tokenizedSents]

    #maxLen = len(wordIdxs[0])
    maxLen = max([len(sent) for sent in wordIdxs])
    paddedInputIds = [sent + [0] * (maxLen - len(sent)) for sent in wordIdxs]
    paddedInputIds = torch.tensor(paddedInputIds)

    attentionMask = torch.tensor([[float(i > 0) for i in sent] for sent in paddedInputIds])

    allLayerEmbeds, _ = bertModel(paddedInputIds, attention_mask=attentionMask,
                                  output_all_encoded_layers=True)
    with torch.no_grad():
        concatSentEmbeds = []
        layerIdxs = [-1, -2, -3, -4]
        for sentIdx, sent in enumerate(tokenizedSents):
            selectedLayersForSent = []
            for tokenIdx in range(maxLen):
                selectedLayersForToken = []
                if tokenIdx == 0 or tokenIdx == origSentsLens[sentIdx] + 1:
                    continue
                for layerIdx in layerIdxs:
                    layerEmbeds = allLayerEmbeds[layerIdx].detach().cpu()[sentIdx]
                    selectedLayersForToken.append(layerEmbeds[tokenIdx])
                selectedLayersForSent.append(torch.cat(selectedLayersForToken))
            concatSentEmbeds.append(torch.stack(selectedLayersForSent))

    return torch.stack(concatSentEmbeds)


def makeSentence(sent: str):
    sent = tokenizer.tokenize(sent)
    s = Sentence()
    for w in sent:
        s.add_token(w)
    return s


def getEmbedOfChar(sent, char):
    sent = makeSentence(sent)
    for i, t in enumerate(sent):
        if t.text == char:
            charIdx = i
            break
    return embedding.embed(sent)[0][charIdx].embedding


def getEmbedsOfChar(sents: List[str], char: str):
    sents = [makeSentence(sent) for sent in sents]
    charIdxs = []
    for sent in sents:
        for i, t in enumerate(sent):
            if t.text == char:
                charIdxs.append(i)
                break

    embeds = embedding.embed(sents)
    return [embeds[i][charIdx].embedding for i, charIdx in enumerate(charIdxs)]


def cosSim(char, sent1, sent2):
    embed1 = getEmbedOfChar(sent1, char)
    embed2 = getEmbedOfChar(sent2, char)
    # print(embed1)
    # print(embed2)
    return cosineSimilarity(embed1, embed2)


def main():
    global embedding, tokenizer
    embedding = FlBertEmbeddings('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')
    tokenizer = BertTokenizer.from_pretrained('/media/yuan/Samsung_T5/Documents/BERT/bert-base-chinese')

    customEmbeddingTest()
    # getEmbedsOfChar(origWordSents, '还')


if __name__ == "__main__":
    main()
