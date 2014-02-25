#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

import six
import errno
import mock

from ..utils import Case, action_template

from cirrocumulus.engine import constants
from cirrocumulus.actions import system

builtin_module_name = '__builtin__' if six.PY2 else 'builtins'


class TestSystemActions(Case):
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    @mock.patch('os.system', return_value=0)
    def test_run_cmd_simple(self, os_system):
        tmpl = action_template('run_cmd', cmd='true')
        orig_env = {}
        action = system.RunCmdAction(tmpl)

        retcode, result, env = action.execute(None, orig_env)

        os_system.assert_called_with('true')
        assert retcode == constants.ACTION_OK
        assert result == 0
        assert env == orig_env

    @mock.patch('os.chown')
    def test_chown_success(self, os_chown):
        tmpl = action_template('chown', path='test1', uid=250, gid=251)
        orig_env = {}
        action = system.ChownAction(tmpl)

        retcode, result, env = action.execute(None, orig_env)

        os_chown.assert_called_with('test1', 250, 251)
        assert retcode == constants.ACTION_OK
        assert result == (True, None, )
        assert env == orig_env

    @mock.patch('os.chown', side_effect=OSError(errno.ENOENT, ''))
    def test_chown_errno(self, os_chown):
        tmpl = action_template('chown', path='test2', uid=250, gid=251)
        orig_env = {}
        action = system.ChownAction(tmpl)

        retcode, result, env = action.execute(None, orig_env)

        os_chown.assert_called_with('test2', 250, 251)
        assert retcode == constants.ACTION_OK
        assert result == (False, 'ENOENT', )
        assert env == orig_env

    @mock.patch('os.chmod')
    def test_chmod_success(self, os_chmod):
        tmpl = action_template('chmod', path='test1', mode=0o100755)
        orig_env = {}
        action = system.ChmodAction(tmpl)

        retcode, result, env = action.execute(None, orig_env)

        os_chmod.assert_called_with('test1', 0o100755)
        assert retcode == constants.ACTION_OK
        assert result == (True, None, )
        assert env == orig_env

    @mock.patch('os.chmod', side_effect=OSError(errno.ENOENT, ''))
    def test_chmod_errno(self, os_chmod):
        tmpl = action_template('chmod', path='test2', mode=0o100755)
        orig_env = {}
        action = system.ChmodAction(tmpl)

        retcode, result, env = action.execute(None, orig_env)

        os_chmod.assert_called_with('test2', 0o100755)
        assert retcode == constants.ACTION_OK
        assert result == (False, 'ENOENT', )
        assert env == orig_env

    def test_write_file_success(self):
        tmpl = action_template(
                'write_file',
                path='target.file',
                content='content_var',
                )
        orig_env = {'content_var': 'to be written', }
        action = system.WriteFileAction(tmpl)

        mock_open = mock.mock_open()
        builtin_open_name = '%s.open' % (builtin_module_name, )

        with mock.patch(builtin_open_name, mock_open, create=True):
            retcode, result, env = action.execute(None, orig_env)

        mock_open.assert_called_with(b'target.file', 'wb')
        handle = mock_open()
        handle.write.assert_called_with(b'to be written')

        assert retcode == constants.ACTION_OK
        assert result == (True, None, )
        assert env == orig_env

    def test_write_file_nonexistent_content(self):
        tmpl = action_template(
                'write_file',
                path='target.file',
                content='nonexistent',
                )
        orig_env = {'content_var': 'to be written', }
        action = system.WriteFileAction(tmpl)

        mock_open = mock.mock_open()
        builtin_open_name = '%s.open' % (builtin_module_name, )

        with mock.patch(builtin_open_name, mock_open, create=True):
            retcode, result, env = action.execute(None, orig_env)

        assert not mock_open.called

        assert retcode == constants.ACTION_ABORT
        assert result == (False, 'EINVAL', )
        assert env == orig_env


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
