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
from flask import Flask, request
from flask_cors import CORS
from EmbeddingDictionary import EmbeddingConfig, EmbeddingDictionary, EntryKey
from DictionaryLoader import DictionaryLoader
from BertEmbedder import BertEmbedder
from SimilarityDictionary import SimilarityDictionary
from SimilarityFunction import cosineSimilarity
from Jsonifiable import JsonifiableEncoder

app = Flask(__name__)
cors = CORS(app, resources={r"/similarity_ranker": {"origins": "*"}})


@app.route("/similarity_ranker", methods=["POST"])
def main():
    response = dict()
    try:
        requestedJson = request.get_json()
        if not requestedJson:
            return "Invalid Requested Data"

        requestInfo = requestedJson.get('request_info', False)
    except Exception:
        return "Invalid Requested Data"
    try:
        if requestInfo:
            response['info'] = dict()
            response['info']['words'] = list(embedDict.word.keys())
            response['info']['categories'] = list(embedDict.category.keys())

        else:
            entryKey = EntryKey.fromJSON(requestedJson)
            n = requestedJson.get("n")
            n = None if n == "null" else n
            simRanks = simDict.rankedSimilarity(entryKey, top=n)

            response['sim_ranks'] = simRanks

        response = json.dumps(response, ensure_ascii=False,
                              cls=JsonifiableEncoder).encode('utf-8')

        # response = json.dumps({
        #     "sim_ranks": str(simRanks)
        # }, ensure_ascii=False).encode('utf-8')
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
