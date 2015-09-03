# -*- coding: utf-8 -*-

__author__ = 'glow'

import datetime
import unittest
from bluebutton.documents import parse_date
from bluebutton.core.wrappers import FixedOffset


class TestParseDate(unittest.TestCase):

    DT = datetime.datetime(2012,1,1,1,1,0)

    def test_dateparse_samples(self):
        """We can parse a wide range of possible time formats"""
        effective_time_values = ['20101028092016.829-0500',
                                 '20101026091700.000-0500',
                                 '19630617120000',
                                 '198708',
                                 '1954',
                                 '201308221815',
                                 '201312010800-0800']
        parsed = [datetime.datetime(2010, 10, 28, 9, 20, 16, 0, FixedOffset(-300, '-0500')),
                  datetime.datetime(2010, 10, 26, 9, 17, 0, 0, FixedOffset(-300, '-0500')),
                  datetime.datetime(1963, 6, 17, 12, 0, 0, 0, FixedOffset(0, 'UTC')),
                  datetime.date(1987, 8, 1),
                  datetime.date(1954, 1, 1),
                  datetime.datetime(2013, 8, 22, 18, 15, 0, 0, FixedOffset(0, 'UTC')),
                  datetime.datetime(2013, 12, 1, 8, 0, 0, 0, FixedOffset(-480, '-0800'))
                  ]
        for datestr, parsed in zip(effective_time_values, parsed):
            lib = parse_date(datestr)
            if isinstance(parsed, datetime.datetime):
                self.assertEqual(lib.date(), parsed.date())
                self.assertEqual(lib.time(), parsed.time())
                self.assertEqual(lib.tzinfo.utcoffset(self.DT),
                                 parsed.tzinfo.utcoffset(self.DT))
            else:
                self.assertEqual(lib, parsed)

    def test_invalid_date_too_short(self):
        self.assertEqual(None, parse_date('08'))

    def test_invalid_date_not_positive(self):
        self.assertEqual(None, parse_date('-08'))

    def test_invalid_date_greenway_case(self):
        # so the date string '000101' gets parsed to 1901/1/1 by Javascript
        # python thinks that is insane, I agree with python
        self.assertEqual(None, parse_date('000101'))

