# -*- coding: utf-8 -*-

__author__ = 'glow'


class NullFlavors(object):
    DESCRIPTION = "NullFlavor"
    SYMBOL = ""

    def __str__(self):
        return self.DESCRIPTION

    def __unicode__(self):
        return unicode(self.DESCRIPTION)

    @classmethod
    def create(cls, symbol):
        for klass in cls.__subclasses__():
            if klass.SYMBOL == symbol:
                return klass()
        cls.SYMBOL = symbol
        return cls()

class NoInformation(NullFlavors):
    DESCRIPTION = "No Information"
    SYMBOL = "NI"


class NotApplicable(NullFlavors):
    DESCRIPTION = "Not Applicable"
    SYMBOL = "NA"


class Unknown(NullFlavors):
    DESCRIPTION = "Unknown"
    SYMBOL = "UNK"


class AskedButNotKnown(NullFlavors):
    DESCRIPTION = "Asked But Not Known"
    SYMBOL = "ASKU"


class TemporarilyUnavailable(NullFlavors):
    DESCRIPTION = "Temporarily Unavailable"
    SYMBOL = "NAV"


class NotAsked(NullFlavors):
    DESCRIPTION = "Not Asked"
    SYMBOL = "NASK"


class Masked(NullFlavors):
    DESCRIPTION = "Masked"
    SYMBOL = "MSK"


class NoMatchingCode(NullFlavors):
    DESCRIPTION = "No Matching Code"
    SYMBOL = "OTH"

