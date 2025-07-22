Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_, and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

.. contents::
   :local:
   :depth: 1


Version 0.1.8 (2025-07-22)
--------------------------

Added
^^^^^
- Added support for plotting annotations using `matplotlib`.
- Added support for searching EMDB entries as a pandas DataFrame.


Changed
^^^^^^^
- Improved the `validation` model to expose additional fields.
- Reorganized Sphinx documentation structure.

Fixed
^^^^^
- Fixed issue where empty results caused errors in the client search.

Version 0.1.0 (2025-07-15)
--------------------------

Added
^^^^^
- Initial release of the EMDB Python Client.
- Support for fetching EMDB entries by ID.
- Downloading of structure maps and related files.
- Access to validation data and annotation cross-references.
- Sphinx documentation with API reference.

