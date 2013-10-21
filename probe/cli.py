#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from argparse import ArgumentParser
from datetime import datetime
from dateutil.rrule import rrulestr
import os
import sys
from textwrap import dedent

from .config import ConfigHandler
from .errors import AnswerError

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

        answer = sub.add_parser(
            'answer',
            description='Answer the questions you have set up'
        )
        answer.set_defaults(func=self.answer)

        for question in self.config.questions:
            arg = answer.add_argument(
                '--%s' % question.key,
                metavar=question.key,
                help=question.hint(),
            )
            if question.type != bool:
                arg.type = question.type

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

        return CONFIG_LOCATION

    def answer(self, args):
        # answer questions
        answers = {}
        for question in self.config.questions:
            last_run = self.config.last_run.last_run(question.key)
            if last_run is not None:
                rule = rrulestr(question.interval, dtstart=last_run)
                next_run = rule.after(last_run)
                if next_run > datetime.now():
                    continue

            if getattr(args, question.key):
                try:
                    answers[question.key] = question.parse_answer(
                        getattr(args, question.key)
                    )
                except AnswerError as err:
                    print('Error in %s: %s' % (question.key, err))
                    sys.exit(1)

                continue

            while question.key not in answers:
                try:
                    answer = raw_input(question.text + ' [' + question.hint() + '] ')
                except (KeyboardInterrupt, EOFError):
                    print('Interrupting. Bye!')
                    sys.exit(1)

                try:
                    answers[question.key] = question.parse_answer(answer)
                except AnswerError as err:
                    print('Error: %s' % err)

        if not answers:
            print('No questions to answer right now. Check back later!')

        for key, answer in answers.items():
            for output in self.config.outputs:
                output.send(key, answer)

            self.config.last_run.update_last_run(key, datetime.now())

        return answers

def main():
    ProbeCLI(ConfigHandler.from_paths(
        CONFIG_LOCATION, LAST_RUN_LOCATION
    )).run(sys.argv[1:])
