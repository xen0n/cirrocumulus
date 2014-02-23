#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

from ..utils import Case

from cirrocumulus.engine import constants


class TestConstantsModule(Case):
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_constant_values(self):
        assert constants.ACTION_OK == 0
        assert constants.ACTION_ABORT == 1


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
