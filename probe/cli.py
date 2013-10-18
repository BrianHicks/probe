#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from argparse import ArgumentParser
import os
import sys
from textwrap import dedent

from .config import ConfigHandler

CONFIG_LOCATION = os.environ.get(
    'PROBE_CONFIG', os.path.expanduser('~/.probe_config')
)
LAST_RUN_LOCATION = os.environ.get(
    'PROBE_LAST_RUN', os.path.expanduser('~/.probe_last_run')
)


class ProbeCLI(object):
    def __init__(self, config):
        self.config = config

        self.parser = ArgumentParser('probe')
        sub = self.parser.add_subparsers()

        init = sub.add_parser(
            'init',
            description='Initialize a new config in "%s" (WILL OVERWRITE)' % CONFIG_LOCATION
        )
        init.set_defaults(func=self.initialize)

    def run(self, args):
        args = self.parser.parse_args(args)
        return args.func(args)

    def initialize(self, args):
        print('Initializing sample config in %s' % CONFIG_LOCATION)
        with open(CONFIG_LOCATION, 'w') as config:
            config.write(dedent('''
                questions:
                    - sleep.hours:
                        text: How long did you sleep last night?
                        interval: every day
                        unit: hours

                    - mood.energy:
                        text: What is your energy level?
                        interval: every hour
                        unit: rating
                        lower: 0
                        upper: 10

                outputs:
                    - stdout:
                        level: info
            ''').strip())

        return args

def main():
    ProbeCLI(ConfigHandler.from_paths(
        CONFIG_LOCATION, LAST_RUN_LOCATION
    )).run(sys.argv[1:])
