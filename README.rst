===============================
Probe
===============================

.. image:: https://badge.fury.io/py/probe.png
    :target: http://badge.fury.io/py/probe
    
.. .. image:: https://travis-ci.org/BrianHicks/probe.png?branch=master
..         :target: https://travis-ci.org/BrianHicks/probe

.. image:: https://pypip.in/d/probe/badge.png
        :target: https://crate.io/packages/probe?version=latest


Probe lets you ship personal metrics (feelings, energy level, productivity) to
external services for analysis.

* Free software: BSD license
* Documentation: http://probe.rtfd.org.

Features
--------

* Keep track of numbers, ratings, hours, and yes/no questions.
* Ship personal metrics to multiple services.
* Schedule how often you want to collect data, it'll keep track.

Getting Started
---------------

Run ``probe init`` after installing. Then look at the "configuratione example"
below. To anwer questions, run ``probe answer``.

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
      - stdout:
        level: debug

      - tempodb:
        key: ...
        secret: ...


Save this as ``~/.probe_config`` and run ``probe``, and you'll get some nice output
asking you questions at appropriate times. Run it as many times as you like,
the questions will only be asked once per appropriate period.

Available Units:

* Hours (key: ``hours``) takes upper and lower limit (lower defaults to 0)

* Rating (key: ``rating``) takes upper and lower limit. (default to 10 and 0,
  respectively)

* Number (key: ``number``) keep track of arbitrary floating-point numbers.

* Yes/No (key: ``yesno``) answers a yes/no question. (accepts yes/no, 0/1, and
  true/false or shortened versions like t/f.)

Available Outputs:

* StdOut (key: ``stdout``) accepts a "level" argument - currently info or
  debug.

* TempoDB (key: ``tempodb``) accepts any arguments passed to ``tempodb.Client``
  but you'll probably only need to know ``key`` and ``secret``. Get these for a
  database in your account.
  
  You'll need to install with the "tempodb" extra (``pip install
  probe[tempodb]``) for this to work. You could also just install the tempodb
  client, but installing with the extra ensures you'll get future dependencies.
