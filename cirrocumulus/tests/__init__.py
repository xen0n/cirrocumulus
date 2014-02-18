#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

import os

TEST_SUITE_PATH = os.path.realpath(os.path.split(__file__)[0])
REPO_PATH = os.path.abspath(os.path.join(TEST_SUITE_PATH, '../..'))


def is_travis():
    # Are we running in Travis CI environment?
    # 我们在 Travis CI 环境中吗?
    # ref. http://about.travis-ci.org/docs/user/ci-environment/
    return os.environ.get('HAS_JOSH_K_SEAL_OF_APPROVAL', None) == 'true'


def setup_package():
    os.chdir(REPO_PATH)


def teardown_package():
    pass


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
