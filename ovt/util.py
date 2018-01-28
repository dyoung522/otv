__all__ = ["pluralize"]


def pluralize(count, singular, plural=None):
    if plural is None:
        plural = singular + "s"

    if count == 0:
        return "{} {}".format("no", plural)

    if count == 1:
        return "{} {}".format(count, singular)

    return "{} {}".format(count, plural)
