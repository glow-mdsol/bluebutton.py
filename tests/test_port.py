#!/usr/bin/env python
###############################################################################
# Copyright 2015 University of Florida. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Compares the demographics output with that of BlueButton.js
"""

import json
import os
import re
import subprocess
import traceback
import unittest
import sys

import bluebutton

prefix = os.path.realpath(__file__ + '/../..')

# XML Declaration failures - owing to the bluebutton.js requiring a <?xml declaration
# these files fail to parse
XMLDECL = ("LMR1TEST.xml",
           "LMR2TEST.xml",
           "LMR3TEST.xml",
           "LMR4TEST.xml",
           "LMR5TEST.xml",
           "partners.ccda.xml",
           "AdamEveryman-ReferralSummary.xml",
           "IsabellaJones-ReferralSummary.xml",
           "MaryGrant-ClinicalSummary.xml")

# Defunct format files - inconsistent date formats, etc
# add files and reason for excluding here
IRREGULAR = ('26933_ExportSummary_CCDA.xml', # has a effectiveTime with value of '000101'
             )

# a list of know failures where the document is 'at fault' - we should work to whittle this block down
# through improved handling or fixed files
BLACKLIST = XMLDECL + IRREGULAR


def escape_name(name):
    """
    replace all the unacceptable chars with underscores and lowercase - used in building test case names
    :param name: file name
    :type name str
    :return:
    """
    _name = str(name).lower()
    return re.sub(r'[^0-9a-zA-Z_]+', '_', _name)


def get_sample_folders():
    """
    Scans for the CCDA documents
    :return: a dict of folder and list of filenames
    :rtype: dict
    """
    matches = {}
    to_search = prefix + '/bluebutton.js/bower_components/sample_ccdas'
    for root, dirs, files in os.walk(to_search):
        for filename in filter(lambda x: x.lower().endswith('.xml'), files):
            if filename in BLACKLIST:
                continue
            # append the path, stripping the prefix
            matches.setdefault(root.replace(prefix, ''), []).append(filename)
    return matches


# populate the global var with the sample documents
sample_ccdas = get_sample_folders()


class TestDocumentsMeta(type):
    def __new__(mcs, name, bases, dict):

        def gen_test(filename):
            def test(self):
                def check(t):
                    self.python_output_is_same_as_javascript(testfile=prefix + t)

                check(filename)

            return test

        for document_root, files in sample_ccdas.items():
            repository = document_root.replace('/bluebutton.js/bower_components/sample_ccdas/', '')
            for filename in files:
                test_name = "test_%s_%s" % (escape_name(repository),
                                            escape_name(filename))
                dict[test_name] = gen_test(os.path.join(document_root,
                                                        filename))
        return type.__new__(mcs, name, bases, dict)


def class_compare(a, b):
    """
    Compares two instances types together accounting for the dict <=> DictWrapper
    :param a: an instance
    :type a object
    :param b: an instance
    :type b object
    :return: whether the two instances are of the same type
    :rtype: bool
    """
    if type(a) == type(b):
        return True
    elif isinstance(a, dict) and isinstance(b, dict):
        # type signatures differ for dict and DictWrapper
        return True
    return False


def text_sections_match(a, b):
    """
    Compare two text sections, stripping all white space and inconsequential character
    NOTE: due to the way the JS and PY get generated, empty fields can be either None or ''
     we assume in the case where one is '' and the other None then these are equivalent
    :param a: left hand text
    :type a str
    :param b: right hand text
    :type b str
    :return: a bool summarising whether the strings are equivalent
    :rtype: bool
    """
    # String matching is challenging! Remove whitespace and try again
    if isinstance(a, basestring) and isinstance(b, basestring):
        if "".join(a.lower().split()) == "".join(b.lower().split()):
            return True
    elif a in ['', None] and b in ['', None]:
        # empty strings match
        return True
    return False


def compare_dicts(a, b, path=[]):
    """
    Compare two nested dicts, returns True and the current path if the dicts match, False if an inconsistency
    :param a: left hand dict
    :type a dict
    :param b: right hand dict
    :type b dict
    :param path: accumulated path in the tree
    :type path list
    :return: state and path
    :rtype: tuple
    """
    state = True
    for key in set(a.keys()).union(set(b.keys())):
        if prettify(a[key]) == prettify(b[key]):
            # they match at a macro level, go no further
            continue
        # add the current key to the path
        path.append(key)
        if isinstance(a[key], dict):
            state, path = compare_dicts(a[key], b[key], path)
        elif isinstance(a[key], list):
            for _a, _b in zip(a[key], b[key]):
                if isinstance(_a, dict):
                    state, path = compare_dicts(_a, _b, path)
                else:
                    state = _a == _b
        else:
            state = a[key] == b[key]
            if state is False:
                if key == u'text':
                    # we know that text sections can differ, so add another layer of checking for content
                    #  similarity
                    state = text_sections_match(a[key], b[key])
                elif a[key] in ["", None] and b[key] in ["", None]:
                    # Owing to the way empty elements get deserialised by the XML parser to
                    #  empty strings, whereas the JS of nil gets munged to None
                    state = a[key] in ["", None] and b[key] in ["", None]
        # get out of the loop
        if state is False:
            return state, path
        # remove the key
        path.pop()

    return state, path


class BlueButtonTestClass(unittest.TestCase):
    """Shared Parent Class for bluebutton.py unit tests"""
    def python_output_is_same_as_javascript(self, section_name=None,
                                            testfile=None):
        """ Compares JavaScript output to Python """
        bluebutton_js = prefix + '/bluebutton.js/build/bluebutton.js'
        sample_ccd = testfile or (prefix +
                                  '/bluebutton.js/bower_components/sample_ccdas'
                                  '/HL7 Samples/CCD.sample.xml')

        try:
            javascript = execute("""
                var fs = require('fs');
                var BlueButton = require('%s');
                var xml = fs.readFileSync('%s', 'utf-8');
                var ccd = BlueButton(xml);

                console.log(ccd.data%s.json());""" % (bluebutton_js, sample_ccd,
                                                      '' if not section_name
                                                      else '.' + section_name))
        except subprocess.CalledProcessError, e:
            self.fail('bluebutton.js unable to process %s: %s' % (sample_ccd.replace(prefix, ''),
                                                                  e.message))
        with open(sample_ccd) as fp:
            xml = fp.read()
            try:
                bb = bluebutton.BlueButton(xml)
            except (ValueError, AttributeError) as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.fail("Error processing %s: %s (%s)" % (sample_ccd.replace(prefix, ''),
                                                            e.message,
                                                            traceback.print_tb(exc_traceback)))
            if section_name:
                python = json.loads(getattr(bb.data, section_name).json())
            else:
                python = json.loads(bb.data.json())

        if not section_name:
            matches, failed = self.element_wise_match(python, javascript)
            self.assertTrue(matches,
                            msg="Matching CCD %s failed - %s" % (sample_ccd.replace(prefix, ''), failed))
        else:
            self.assertEquals(prettify(javascript), prettify(python))

    def element_wise_match(self, py, js):
        """
        Compares the results on an elementwise basis
        :param text_guard: handle spacing inconsistencies
        :type text_guard bool
        :param py: the resultant dict from the processing using bluebutton.py
        :type py dict
        :param js: the resultant dict from the processing using bluebutton.js
        :type js dict
        :return: do the structures match?
        :rtype : bool
        """
        if prettify(js) == prettify(py):
            # quick compare
            return True, None

        return compare_dicts(py, js)


class SampleCCDATests(BlueButtonTestClass):
    # TODO: look at parallel testing, this runs slowly
    __metaclass__ = TestDocumentsMeta


class GreenwayCCDATests(BlueButtonTestClass):

    def test_bom_parsing(self):
        filepath = '/bluebutton.js/bower_components/sample_ccdas/' + \
            'Greenway Samples/26562_ExportSummary_CCDA.xml'
        filename = prefix + filepath
        with open(filename, 'r') as fp:
            xml = fp.read()
            try:
                bb = bluebutton.BlueButton(xml)
            except (ValueError, AttributeError) as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.fail("Error processing %s: %s (%s)" % (filename.replace(prefix, ''),
                                                            e.message,
                                                            traceback.print_tb(exc_traceback)))
        self.assertEqual(["Maria"], bb.data.demographics.name.given)
        self.assertEqual("Hernandez", bb.data.demographics.name.family)


class PortTests(BlueButtonTestClass):
    """
    Tests the Python port of BlueButton.js

    The JSON output must be exactly identical.
    """

    def test_compare_document(self):
        return self.python_output_is_same_as_javascript('document')

    def test_compare_allergies(self):
        self.python_output_is_same_as_javascript('allergies')

    def test_compare_care_plan(self):
        self.python_output_is_same_as_javascript('care_plan')

    def test_compare_chief_complaint(self):
        self.python_output_is_same_as_javascript('chief_complaint')

    def test_compare_demographics(self):
        self.python_output_is_same_as_javascript('demographics')

    def test_compare_encounters(self):
        self.python_output_is_same_as_javascript('encounters')

    def test_compare_functional_statuses(self):
        self.python_output_is_same_as_javascript('functional_statuses')

    def test_compare_immunizations(self):
        self.python_output_is_same_as_javascript('immunizations')

    def test_compare_immunizations_declines(self):
        self.python_output_is_same_as_javascript('immunization_declines')

    def test_compare_instructions(self):
        self.python_output_is_same_as_javascript('instructions')

    def test_compare_results(self):
        self.python_output_is_same_as_javascript('results')

    def test_compare_medications(self):
        self.python_output_is_same_as_javascript('medications')

    def test_compare_problems(self):
        self.python_output_is_same_as_javascript('problems')

    def test_compare_procedures(self):
        self.python_output_is_same_as_javascript('procedures')

    def test_compare_smoking_status(self):
        self.python_output_is_same_as_javascript('smoking_status')

    def test_compare_vitals(self):
        self.python_output_is_same_as_javascript('vitals')


class DictWrapper(dict):
    def __init__(self, *args, **kwargs):
        super(DictWrapper, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        return self[name]


def execute(javascript):
    results = subprocess.check_output(['/usr/bin/env', 'node', '-e',
                                       javascript])
    return json.loads(results, object_hook=DictWrapper)


def prettify(obj):
    return json.dumps(obj, sort_keys=True, indent=4)


if __name__ == '__main__':
    unittest.main()
