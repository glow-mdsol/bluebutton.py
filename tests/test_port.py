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
import random
import subprocess
import traceback
import unittest
import Levenshtein
import sys

import bluebutton


class PortTests(unittest.TestCase):
    """
    Tests the Python port of BlueButton.js

    The JSON output must be exactly identical.
    """

    prefix = os.path.realpath(__file__ + '/../..')

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

    def test_sample_allscripts_mu2(self):
        # so, this always fails on the text in the medications records
        testfile = ('/bluebutton.js/bower_components/sample_ccdas/'
                    'Allscripts Samples/Internal Test with MU 2 data/'
                    '170.314B2_Amb_CCD.xml')
        self.python_output_is_same_as_javascript(testfile=self.prefix + testfile)

    def get_random_samples(self, count=5):
        """
        Search the bower_components for xml files and return up to count paths
        :param count: number of xml files to return
        :return: list of paths
        """
        matches = []
        to_search = self.prefix + '/bluebutton.js/bower_components/sample_ccdas'
        for root, dirs, files in os.walk(to_search):
            for file in files:
                if file.endswith(".xml"):
                    # append the path, stripping the prefix
                    matches.append(os.path.join(root, file).replace(self.prefix, ''))

        return [random.choice(matches) for x in range(0, count)]

    def test_samples(self):
        def check(t):
            self.python_output_is_same_as_javascript(testfile=self.prefix + t)

        check('/bluebutton.js/bower_components/sample_ccdas/HL7 Samples/CCD.sample.xml')
        check('/bluebutton.js/bower_components/sample_ccdas/NIST Samples/CCDA_CCD_b1_Ambulatory_v2.xml')
        check('/bluebutton.js/bower_components/sample_ccdas/NIST Samples/CCDA_CCD_b1_InPatient_v2.xml')
        check('/bluebutton.js/bower_components/sample_ccdas/Transitions of Care Samples/'
              'ToC_CCDA_CCD_CompGuideSample_FullXML.xml')
        check('/bluebutton.js/bower_components/sample_ccdas/Allscripts Samples/Professional EHR'
              '/Encounter Based C-CDA CCD - 08-06-2012 [Jones, Isabella - 170314E2].xml')
        # randomly choose CDA documents to test
        for sample_ccd in self.get_random_samples(10):
            check(sample_ccd)

    def python_output_is_same_as_javascript(self, section_name=None,
                                            testfile=None):
        """ Compares JavaScript output to Python """
        bluebutton_js = self.prefix + '/bluebutton.js/build/bluebutton.js'
        sample_ccd = testfile or (self.prefix +
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
            self.fail('bluebutton.js unable to process %s: %s' % (sample_ccd.replace(self.prefix, ''), e.message))
        with open(sample_ccd) as fp:
            xml = fp.read()
            try:
                bb = bluebutton.BlueButton(xml)
            except (ValueError, AttributeError) as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.fail("Error processing %s: %s (%s)" % (sample_ccd.replace(self.prefix, ''),
                                                            e.message,
                                                            traceback.print_tb(exc_traceback)))
            if section_name:
                python = json.loads(getattr(bb.data, section_name).json())
            else:
                python = json.loads(bb.data.json())

        if not section_name:
            status, failed = self.element_wise_match(python, javascript)
            self.assertTrue(status,
                            msg="Matching CCD %s failed - %s" % (sample_ccd.replace(self.prefix, ''), failed))
        else:
            self.assertEquals(prettify(javascript), prettify(python))

    def element_wise_match(self, py, js, text_guard=True):
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
        for section_name, py_section in py.items():
            js_section = js.get(section_name)
            if js_section != py_section:
                for idx in range(0, len(py_section)):
                    if py_section[idx] != js_section[idx]:
                        # doesn't match, let's dig a little deeper
                        for attr, value in py_section[idx].items():
                            if py_section[idx].get(attr) != js_section[idx].get(attr):
                                if py_section[idx].get(attr) == '' and js_section[idx].get(attr) is None:
                                    # the way that empty strings are interpreted
                                    continue
                                if attr != u'text':
                                    # if one of the non-text sections doesn't match
                                    # then that's a automatic fail
                                    return False, section_name
                                else:
                                    try:
                                        # String matching is difficult! Remove whitespace and try again
                                        _py_text = "".join(py_section[idx].get(attr).split())
                                        _js_text = "".join(js_section[idx].get(attr).split())
                                        if Levenshtein.distance(_py_text, _js_text) > 0:
                                            return False, section_name
                                    except TypeError:
                                        # Not
                                        return False, section_name
        else:
            return True, None


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
