
from typing import Union, List


class Embedder(object):
    def __init__(self):
        pass

    def embed(self, sentences: Union[str, List[str]], *args, **kwargs):
        raise NotImplementedError
