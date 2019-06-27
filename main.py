"""
A program to load dictionary txt file and extract similarity between given words

Usage:
    main.py --dict-src=<file> --bert-src=<dir> [options]

Options:
    -h, --help              show this message
    --dict-src=<file>       file path to the dictionary file to be read from
    --bert-src=<dir>        directory path to pretrained BERT model used for embedding
    --layers=<list>         index/indices of the bert encoding layer to be used [default: -1,-2,-3,-4]
"""

import sys
import SimilarityFunction as sf

from docopt import docopt
from BertEmbedder import BertEmbedder
from SimilarityDictionary import *
from DictionaryLoader import DictionaryLoader


def main():
    args = docopt(__doc__)
    EmbeddingConfig.DefaultEmbedder = BertEmbedder(args['--bert-src'], args['--layers'])

    # construct and load dictionary
    embedDict = SimilarityDictionary()
    loader = DictionaryLoader(embedDict)
    loader.load(args['--dict-src'])

    print("Dictionary loaded: %s" % embedDict)

    helpMsg = 'Help:\n\t-h, --help\t\tshow this help message\n' \
        '\texit, quit\t\texit program'
    while True:
        try:
            request = input('Request format: <N> <word> [category]: ')
            if request == '-h' or request == '--help':
                print(helpMsg)
            elif request == 'exit' or request == 'quit':
                break
            else:
                wc = request.strip().split(' ')
                if len(wc) == 2:
                    key = EntryKey(wc[1])
                elif len(wc) == 3:
                    key = EntryKey(wc[1], wc[2])
                else:
                    print('wrong request format!', file=sys.stderr)
                    continue
                try:
                    sims = embedDict.getTopNWordSimilarity(int(wc[0]), key, sf.cosineSimilarity)
                except KeyError:
                    print(sys.exc_info()[1])
                    continue
                print(sims)
        except BaseException:
            print(sys.exc_info())
            continue


if __name__ == "__main__":
    main()
