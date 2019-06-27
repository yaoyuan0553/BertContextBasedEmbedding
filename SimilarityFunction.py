import math


def cosineSimilarity(v1, v2):
    dotProduct = sum(p * q for p,q in zip(v1, v2))
    magnitude = math.sqrt(sum([val**2 for val in v1])) * math.sqrt(sum([val**2 for val in v2]))
    if not magnitude:
        return 0
    return dotProduct / magnitude
