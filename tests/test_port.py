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
import Levenshtein
import sys

import bluebutton

prefix = os.path.realpath(__file__ + '/../..')


def escape_name(name):
    """
    replace all the unacceptable chars with underscores and lowercase
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


class BlueButtonTestClass(unittest.TestCase):

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
        if set(py.keys()).difference(js.keys()):
            # different keys, that's a fail
            return False, 'sections'
        for section_name in sorted(py.keys()):
            js_section = js.get(section_name)
            py_section = py.get(section_name)
            if js_section != py_section:
                if not type(py_section) == type(js_section):
                    # if the types of the section differ then that's a problem
                    return False, section_name
                for py, js in zip(py_section, js_section):
                    if py != js:
                        # doesn't match, let's dig a little deeper
                        for attr, value in py.items():
                            if py.get(attr) != js.get(attr):
                                if py.get(attr) == '' and js.get(attr) is None:
                                    # the way that empty strings are interpreted
                                    continue
                                if attr != u'text':
                                    # if one of the non-text sections doesn't match
                                    # then that's a automatic fail
                                    return False, section_name
                                else:
                                    try:
                                        # String matching is challenging! Remove whitespace and try again
                                        _py_text = "".join(py.get(attr).split())
                                        _js_text = "".join(js.get(attr).split())
                                        if Levenshtein.distance(_py_text, _js_text) > 0:
                                            return False, section_name
                                    except TypeError:
                                        # Not
                                        return False, section_name
        else:
            return True, None


class SampleCCDATests(BlueButtonTestClass):
    # TODO: look at parallel testing, this runs slowly
    __metaclass__ = TestDocumentsMeta


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
