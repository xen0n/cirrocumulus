#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

import six
import abc

from ..utils import Case

from cirrocumulus.util import compat


class TestCompatModule(Case):
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_abstractclassmethod(cls):
        class Base(six.with_metaclass(abc.ABCMeta)):
            PARAM = 2

            @compat.abstractclassmethod
            def meth(cls, spam):
                return spam + cls.PARAM

        try:
            Base()
            assert False, 'class with abstract class method instantiated'
        except TypeError:
            pass

        class Subclass(Base):
            PARAM = 3

            @classmethod
            def meth(cls, spam):
                return (super(Subclass, cls).meth(spam), spam * cls.PARAM, )

        assert Subclass.meth(3) == (6, 9, )

    def test_abstractstaticmethod(cls):
        class Base(six.with_metaclass(abc.ABCMeta)):
            @compat.abstractstaticmethod
            def meth(spam):
                return spam + 2

        try:
            Base()
            assert False, 'class with abstract static method instantiated'
        except TypeError:
            pass

        class Subclass(Base):
            @staticmethod
            def meth(spam):
                # reference to the usage of super:
                # super 用法参考:
                # http://stackoverflow.com/a/16211512/596531
                return (super(Subclass, Subclass).meth(spam), spam * 3, )

        assert Subclass.meth(3) == (5, 9, )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
