"""
ServerDeployer: deploy word similarity ranker with flask

Usage:
    ServerDeployer.py --dict-src=<file> --bert-src=<dir> [options]

Options:
    -h, --help              show this message
    --dict-src=<file>       file path to the dictionary file to be read from
    --bert-src=<dir>        directory path to pretrained BERT model used for embedding
    --layers=<list>         index/indices of the bert encoding layer to be used [default: -1,-2,-3,-4]
"""

import sys
import json

from docopt import docopt
from flask import Flask
from flask import request
from EmbeddingDictionary import EmbeddingConfig, EmbeddingDictionary, EntryKey
from DictionaryLoader import DictionaryLoader
from BertEmbedder import BertEmbedder
from SimilarityDictionary import SimilarityDictionary
from SimilarityFunction import cosineSimilarity

app = Flask(__name__)


@app.route("/similarity_ranker", methods=["POST"])
def main():
    try:
        requestedJson = request.get_json()
        if not requestedJson:
            return "Invalid Requested Data"
        n = requestedJson.get("n")
        word = requestedJson.get("word")
        category = requestedJson.get("category")
        entryKey = EntryKey(word, category)
    except Exception:
        return "Invalid Requested Data"
    try:
        simRanks = simDict.rankedSimilarity(entryKey, top=n)
        response = json.dumps({
            "sim_ranks": str(simRanks)
        }, ensure_ascii=False).encode('utf-8')
        # print(simRanks)
    except (KeyError, ValueError) as e:
        response = json.dumps({"error": "%s" % sys.exc_info()[1]})

    print(response)
    return response


if __name__ == "__main__":
    global embedDict, simDict
    args = docopt(__doc__)
    EmbeddingConfig.DefaultEmbedder = BertEmbedder(args['--bert-src'], args['--layers'])
    embedDict = EmbeddingDictionary()
    loader = DictionaryLoader(embedDict)
    loader.load(args['--dict-src'])
    simDict = SimilarityDictionary(embedDict, cosineSimilarity)

    app.run(port=5001)
