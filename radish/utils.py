# -*- coding: utf-8 -*-

"""
    This module provides several utility functions
"""

import os
import re
import sys
import fnmatch
import traceback
import warnings

from .compat import u


class Failure(object):  # pylint: disable=too-few-public-methods
    """
        Represents the fail reason for a step
    """
    def __init__(self, exception):
        """
            Initalizes the Step failure with a given Exception

            :param Exception exception: the exception shrown in the step
        """
        self.exception = exception
        self.reason = u(str(exception))
        self.traceback = u(traceback.format_exc())
        self.name = exception.__class__.__name__
        traceback_info = traceback.extract_tb(sys.exc_info()[2])[-1]
        self.filename = traceback_info[0]
        self.line = int(traceback_info[1])


def console_write(text):
    """
        Writes the given text to the console

        If the --no-colors flag is given all colors are removed from the text
    """
    print(text)


def expandpath(path):
    """
        Expands a path

        :param string path: the path to expand
    """
    return os.path.expanduser(os.path.expandvars(path))


def recursive_glob(root, pattern):
    """
        Recursively search for files with given pattern inside a path

        :param str root: the root location to start search
        :param str pattern: to pattern to look for. It's matched against the filenames under `root`.

        :rtype: list
        :returns: A list of matching files
    """
    matches = []
    for root, dirnames, filenames in os.walk(root):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


def get_debugger():
    """
        Returns a debugger instance
    """
    try:
        from IPython.core.debugger import Pdb
        pdb = Pdb()
    except ImportError:
        try:
            from IPython.Debugger import Pdb
            from IPython.Shell import IPShell

            IPShell(argv=[""])
            pdb = Pdb()
        except ImportError:
            warnings.warn('pdb was selected as a debugger. If you want to use ipython as a debugger you have to "pip install radish-bdd[ipython-debugger]"')
            import pdb

    return pdb


def datetime_to_str(datetime):
    """
        Returns the datetime object in a defined human readable format.

        :param Datetime datetime: the datetime object
    """
    if not datetime:
        return ""

    return datetime.strftime("%Y-%m-%dT%H:%M:%S")


def get_width(data):
    """
        Returns the needed width for a data column

        :param list data: a column with data
    """
    return max(len(x) for x in data)


def make_unique_obj_list(somelist, attr):
    """
        Make list with objects unique
        according to an objects attribute.
    """
    tmp = {}
    for item in somelist:
        tmp[attr(item)] = item
    return tmp.values()


def get_func_code(func):
    """
        Get the code object for the given function.
    """
    if sys.version_info[0] == 3:
        return func.__code__
    else:
        return func.func_code


def get_func_arg_names(func):
    """
        Get the argument names of the given function.
    """
    return get_func_code(func).co_varnames


def get_func_location(func):
    """
        Get the location where the given function is implemented.
    """
    func_code = get_func_code(func)
    return '{0}:{1}'.format(func_code.co_filename, func_code.co_firstlineno)


def str_lreplace(pattern, replacement, string, escape_pattern=False, flags=0):
    """
    Only replace the pattern with replacement
    if the string starts with the pattern.
    """
    if escape_pattern:
        pattern = re.escape(pattern)

    return re.sub(r'^{0}'.format(pattern), replacement, string, flags=flags)
