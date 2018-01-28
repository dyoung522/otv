__all__ = ["pluralize"]


def pluralize(count, singular, plural):
    if count == 0:
        return "{} {}".format("no", plural)

    if count == 1:
        return "{} {}".format(count, singular)

    return "{} {}".format(count, plural)
