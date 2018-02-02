import colorama as color
import sys

__all__ = ["pluralize", "usage"]


def pluralize(count, singular, plural=None):
    if plural is None:
        plural = singular + "s"

    if count == 0:
        return "{} {}".format("no", plural)

    if count == 1:
        return "{} {}".format(count, singular)

    return "{} {}".format(count, plural)


def usage(help_message, error_message=""):
    if error_message != "": print(color.Fore.RED + color.Style.BRIGHT + f"!!! {error_message} !!!\n", file=sys.stderr)
    print(help_message)

    sys.exit(255)
