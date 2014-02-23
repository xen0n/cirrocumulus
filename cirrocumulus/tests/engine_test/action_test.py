#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

from ..utils import Case

from cirrocumulus.engine import action


class TestActionModule(Case):
    @classmethod
    def setup_class(cls):
        make_template = lambda name: {'$act': name, }

        cls.dummy_template = make_template('dummy')
        cls.dummy1_template = make_template('dummy1')
        cls.dummy2_template = make_template('dummy2')
        cls.dummy2_1_template = make_template('dummy2_1')
        cls.invalid_template = {}

    @classmethod
    def teardown_class(cls):
        pass

    def test_BaseAction(self):
        assert action.BaseAction.abstract

        try:
            action.BaseAction(self.dummy_template)
            assert False, 'BaseAction should not be instantiable'
        except TypeError:
            pass
        except:  # pragma: no cover
            raise

    def test_MetaAction_valid_action(self):
        try:
            class ValidAction(action.BaseAction):
                name = 'dummy1'

                def execute(self, executor, env):  # pragma: no cover
                    return 0, None, env
        except:  # pragma: no cover
            assert False, 'correctly declared action class does not validate'

        assert not ValidAction.abstract

        try:
            ValidAction(self.dummy1_template)
        except:  # pragma: no cover
            assert False, 'concrete action class failed to instantiate'

        try:
            ValidAction(self.dummy2_template)
            assert False, 'action class instantiated with wrong action name'
        except TypeError:
            pass

        try:
            ValidAction(self.invalid_template)
            assert False, 'action class instantiated without action name'
        except TypeError:
            pass

    def test_MetaAction_invalid_action_without_name(self):
        try:
            class InvalidActionWithoutName(action.BaseAction):
                def execute(self, executor, env):  # pragma: no cover
                    return 0, None, env

            assert False, 'action class without name should not validate'
        except TypeError:
            pass
        except:  # pragma: no cover
            raise

    def test_MetaAction_invalid_action_with_wrongly_typed_name(self):
        try:
            class InvalidActionWithWronglyTypedName(action.BaseAction):
                name = b'illegal_name'

                def execute(self, executor, env):  # pragma: no cover
                    return 0, None, env

            assert False, (
                    'action class with wrongly typed name should not validate'
                    )
        except TypeError:
            pass
        except:  # pragma: no cover
            raise

    def test_MetaAction_valid_abstract_action(self):
        try:
            class ValidAbstractAction(action.BaseAction):
                abstract = True

                def execute(self, executor, env):  # pragma: no cover
                    return 0, None, env
        except:  # pragma: no cover
            assert False, (
                    'correctly declared abstract action class does not'
                    ' validate'
                    )

        assert ValidAbstractAction.abstract

        try:
            ValidAbstractAction(self.dummy_template)
            assert False, 'abstract action class should not be instantiable'
        except TypeError:
            pass
        except:  # pragma: no cover
            raise

        # test subclassing
        # 测试继承
        try:
            class ValidSubclassedAction(ValidAbstractAction):
                name = 'dummy2_1'
        except:  # pragma: no cover
            assert False, (
                    'correctly declared action subclass does not validate'
                    )

        assert not ValidSubclassedAction.abstract

        try:
            ValidSubclassedAction(self.dummy2_1_template)
        except TypeError:  # pragma: no cover
            assert False, 'action subclass failed to instantiate'

    def test_MetaAction_invalid_abstract_action_with_name(self):
        try:
            class InvalidAbstractAction(action.BaseAction):
                name = 'dummy3'
                abstract = True

                def execute(self, executor, env):  # pragma: no cover
                    return 0, None, env

            assert False, 'abstract action class with name should not validate'
        except TypeError:
            pass
        except:  # pragma: no cover
            raise



# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
