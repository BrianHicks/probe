#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import shelve
import yaml

from . import questions
from . import outputs


class LastRun(object):
    def __init__(self, path):
        self.path = path
        store = shelve.open(path)

    def last_run(self, key):
        s = shelve.open(self.path)
        try:
            return s[key]
        except KeyError:
            return None
        finally:
            s.close()

    def update_last_run(self, key, value):
        s = shelve.open(self.path)
        try:
            s[key] = value
        finally:
            s.close()

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.path)


class ConfigHandler(object):
    @classmethod
    def from_paths(cls, config_path, last_run_path):
        try:
            with open(config_path, 'r') as c:
                config = c.read()
        except IOError:
            config = ''

        last_run = LastRun(last_run_path)

        return cls(config, last_run)

    def __init__(self, config_text, last_run):
        self.config = yaml.safe_load(config_text) or {}

        # dehydrate questions
        self.questions = map(
            self.parse_question, self.config.get('questions', [])
        )
        self.outputs = map(
            self.parse_output, self.config.get('outputs', [])
        )
        self.last_run = last_run

    def parse_question(self, question):
        unit = question.values()[0].get('unit', 'number')
        units = {
            'hours': questions.HoursQuestion,
            'rating': questions.RatingQuestion,
            'number': questions.NumberQuestion,
            'yesno': questions.YesNoQuestion,
        }
        return units[unit](question)

    def parse_output(self, output):
        key = output.keys()[0]

        return {
            'stdout': outputs.StdoutOutput,
            'tempodb': outputs.TempoDBOutput
        }[key](**output.values()[0])
