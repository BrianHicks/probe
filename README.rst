===============================
Probe
===============================

.. image:: https://badge.fury.io/py/probe.png
    :target: http://badge.fury.io/py/probe
    
.. image:: https://travis-ci.org/BrianHicks/probe.png?branch=master
        :target: https://travis-ci.org/BrianHicks/probe

.. image:: https://pypip.in/d/probe/badge.png
        :target: https://crate.io/packages/probe?version=latest


Probe lets you ship personal metrics (feelings, energy level, productivity) to
external services for analysis.

* Free software: BSD license
* Documentation: http://probe.rtfd.org.

Features
--------

* TODO

Configuration Example
---------------------

::

    questions:
      - sleep.hours:
        text: How long did you sleep last night? (in hours)
        unit: hours
        interval: every day

      - energy:
        text: what is your energy level right now?
        unit: rating
        lower: 0
        upper: 10

    outputs:
      - filesystem:
        file: ~/probe_data.json


Save this as ``~/probe.yml`` and run ``probe``, and you'll get some nice output
asking you questions at appropriate times. Run it as many times as you like,
the questions will only be asked once per appropriate period.

Planned Features
----------------

* Intervals: hourly, daily, weekly, monthly, every {n} [minutes|hours|weeks|days]
* Outputs:
  * TempoDB
  * webhooks
  * filesystem
