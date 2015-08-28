Technical Specification for PyCCDA
==================================

This document outlines the port of [BlueButton.js][] to Python.

[BlueButton.js]: https://github.com/blue-button/bluebutton.js/


Values
------

 - **Pythonic**
   - The code should feel natural to a Python developer.

 - **Excellent documentation**
   - Classes and functions should be well documented.
   - Seasoned developers and new or part-time coders should all get use out of
   the documentation.
   - Code should be self-documenting, meaning written for readability.

 - **Utilize the original BlueButton.js**
   - BlueButton.js serves as an implementation guide.
   - Translation is easier than re-implementing. _(Hopefully this is true!)_
   - User communities should be able to share, help, and understand each other.


Concepts
--------

 * Parser ...
 * Generator ...
 * Section ...
 * Document ...
 * Allergies
 * Care Plan
 * Chief Complaint
 * Demographics
 * Encounters
 * Functional Statuses
 * Immunizations
 * Instructions
 * Results
 * Medications
 * Problems
 * Procedures
 * Smoking Status
 * Vitals

References
----------

 * [BlueButton.js](http://bluebuttonjs.com)
 * [HL7 Consolidated CDA Specification](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=258)


Todo
----

 * Convert all BlueButton.js files from JavaScript to Python

| BlueButton.js file | Python equivalent | Notes | Ported? |
| :------------------ | :----------------- | :----- | :-------: |
| ```lib/bluebutton.js``` | ```pyccda/__init__.py``` | - | Not yet |
| ```lib/core.js``` | ```pyccda/core/__init__.py``` | - | Not yet |
| ```lib/core/codes.js``` | ```pyccda/core/codes.py``` | - | Not yet |
| ```lib/core/xml.js``` | ```pyccda/core/xml.py``` | - | Not yet |
| ```lib/documents.js``` | ```pyccda/documents/__init__.py``` | - | Not yet |
| ```lib/documents/c32.js``` | ```pyccda/documents/c32.py``` | - | Not yet |
| ```lib/documents/ccda.js``` | ```pyccda/documents/ccda.py``` | - | Not yet |
|```lib/documents/ccda.js```|```pyccda/documents/ccda.py```|   | Not yet |
|```lib/generators.js```|```pyccda/generators/__init__.py```|   | Not yet |
|```lib/generators/c32.js```|```pyccda/generators/c32.py```|   | Not yet |
|```lib/generators/ccda.js```|```pyccda/generators/ccda.py```|   | Not yet |
|```lib/generators/ccda_template.ejs```| NA|   |   |
|```lib/parsers.js```|```pyccda/parsers/__init__.py```|   | Not yet |
|```lib/parsers/c32.js```|```pyccda/parsers/c32/__init__.py```|   | Not yet |
|```lib/parsers/c32/allergies.js```|```pyccda/parsers/c32/allergies.py```|   | Not yet |
|```lib/parsers/c32/demographics.js```|```pyccda/parsers/c32/demographics.py```|   | Not yet |
|```lib/parsers/c32/document.js```|```pyccda/parsers/c32/document.py```|   | Not yet |
|```lib/parsers/c32/encounters.js```|```pyccda/parsers/c32/encounters.py```|   | Not yet |
|```lib/parsers/c32/immunizations.js```|```pyccda/parsers/c32/immunizations.py```|   | Not yet |
|```lib/parsers/c32/medications.js```|```pyccda/parsers/c32/medications.py```|   | Not yet |
|```lib/parsers/c32/problems.js```|```pyccda/parsers/c32/problems.py```|   | Not yet |
|```lib/parsers/c32/procedures.js```|```pyccda/parsers/c32/procedures.py```|   | Not yet |
|```lib/parsers/c32/results.js```|```pyccda/parsers/c32/results.py```|   | Not yet |
|```lib/parsers/c32/vitals.js```|```pyccda/parsers/c32/vitals.py```|   | Not yet |
|```lib/parsers/ccda.js```|```pyccda/parsers/ccd/__init__.py```|   | Not yet |
|```lib/parsers/ccda/allergies.js```|```pyccda/parsers/ccda/allergies.py```|   | Not yet |
|```lib/parsers/ccda/care_plan.js```|```pyccda/parsers/ccda/care_plan.py```|   | Not yet |
|```lib/parsers/ccda/demographics.js```|```pyccda/parsers/ccda/demographics.py```|   | Not yet |
|```lib/parsers/ccda/document.js```|```pyccda/parsers/ccda/document.py```|   | Not yet |
|```lib/parsers/ccda/encounters.js```|```pyccda/parsers/ccda/encounters.py```|   | Not yet |
|```lib/parsers/ccda/free_text.js```|```pyccda/parsers/ccda/free_text.py```|   | Not yet |
|```lib/parsers/ccda/functional_statuses.js```|```pyccda/parsers/ccda/functional_statuses.py```|   | Not yet |
|```lib/parsers/ccda/immunizations.js```|```pyccda/parsers/ccda/immunizations.py```|   | Not yet |
|```lib/parsers/ccda/instructions.js```|```pyccda/parsers/ccda/instructions.py```|   | Not yet |
|```lib/parsers/ccda/medications.js```|```pyccda/parsers/ccda/medications.py```|   | Not yet |
|```lib/parsers/ccda/problems.js```|```pyccda/parsers/ccda/problems.py```|   | Not yet |
|```lib/parsers/ccda/procedures.js```|```pyccda/parsers/ccda/procedures.py```|   | Not yet |
|```lib/parsers/ccda/results.js```|```pyccda/parsers/ccda/results.py```|   | Not yet |
|```lib/parsers/ccda/smoking_status.js```|```pyccda/parsers/ccda/smoking_status.py```|   | Not yet |
|```lib/parsers/ccda/vitals.js```|```pyccda/parsers/ccda/vitals.py```|   | Not yet |
|```lib/renderers.js```|```pyccda/renderers/__init__.py```|   | Not yet |
|```lib/renderers/html.js```|```pyccda/renderers/html.py```|   | Not yet |

Testing
-------

	shell$ make test

Testing serves a dual-purpose: to ensure our code works as expected and to
document its intended use.

 - Port original tests:
   - spec/javascripts/amd_specs/bluebutton_spec.js
   - spec/javascripts/amd_specs/c32_spec.js
   - spec/javascripts/amd_specs/ccda_generator_spec.js
   - spec/javascripts/amd_specs/ccda_spec.js
   - spec/javascripts/browser_specs/bluebutton_spec.js
   - spec/javascripts/browser_specs/c32_spec.js
   - spec/javascripts/browser_specs/ccda_generator_spec.js
   - spec/javascripts/browser_specs/ccda_spec.js
   - spec/javascripts/fixtures/c32/HITSP_C32_with_HL7_IDs.xml
   - spec/javascripts/fixtures/c32/HITSP_C32v2.5_Rev6_16Sections_Entries_MinimalErrors.xml
   - spec/javascripts/fixtures/ccda/hl7_expected_ccda.xml
   - spec/javascripts/fixtures/ccda/nist_expected_ccda.xml
   - spec/javascripts/fixtures/json/allscripts_ccda_expected_output.json
   - spec/javascripts/fixtures/json/c32_expected_browser_output.json
   - spec/javascripts/fixtures/json/emerge_ccda_expected_output.json
   - spec/javascripts/fixtures/json/hl7_ccda_expected_output.json
   - spec/javascripts/fixtures/json/nist_ccda_expected_output.json
   - spec/javascripts/helpers/ejs.js
   - spec/javascripts/helpers/jasmine-jquery.js
   - spec/javascripts/helpers/jquery.js
   - spec/javascripts/helpers/shared_spec.js
   - spec/javascripts/helpers/underscore.js
   - spec/javascripts/node_specs/bluebutton_spec.js
   - spec/javascripts/node_specs/c32_spec.js
   - spec/javascripts/node_specs/ccda_generator_spec.js
   - spec/javascripts/node_specs/ccda_spec.js

 - Add additional tests to showcase Python functionality if necessary

Rationale
---------

There are tools out there which parse and generate C-CDA, so why have another
one and, furthermore, why port an existing one?

We wanted to write a C-CDA parser for use by our medical researchers and
informaticians. Many of them do not have a background in computer science, but
are familiar with data processing and logic.

These days, it's not difficult to search for how to do something, copy some
code from a question-and-answer site, tweak a few things, and be able to, for
example, pull out valuable information from one flat file format into another
one that can be ingested into a database.

We have heard from these willing researchers-turned-coders who have said the
existing C-CDA tools for Java have too steep of a learning curve. Also, they'd
prefer to use Python since their other tools are in Python.

According to [the ACM][1], as of July 2014, Python is the most popular language for
teaching introductory computer science courses at top-ranked U.S. departments.
Python is written to be easy for newcomers, but still allows coders the ability
to use OOP, lambda functions, parallel programming, and much more.

[1]: http://cacm.acm.org/blogs/blog-cacm/176450-python-is-now-the-most-popular-introductory-teaching-language-at-top-us-universities/fulltext

Having found no active, Python libraries for C-CDA, we started to write our
own. We were able to manipulate the HL7 XML Schemas to generate Python bindings
from the HL7 XML Schemas using [PyXB][], but the resulting code was difficult
to decipher. We then tried [generateDS][], but that failed to generate working
code.

[PyXB]: http://pyxb.sourceforge.net/
[generateDS]: http://www.davekuhlman.org/generateDS.html

We were just about to dive into implementing the giant, 595-page specification
when we found BlueButton.js. It was straigt-forward to use and we could even
call it from Python and use the standard JSON module to convert the JSON into
Python objects.

While that solution (XML to JSON to Python) might work for some, we wanted to
completely remove the dependency on NodeJS, thus we decided to port
BlueButton.js.

