#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Output(object):
    pass


class StdoutOutput(Output):
    def __init__(self, level='info'):
        self.level = level

        if self.level == 'debug':
            print 'DEBUG: Initialized StdoutOutput'

    def send(self, key, value):
        print 'INFO: sending with key %r and value %r' % (key, value)
