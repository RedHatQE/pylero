#!/usr/bin/env python
# -*- coding: utf8 -*-

# I want to separate internal tests from the sources because the term "test"
# is often used in the sources as one of key abstractions. It would be
# confusing to mix files of the testing code and sources related to the test
# abstraction.

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import unittest

# Have sources on the module search path
project_root = os.path.dirname((sys.path[0]))
project_sources = os.path.join(project_root, 'src')
sys.path.insert(1, project_sources)

# Here the main testing driver will come. In the mean time, just
# use brute force...
import pylarionlib_tests.replace_me_later
unittest.main(pylarionlib_tests.replace_me_later)
