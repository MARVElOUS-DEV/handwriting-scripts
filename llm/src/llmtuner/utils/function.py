
import math


def get_perplexity(loss):
    if loss is None:
        return None

    try:
        perplexity = math.exp(loss)
        perplexity = float(perplexity)
    except OverflowError:
        perplexity = float("inf")

    return perplexity
