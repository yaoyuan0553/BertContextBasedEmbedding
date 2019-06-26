from EmbeddingDictionary import *


class EmbeddingDictionaryLoader(object):
    def __init__(self, embedDict: EmbeddingDictionary):
        """
        constructs a loader
        :param (EmbeddingDictionary) embedDict: saved for later use
        """
        self.embedDict = embedDict

    def load(self, path: str):
        """
        reads file and constructs an EmbeddingDictionary
        :param (str) path: path to file
        """
        with open(path, 'rb') as f:
            lines = f.read().decode('utf-8').splitlines()

        curCategory = None
        for l in lines:
            if l[0] == '#':
                curCategory = l
            else:
                try:
                    w, n, exp, egs = l.split('-')
                    egs = egs.split('+')
                except ValueError:  # skip cases with wrong format
                    continue
                if curCategory is None:
                    raise ValueError("Current Category not found in file!")
                try:
                    entry = Entry(EntryKey(w, curCategory), EntryValue(w, int(n), exp, egs))
                # TODO: deal with unexpected inputs
                except Exception:
                    continue    # skip this line if an error happened
                self.embedDict.add(entry)
