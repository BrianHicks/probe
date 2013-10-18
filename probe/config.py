#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import shelve
import yaml

from . import questions


class ConfigHandler(object):
    @classmethod
    def from_paths(cls, config_path, last_run_path):
        with open(config_path, 'r') as c:
            config = c.read()

        data = shelve.open(last_run_path)

        try:
            last_run = data['last_run']
        except KeyError:
            last_run = datetime.now()
            data['last_run'] = last_run

        data.close()

        return cls(config, last_run)

    def __init__(self, config_text, last_run):
        self.config = yaml.safe_load(config_text)

        # dehydrate questions
        self.config['questions'] = map(
            self.parse_question, self.config.get('questions', [])
        )
        self.config['last_run'] = last_run

    def parse_question(self, question):
        unit = question.values()[0].get('unit', 'number')
        units = {
            'hours': questions.HoursQuestion,
            'rating': questions.RatingQuestion,
            'number': questions.NumberQuestion,
            'yesno': questions.YesNoQuestion,
        }
        return units[unit](question)
