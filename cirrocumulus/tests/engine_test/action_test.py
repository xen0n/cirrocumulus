#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

from nose.tools import assert_raises

from ..utils import Case, action_template, action_class

from cirrocumulus.engine import action


class TestActionModule(Case):
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_BaseAction_basic(self):
        assert action.BaseAction.abstract

        try:
            action.BaseAction(action_template('dummy'))
            assert False, 'BaseAction should not be instantiable'
        except TypeError:
            pass

    def test_BaseAction_output_var_ctor(self):
        DummyOutputVarCtorAction = action_class('dummy_out_var_ctor_1')
        template = action_template('dummy_out_var_ctor_1', 'out_var')

        obj = DummyOutputVarCtorAction(template)

        assert obj.output_var == 'out_var'

    def test_BaseAction_output_var_ctor_invalid_name(self):
        DummyOutputVarCtorAction = action_class('dummy_out_var_ctor_2')
        template = action_template('dummy_out_var_ctor_2', b'out_var')

        assert_raises(TypeError, DummyOutputVarCtorAction, template)

    def test_BaseAction_output_var_execute(self):
        class DummyOutputVarExecuteAction(action.BaseAction):
            name = 'dummy_out_var_execute'

            def _execute(self, executor, env):
                return 0, 'stored result', env

        template = action_template('dummy_out_var_execute', 'out_var')

        obj = DummyOutputVarExecuteAction(template)
        env = {}
        retcode, result, env = obj.execute(None, env)

        assert 'out_var' in env
        assert env['out_var'] == 'stored result'

    def test_MetaAction_valid_action(self):
        # should validate
        # 应该验证通过
        ValidAction = action_class('dummy1')

        assert not ValidAction.abstract

        # should instantiate successfully
        # 应该成功实例化
        ValidAction(action_template('dummy1'))

        try:
            ValidAction(action_template('dummy2'))
            assert False, 'action class instantiated with wrong action name'
        except TypeError:
            pass

        try:
            ValidAction({})
            assert False, 'action class instantiated without action name'
        except TypeError:
            pass

    def test_MetaAction_invalid_action_without_name(self):
        try:
            InvalidActionWithoutName = action_class()
            assert False, 'action class without name should not validate'
        except TypeError:
            pass

    def test_MetaAction_invalid_action_with_wrongly_typed_name(self):
        try:
            InvalidActionWithWronglyTypedName = action_class(b'illegal_name')
            assert False, (
                    'action class with wrongly typed name should not validate'
                    )
        except TypeError:
            pass

    def test_MetaAction_valid_abstract_action(self):
        # should validate
        # 应该验证通过
        ValidAbstractAction = action_class(is_abstract=True)

        assert ValidAbstractAction.abstract

        try:
            ValidAbstractAction(action_template('dummy'))
            assert False, 'abstract action class should not be instantiable'
        except TypeError:
            pass

        # test subclassing
        # 测试继承
        # should validate
        # 应该验证通过
        class ValidSubclassedAction(ValidAbstractAction):
            name = 'dummy2_1'

        assert not ValidSubclassedAction.abstract

        # should instantiate successfully
        # 应该成功实例化
        ValidSubclassedAction(action_template('dummy2_1'))

    def test_MetaAction_invalid_abstract_action_with_name(self):
        try:
            InvalidAbstractAction = action_class('dummy3', True)
            assert False, 'abstract action class with name should not validate'
        except TypeError:
            pass

    def test_create_action(self):
        Dummy3Action = action_class('dummy3')
        obj = action.create_action(action_template('dummy3'))
        assert isinstance(obj, Dummy3Action)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
