#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

__all__ = [
        'abstractclassmethod',
        'abstractstaticmethod',
        ]

import abc

# for abc.abstract{class,static}method in Python 2.x
# The following code is taken directly from Python 3.3 stdlib, with minor
# modification to make it Py2-compatible. The original code is licensed under
# the PSF license.
#
### START OF PYTHON STDLIB CODE
class abstractclassmethod(classmethod):
    """
    A decorator indicating abstract classmethods.

    Similar to abstractmethod.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractclassmethod
            def my_abstract_classmethod(cls, ...):
                ...

    'abstractclassmethod' is deprecated. Use 'classmethod' with
    'abstractmethod' instead.
    """

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)


class abstractstaticmethod(staticmethod):
    """
    A decorator indicating abstract staticmethods.

    Similar to abstractmethod.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractstaticmethod
            def my_abstract_staticmethod(...):
                ...

    'abstractstaticmethod' is deprecated. Use 'staticmethod' with
    'abstractmethod' instead.
    """

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractstaticmethod, self).__init__(callable)


### END OF PYTHON STDLIB CODE


# Always prefer the stdlib version, even if they are actually the same.
# 即使完全一样, 也总是优先使用标准库里的实现
try:
    abstractclassmethod = abc.abstractclassmethod
except AttributeError:
    pass

try:
    abstractstaticmethod = abc.abstractstaticmethod
except AttributeError:
    pass


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
