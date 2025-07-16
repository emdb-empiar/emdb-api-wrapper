from emdb.client import EMDBClient

client = EMDBClient()

entry = client.get_entry("EMD-8117")
# entry = client.get_entry("EMD-45474")

annotations = entry.get_annotations()

for m in annotations.macromolecules:
    for annotation in m.gene_ontology:
        print(annotation)

# validation = entry.get_validation()
# print(validation.plots.fsc.plot())
