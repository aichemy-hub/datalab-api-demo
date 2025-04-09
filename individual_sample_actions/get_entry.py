from datalab_api import DatalabClient

client = DatalabClient("http://aichemy-datalab.ch.ic.ac.uk:5001")
item = client.get_item(
    item_id="AB-02-009-02_43",
    display=True,
    load_blocks=True,
)

print(item["synthesis_constituents"])
