from emdb.client import EMDBClient

client = EMDBClient()
entry = client.get_entry("EMD-8117")
validation = entry.get_validation()
print(validation.plots.rawmap_mmcif[0].plot())
