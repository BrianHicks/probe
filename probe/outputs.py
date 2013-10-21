#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
try: # make it optional!
    from tempodb import Client, DataPoint
except ImportError:
    pass

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


class TempoDBOutput(Output):
    def __init__(self, **tempo_kwargs):
        # imported here to make this optional
        print tempo_kwargs
        self.client = Client(**tempo_kwargs)

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def send(self, key, value):
        self.client.write_key(
            key,
            [DataPoint(datetime.now(), value)]
        )
