.. image:: https://travis-ci.org/mattboyer/nosedive.svg?branch=master
    :target: https://travis-ci.org/mattboyer/nosedive

.. image:: https://coveralls.io/repos/mattboyer/nosedive/badge.svg?branch=master
    :target: https://coveralls.io/r/mattboyer/nosedive

.. image:: https://img.shields.io/pypi/v/nosedive.svg
    :target: https://pypi.python.org/pypi/nosedive/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/format/nosedive.svg
    :target: https://pypi.python.org/pypi/nosedive/
    :alt: Download format

.. image:: https://img.shields.io/pypi/pyversions/nosedive.svg
    :target: https://pypi.python.org/pypi/nosedive/
    :alt: Supported Python versions

Nosedive
========

``nosedive`` is a plugin for the popular `Nose <http://nose.readthedocs.org/en/latest/index.html>`_ unit test framework and runner for Python. ``nosedive`` aims to complement code coverage metrics by exposing how *directly* the code in the product under test is called from your unit tests.

But why?
--------

I have found that code coverage metrics can be very misleading. Code coverage tools, such as Ned Batchelder's excellent `coverage <http://coverage.readthedocs.org/en/latest/>`_ Nose plugin, give developers an incentive to increase their code's overall coverage index. In other words, I am encouraged to ensure that my unit tests cause 100% of the Python statements in the code under test to be executed. This doesn't necessarily mean that 100% of the statements in the code under test will be executed as part of a specific and meaningful unit test!

Enter `nosedive`. Whereas `coverage` reports how many of the statements in the code under test have been executed, `nosedive` reports the shortest call stack distance between your unit tests and every callable in the code under test that is called at least once. If for instance `nosedive` reports that `product.widgets.foo.FooWidget.widgetise()` has a score of 3, this means that the `widgetise` method defined on my `FooWidget` class in module `product.widgets.foo` is indeed reached by my unit tests, but only very indirectly. It is exercised most directly when it is called by *something* called by **another something** called by my unit test. This isn't necessarily wrong, but it may be a meaningful signal that I need to write more specific and focused unit tests for `FooWidget`.

Screenshot
----------

.. image:: docs/screenshot.png

Installation
------------

``nosedive`` does not require any dependency beside Python and Nose. To install, simply type:

.. code-block:: bash

    pip install nosedive

You can also `clone <https://help.github.com/articles/cloning-a-repository/>`_ this repository and run the following from your working copy:

.. code-block:: bash

    python setup.py install

Usage
-----------------------

Simply run

.. code-block:: bash

    nosetests (other nose options) --with-nosedive

Notes
-----

``nosedive`` currently conflicts with the ``coverage`` Nose plugins. It is recommended that you do not run nose with both plugins enabled at the same time.

To-Dos
------

``nosedive`` isn't very mature and does not have special handling for decorators. Therefore, decorated calls will be given a score that reflects the presence of the decorators in the call stack.
