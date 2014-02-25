#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

__all__ = [
        'Case',
        'action_template',
        'action_class',
        ]

from ..engine import action


class Case(object):
    pass


def action_template(name, out_var=None, **kwargs):
    kwargs['$act'] = name

    if out_var is not None:
        kwargs['$out'] = out_var

    return kwargs


def action_class(action_name=None, is_abstract=False):
    class GeneratedActionClass(action.BaseAction):
        if action_name is not None:
            name = action_name

        if is_abstract:
            abstract = True

        def _execute(self, executor, env):  # pragma: no cover
            return 0, None, env

    return GeneratedActionClass


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
