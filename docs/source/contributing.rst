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
       pip install -e .

4. Create a new branch for your feature or fix:

   .. code-block:: bash

       git checkout -b my-feature

Development Guidelines
----------------------

- Follow **PEP8** and existing code style.
- Include **type hints** and **docstrings** where applicable.
- Keep pull requests focused: one change per PR.
- Write or update **unit tests** for any new functionality.

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
