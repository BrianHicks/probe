#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Output(object):
    pass


class StdoutOutput(Output):
    def __init__(self, level='info'):
        self.level = level

        if self.level == 'debug':
            print 'DEBUG: Initialized StdoutOutput'

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.level)

    def send(self, key, value):
        print 'INFO: sending with key %r and value %r' % (key, value)
