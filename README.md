# EMDB Python Client

A Python client for accessing and interacting with the [Electron Microscopy Data Bank (EMDB)](https://www.ebi.ac.uk/emdb/).  
This package provides an easy-to-use interface to query EMDB entries, access metadata, and download associated files.

## 🚀 Features
- Retrieve EMDB entries by ID
- Query metadata such as resolution, sample description, and related PDBs
- Download associated files (maps, images, metadata)
- Utility models for plotting and file handling
- Access to validation analysis and annotation data

## 📚 Documentation
Full API documentation is available at:  
👉 [https://emdb.readthedocs.io/en/latest/](https://emdb.readthedocs.io/en/latest/)

## 🔧 Installation
COMING SOON

## ✨ Quick Start
```python
from emdb.client import EMDB
from emdb.exceptions import EMDBNotFoundError

client = EMDB()

try:
    # Retrieve an entry by ID
    entry = client.get_entry("EMD-8117")
    print(entry.resolution)
    
    # Access cross-reference annotations
    annotations = entry.get_annotations()
    print(annotations)
    
    # Access validation data and plot FSC
    validation = entry.get_validation()
    validation.plots.fsc.plot()
    
    # Download all files
    entry.download_all_files(output_dir="/tmp/emd1234/")
except EMDBNotFoundError:
    print("Entry not found.")
```

## 🧪 Tests
COMING SOON

## 🛠 Requirements
- Python 3.8+
See [requirements.txt](requirements.txt) for full dependencies.

## 🤝 Contributing
Contributions are welcome!
Feel free to open issues or submit pull requests.

## 📄 License
This project is licensed under the Apache License 2.0.

## 📧 Contact
For questions or feedback, please open an issue on GitHub or contact the maintainers.

