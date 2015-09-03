###############################################################################
# Copyright 2015 University of Florida. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

import datetime
import re

from ..core import wrappers


def detect(data):
    if not hasattr(data, 'template'):
        return 'json'

    if not data.template('2.16.840.1.113883.3.88.11.32.1').is_empty():
        return 'c32'

    if not data.template('2.16.840.1.113883.10.20.22.1.1').is_empty():
        return 'ccda'


def entries(element):
    """
    Get entries within an element (with tag name 'entry'), adds an `each` method
    """
    els = element.els_by_tag('entry')
    els.each = lambda callback: map(callback, els)
    return els


def parse_address(address_element):
    """
    Parses an HL7 address (streetAddressLine [], city, state, postalCode,
    country)

    :param address_element:
    :return:
    """
    els = address_element.els_by_tag('streetAddressLine')
    street = [e.val() for e in els if e.val()]

    city = address_element.tag('city').val()
    state = address_element.tag('state').val()
    zip = address_element.tag('postalCode').val()
    country = address_element.tag('country').val()

    return wrappers.ObjectWrapper(
        street=street,
        city=city,
        state=state,
        zip=zip,
        country=country,
    )


def parse_date(string):
    """
    Parses an HL7 date in String form and creates a new Date object.

    TODO: CCDA dates can be in form:
        <effectiveTime value="20130703094812"/>
    ...or:
        <effectiveTime>
            <low value="19630617120000"/>
            <high value="20110207100000"/>
        </effectiveTime>

    For the latter, parse_date will not be given type `string` and will return
    `None`.

    The syntax is "YYYYMMDDHHMMSS.UUUU[+|-ZZzz]" where digits can be omitted
    the right side to express less precision
    """
    if not isinstance(string, basestring):
        return None

    if len(string) < 4:
        # not even a year
        return None

    if int(string[:4]) < 1800:
        # Arbitrate on the year value
        return None

    # ex. value="1999" translates to 1 Jan 1999
    if len(string) == 4:
        return datetime.date(int(string), 1, 1)

    year = int(string[0:4])
    month = int(string[4:6])
    day = int(string[6:8] or 1)

    # check for time info (the presence of at least hours and mins after the
    # date)
    if len(string) >= 12:
        # owing to the vagueries of the different time formats we can get a range of inputs
        # Solution: Regex!
        time_re = re.compile(r'(\d{4})(\d{2})(\d{2})(\d{2})?(\d{2})?(\d{2})?(\.\d+)?([+-]\d{4}|Z)?')
        if time_re.match(string):
            # we capture microseconds, have seen in CCDA documents, but throw it away
            # we do need to capture the timezone, and the microseconds were throwing that off
            _year, _month, _day, _hour, _mins, _secs, _msecs, _tz = time_re.match(string).groups()
            year = int(_year)
            month = int(_month)
            day = int(_day)
            hour = int(_hour)
            mins = int(_mins)
            if not _secs:
                secs = 0
            else:
                secs = int(_secs)
            if _tz is None:
                _tz = ''
        else:
            hour = int(string[8:10])
            mins = int(string[10:12])
            secs = string[12:14]
            secs = int(secs) if secs else 0
            _tz = string[14:]
        timezone = wrappers.FixedOffset.from_string(_tz)
        return datetime.datetime(year, month, day, hour, mins, secs,
                                 tzinfo=timezone)

    return datetime.date(year, month, day)


def parse_name(name_element):
    prefix = name_element.tag('prefix').val()
    els = name_element.els_by_tag('given')
    given = [e.val() for e in els if e.val()]
    family = name_element.tag('family').val()

    return wrappers.ObjectWrapper(
        prefix=prefix,
        given=given,
        family=family
    )