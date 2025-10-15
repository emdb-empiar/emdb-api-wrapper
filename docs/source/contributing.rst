Contributing
============

Thank you for your interest in contributing to the EMDB Python Client!
We welcome contributions in the form of bug reports, feature requests, documentation improvements, and code enhancements.

.. contents::
   :local:
   :depth: 2

Getting Started
---------------

To contribute, you will need to:

1. Fork the repository on `GitHub <https://github.com/emdb-empiar/emdb-api-wrapper>`_.
2. Clone your fork:

   .. code-block:: bash

       git clone git@github.com/your-username/emdb-api-wrapper.git
       cd emdb-api-wrapper

3. Set up a virtual environment and install the package in editable mode:

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate
       pip install -e ".[test]"

4. Create a new branch for your feature or fix:

   .. code-block:: bash

       git checkout -b my-feature

Development Guidelines
----------------------

- Follow **PEP8** and existing code style.
- Include **type hints** and **docstrings** where applicable.
- Keep pull requests focused: one change per PR.
- Write or update **unit tests** for any new functionality.

Testing
-------

This project uses pytest for unit testing. Before submitting a pull request, make sure all tests pass:

.. code-block:: bash

    # Run all tests
    pytest

    # Run tests with verbose output
    pytest -v

    # Run tests with coverage report
    pytest --cov=emdb --cov-report=html

    # Run specific test file
    pytest tests/test_client.py

    # Run specific test class or function
    pytest tests/test_client.py::TestEMDBClient::test_get_entry_success

Test files are located in the `tests/` directory. Each module has a corresponding test file:

- `tests/test_client.py` - Tests for the EMDB client
- `tests/test_exceptions.py` - Tests for exception classes
- `tests/test_utils.py` - Tests for utility functions
- `tests/test_search.py` - Tests for search and lazy entry loading

When adding new features, please include comprehensive unit tests that cover:

- Normal operation cases
- Edge cases
- Error conditions

Documentation
-------------

Documentation is built using Sphinx. To build it locally:

.. code-block:: bash

    sphinx-build -b html docs/source docs/build/html

Then open `docs/build/html/index.html` in your browser.

Submitting a Pull Request
-------------------------

1. Push your changes to your fork:

   .. code-block:: bash

       git push origin my-feature

2. Open a Pull Request on GitHub.
3. The maintainers will review your PR. Please respond to any feedback.

Code of Conduct
---------------

All contributors are expected to follow our Code of Conduct.
Be respectful, collaborative, and inclusive in all interactions.

---

Happy coding and thank you for making the EMDB Python Client better!
