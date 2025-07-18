from emdb.client import EMDB

client = EMDB()

entry = client.get_entry("EMD-8117")
# entry = client.get_entry("EMD-45474") # Example with annotations
# entry = client.get_entry("EMD-45369")  # Example with additional maps
# entry = client.get_entry("EMD-1016")  # Example with slices, model and figures
# entry = client.get_entry("EMD-46893")  # Example with masks
# entry = client.get_entry("EMD-3434")  # Example with masks details

# file = entry.pdb_models[0]
# file.download("/Users/neli/Downloads/")

# print(entry.deposited_files)
# entry.download_all_files("/Users/neli/Downloads/test_wrapper/")

# annotations = entry.get_annotations()
#
# for m in annotations.macromolecules:
#     for annotation in m.gene_ontology:
#         print(annotation)

# validation = entry.get_validation()
# print(validation.plots.fsc.plot())
