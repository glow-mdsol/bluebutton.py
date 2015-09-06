# -*- coding: utf-8 -*-
__author__ = 'glow'

import unittest
from bluebutton.core.null_flavors import NullFlavors, NoInformation, NotApplicable, Unknown, AskedButNotKnown, \
    TemporarilyUnavailable, NotAsked, Masked, NoMatchingCode


class TestNullFlavors(unittest.TestCase):

    def test_no_information(self):
        cls = NullFlavors.create("NI")
        self.assertTrue(isinstance(cls, NoInformation))
        self.assertEqual("No Information", str(cls))

    def test_not_applicable(self):
        cls = NullFlavors.create("NA")
        self.assertTrue(isinstance(cls, NotApplicable))
        self.assertEqual("Not Applicable", str(cls))

    def test_unknown(self):
        cls = NullFlavors.create("UNK")
        self.assertTrue(isinstance(cls, Unknown))
        self.assertEqual("Unknown", str(cls))

    def test_asked_but_not_known(self):
        cls = NullFlavors.create("ASKU")
        self.assertTrue(isinstance(cls, AskedButNotKnown))
        self.assertEqual("Asked But Not Known", str(cls))

    def test_temporarily_unavailable(self):
        cls = NullFlavors.create("NAV")
        self.assertTrue(isinstance(cls, TemporarilyUnavailable))
        self.assertEqual("Temporarily Unavailable", str(cls))

    def test_not_asked(self):
        cls = NullFlavors.create("NASK")
        self.assertTrue(isinstance(cls, NotAsked))
        self.assertEqual("Not Asked", str(cls))

    def test_masked(self):
        cls = NullFlavors.create("MSK")
        self.assertTrue(isinstance(cls, Masked))
        self.assertEqual("Masked", str(cls))

    def test_no_matching_code(self):
        cls = NullFlavors.create("OTH")
        self.assertTrue(isinstance(cls, NoMatchingCode))
        self.assertEqual("No Matching Code", str(cls))

    def test_fall_back(self):
        cls = NullFlavors.create("NINF")
        self.assertTrue(isinstance(cls, NullFlavors))
        self.assertEqual("NullFlavor", str(cls))
        self.assertEqual("NINF", cls.SYMBOL)


if __name__ == '__main__':
    unittest.main()
