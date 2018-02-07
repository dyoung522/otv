import colorama as color
import os
import platform
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


def usage(help_message, error_message=None, pause=False):
    if error_message is not None:
        print(color.Fore.LIGHTRED_EX + "!!! {} !!!".format(error_message) + os.linesep, file=sys.stderr)

    print(help_message)

    if pause or (platform.system() == "Windows"):
        input(os.linesep + "Press ENTER key to exit")

    sys.exit(255)
