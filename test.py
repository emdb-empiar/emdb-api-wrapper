from emdb.client import EMDBClient

client = EMDBClient()

# entry = client.get_entry("EMD-8117")
entry = client.get_entry("EMD-45474")

annotations = entry.get_annotations()

for m in annotations.supramolecules:
    print(str(m))

# TODO: Check if EMDBAnnotation only contains the info that make sense for that type
# TODO: Another option is to extend EMDBAnnotation class in subclasses for each type

# validation = entry.get_validation()
# print(validation.plots.fsc.plot())
