# Welcome to BlueButton.js

BlueButton.js is a JavaScript library for working with Blue Button data. A simple and consistent API is exposed from a C32 or CCDA continuity of care document in XML.

## Getting Started

Start by creating a Blue Button document object by passing the CCD XML (C32 or CCDA) to `BlueButton`:

```javascript
var bb = BlueButton(xml);
```

The document object, `bb` in this example, now exposes all CCD data through a simple and consistent interface. Each section of the document can be accessed using its associated method.

## Document Sections

All health records have the following sections:

- Allergies
- Demographics
- Discharge
- Encounters
- Functions
- History
- Immunizations
- Labs
- Medications
- Plan
- Problems
- Procedures
- Vitals

Each section can be accessed by using methods named after the sections. For example, get a list of all medications, use:

```javascript
bb.medications();
```

An array containing all medications in the patient record is returned.

## Filters

Filters are objects that can be used to access a subset of the document section. Each section method accepts different filters.

Example: These options will return medications from 2012 to 2013 that are active:

```javascript
bb.medications({
  from: 2012,
  to: 2013,
  status: "active"
});
```

## Other Methods

TODO: Consider other methods supported by the Blue Button document object.

```javascript
bb.toJSON();  // Get the entire record as JSON

bb.xml();     // Get the source XML element
bb.xmlDOM();
bb.dom();

bb.all();     // Get the entire health record
bb.everything();
```



