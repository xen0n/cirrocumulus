#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

__all__ = [
        'BaseAction',
        'create_action',
        ]

import six
import abc
import logging
import weakref

from ..util import compat

_ABSTRACT_ACTION_CLASSES = weakref.WeakSet()
_KNOWN_ACTIONS = {}

log = logging.getLogger(__name__)


class MetaAction(abc.ABCMeta):
    def __new__(mcs, name, bases, attrs):
        new_cls = super(MetaAction, mcs).__new__(mcs, name, bases, attrs)

        # check if we are creating some abstract action classes
        # 检查当前创建的动作类是不是定义为抽象
        try:
            is_abstract = attrs['abstract']
        except KeyError:
            is_abstract = new_cls.abstract = False

        if is_abstract:
            # indeed we are, let it go without an action name
            # any name given is an error
            # 确实是抽象动作类, 那么这个类不能定义动作名
            if new_cls.name is not None:
                log.error(
                        "abstract action class '%s' should not have"
                        " action name",
                        name,
                        )
                raise TypeError(
                        'abstract action classes must not set the'
                        ' name property'
                        )

            _ABSTRACT_ACTION_CLASSES.add(new_cls)
            log.debug("abstract action class '%s' now known", name)
            return new_cls

        # check presence and validity of action name
        # 检查动作名的存在性和有效性
        new_action_name = new_cls.name

        if new_action_name is None:
            log.error("action class '%s' has no action name", name)
            raise TypeError('name property required for action classes')

        if not isinstance(new_action_name, six.text_type):
            log.error(
                    "action class '%s' declared non-text action name %s",
                    name,
                    repr(new_action_name),
                    )
            raise TypeError(
                    'action name must be %s' % (repr(six.text_type), )
                    )

        _KNOWN_ACTIONS[new_action_name] = new_cls
        log.debug("action '%s' (class '%s') now known", new_action_name, name)

        return new_cls


def validate_action_template(template):
    try:
        act_name = template['$act']
    except KeyError:
        raise TypeError('action templates must contain action name')

    if act_name not in _KNOWN_ACTIONS:
        raise TypeError("unregistered action '%s'" % (act_name, ))


def name_from_template(template):
    return template['$act']


@six.add_metaclass(MetaAction)
class BaseAction(object):
    name = None
    abstract = True

    def __init__(self, template):
        validate_action_template(template)

        # action name consistency
        # 动作名一致性
        act_name = name_from_template(template)
        if act_name != self.name:
            raise TypeError("wrong class for action '%s'" % (act_name, ))

        params = template.copy()
        params.pop('$act')

        # result variable
        # 结果变量
        try:
            out_var = params.pop('$out')
        except KeyError:
            out_var = None

        if out_var is not None and not isinstance(out_var, six.text_type):
            raise TypeError('output variable name must be Unicode string')

        self.output_var = out_var
        self.params = params

    def __new__(cls, *args, **kwargs):
        # no instantiation of known abstract action classes allowed
        # 不允许实例化抽象动作类
        if cls in _ABSTRACT_ACTION_CLASSES:
            raise TypeError('cannot instantiate abstract action class')

        # this __new__ is type's one, which does not accept any parameter
        # 这个 __new__ 是 type 类型的, 不接受参数
        return super(BaseAction, cls).__new__(cls)

    def execute(self, executor, env):
        retcode, result, env = self._execute(executor, env)

        if self.output_var is not None:
            env[self.output_var] = result

        return retcode, result, env

    @abc.abstractmethod
    def _execute(self, executor, env):
        raise NotImplementedError


def create_action(template):
    validate_action_template(template)

    return _KNOWN_ACTIONS[template['$act']](template)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
