#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

import six
import abc


class BaseRecipe(six.with_metaclass(abc.ABCMeta)):
    def __init__(self):
        pass

    @abc.abstractmethod
    def describe_plan(self):
        return []


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
