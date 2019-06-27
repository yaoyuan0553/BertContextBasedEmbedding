import sys
import torch
import pytorch_pretrained_bert as ppb
from typing import Union, List, Optional, Callable
from Embedder import Embedder


class BertTokenizer(ppb.BertTokenizer):
    """
    A customized version of pytorch_pretrained_bert's BertTokenizer
    handles unknown tokens as [UNK] instead of empty string
    """
    def __init__(self, vocab_file, do_lower_case=True, max_len=None, do_basic_tokenize=True,
                 never_split=("[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]")):
        super().__init__(vocab_file, do_lower_case, max_len, do_basic_tokenize, never_split)

    def convert_tokens_to_ids(self, tokens: str):
        ids = []
        for token in tokens:
            try:
                ids.append(self.vocab[token])
            except KeyError:    # token not found in vocab
                ids.append(self.vocab['[UNK]'])     # append unknown token instead

        return ids


class BertEmbedder(Embedder):
    """
    Embedder class for embedding given sentences with BERT
    """
    def __init__(
            self, bertModelOrPath: str = "bert-base-chinese",
            layers: str = "-1, -2, -3, -4",
    ):
        """
        constructs a BertEmbedder object
        :param bertModelOrPath: bert model string or path to a bert model
        :param layers: BERT output layers to be used for embedding
        """
        self.tokenizer = BertTokenizer.from_pretrained(bertModelOrPath)
        self.model = ppb.BertModel.from_pretrained(bertModelOrPath)
        self.layerIdxs = [int(x) for x in layers.split(',')]
        self.name = str(bertModelOrPath)

        self.model.eval()

    def embed(self, sentences: Union[str, List[str]], word: Optional[str] = None):
        """
        Embed a given list of sentences with Bert
        :param (Union[str, List[str]) sentences: sentences to be embedded
        :param (str) word: if given, only the embeddings of the given word
            in each sentence will be returned
        :return (torch.Tensor): torch tensor of shape
            (number_of_sentences, max_sentence_length, bert_hidden_size)  if word is None
            (number_of_sentences, 1, bert_hidden_size) if word is given
        """
        if isinstance(sentences, str):
            sentences = [sentences]

        tokenizedSents = [self.tokenizer.tokenize(sent) for sent in sentences]
        origSentsLens = [len(sent) for sent in tokenizedSents]
        tokenizedSents = [["[CLS]"] + sent + ["[SEP]"] for sent in tokenizedSents]
        if word:
            wordLen = len(word)
            if wordLen == 1:
                try:
                    wordIdxs = [sent.index(word) for sent in tokenizedSents]
                except ValueError:
                    print(word, file=sys.stderr)
                    print(sentences, file=sys.stderr)
            else:
                charList = [char for char in word]
                wordIdxs = [i for sent in tokenizedSents for i in range(len(sent)-wordLen)
                            if sent[i:i+wordLen] == charList]

        tokenIdxs = [self.tokenizer.convert_tokens_to_ids(sent) for sent in tokenizedSents]

        maxLen = max([len(sent) for sent in tokenIdxs])
        paddedInputIds = [sent + [0] * (maxLen - len(sent)) for sent in tokenIdxs]
        paddedInputIds = torch.tensor(paddedInputIds)

        attentionMask = torch.tensor([[float(i > 0) for i in sent] for sent in paddedInputIds])

        allLayerEmbeds, _ = self.model(paddedInputIds, attention_mask=attentionMask,
                                       output_all_encoded_layers=True)
        with torch.no_grad():
            concatSentEmbeds = []
            for sentIdx, sent in enumerate(tokenizedSents):
                selectedLayersForSent = []
                if word:
                    try:
                        for tokenIdx in range(wordIdxs[sentIdx], wordIdxs[sentIdx] + len(word)):
                            selectedLayersForToken = []
                            for layerIdx in self.layerIdxs:
                                layerEmbeds = allLayerEmbeds[layerIdx].detach().cpu()[sentIdx]
                                selectedLayersForToken.append(layerEmbeds[tokenIdx])
                            selectedLayersForSent.append(torch.cat(selectedLayersForToken))
                    except IndexError:
                        print(word, file=sys.stderr)
                        print(sentences, file=sys.stderr)
                else:
                    for tokenIdx in range(maxLen):
                        selectedLayersForToken = []
                        if tokenIdx == 0 or tokenIdx == origSentsLens[sentIdx] + 1:
                            continue
                        for layerIdx in self.layerIdxs:
                            layerEmbeds = allLayerEmbeds[layerIdx].detach().cpu()[sentIdx]
                            selectedLayersForToken.append(layerEmbeds[tokenIdx])
                        selectedLayersForSent.append(torch.cat(selectedLayersForToken))
                concatSentEmbeds.append(torch.stack(selectedLayersForSent))

        return torch.stack(concatSentEmbeds)


# global variable to be initialized by main and used by other modules
# def BertEmbedderInit(bertModelOrPath: str, layers: str = "-1,-2,-3,-4"):
#     """
#     initializes a BertEmbedder global object to be used by others
#     :param (str) bertModelOrPath:
#     :param (str) layers:
#     """
#     global bertEmbedder
#     bertEmbedder = BertEmbedder(bertModelOrPath, layers)
