#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

__all__ = [
        'Executor',
        ]

import logging

from . import constants

log = logging.getLogger(__name__)


class Executor(object):
    def __init__(self, config=None):
        pass

    def execute_actions(self, actions, env):
        results, curr_env = [], env

        for action in actions:
            log.debug('executing action %s', repr(action))
            log.debug('current env = %s', repr(curr_env))

            exitcode, result, curr_env = action.execute(self, curr_env)
            log.debug('exitcode=%d, result=%s', exitcode, repr(result))

            results.append(result)

            if exitcode == constants.ACTION_ABORT:
                log.error('action requested aborting execution')
                break

        return results, curr_env


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
