Quickstart
==========

Installation
------------

Install the latest version from PyPI:

.. code-block:: bash

    pip install emdb

Basic Usage
-----------

Here's how to get started with the EMDB client:


.. code-block:: python

   from emdb.client import EMDB
   client = EMDB()
   entry = client.get_entry("EMD-8117")
   print(entry.method)
   print(entry.resolution)
   print(entry.related_pdb_ids)

Output:

.. code-block:: text

    singleParticle
    2.95
    [{'instance_type': 'pdb_reference', 'pdb_id': '5irx', 'relationship': {'in_frame': 'FULLOVERLAP'}}]

This code snippet demonstrates how to retrieve an entry from the EMDB database using the EMDB client. The `get_entry` method fetches the entry with the specified ID, and you can access various attributes of the entry, such as its resolution.

Next Steps
----------
- See the :doc:`API Reference <api/index>` for all methods and models.