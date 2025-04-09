from datalab_api import DatalabClient

client = DatalabClient("http://aichemy-datalab.ch.ic.ac.uk:5001")

block = client.create_data_block(
    item_id="AB-02-005-01_01",
    block_type="nmr",
    file_ids="67f538b23f91fe8acff4b738",
    display=False,
)
