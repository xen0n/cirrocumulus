#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

__all__ = [
        'RunCmdAction',
        'ChownAction',
        'ChmodAction',
        'WriteFileAction',
        ]

import six
import os
import errno

from ..engine import constants
from ..engine import action


def desc_from_errno(code):
    return errno.errorcode[code]


class RunCmdAction(action.BaseAction):
    name = 'run_cmd'

    def _execute(self, executor, env):
        assert 'cmd' in self.params

        retcode = os.system(self.params['cmd'])

        return constants.ACTION_OK, retcode, env


class ChownAction(action.BaseAction):
    name = 'chown'

    def _execute(self, executor, env):
        assert 'path' in self.params
        assert 'uid' in self.params
        assert 'gid' in self.params

        try:
            os.chown(
                    self.params['path'],
                    self.params['uid'],
                    self.params['gid'],
                    )
        except OSError as e:
            err_desc = desc_from_errno(e.errno)
            return constants.ACTION_OK, (False, err_desc, ), env

        return constants.ACTION_OK, (True, None, ), env


class ChmodAction(action.BaseAction):
    name = 'chmod'

    def _execute(self, executor, env):
        assert 'path' in self.params
        assert 'mode' in self.params

        try:
            os.chmod(self.params['path'], self.params['mode'])
        except OSError as e:
            err_desc = desc_from_errno(e.errno)
            return constants.ACTION_OK, (False, err_desc, ), env

        return constants.ACTION_OK, (True, None, ), env


class WriteFileAction(action.BaseAction):
    name = 'write_file'

    def _execute(self, executor, env):
        assert 'path' in self.params
        assert 'content' in self.params

        content_var = self.params['content']
        if content_var not in env:
            return constants.ACTION_ABORT, (False, 'EINVAL', ), env

        content = env[content_var]

        with open(six.b(self.params['path']), 'wb') as fp:
            fp.write(six.b(content))

        return constants.ACTION_OK, (True, None, ), env


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
