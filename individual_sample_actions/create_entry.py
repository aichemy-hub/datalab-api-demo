from datalab_api import DatalabClient

client = DatalabClient("http://aichemy-datalab.ch.ic.ac.uk:5001")

synthesis_constituents = [
    {
        "item": {
            "chemform": None,
            "immutable_id": None,
            "item_id": "AB-precursor-U",
            "type": "samples",
        },
        "quantity": 0.0092,
        "unit": "M",
    }
]

json_data = {
    "name": "AB-02-005-01_01",
    "description": "Test entry",
    "synthesis_constituents": synthesis_constituents,
}

client.create_item(
    item_id="AB-02-005-01_01",
    collection_id="AB-AUTO-CAGES",
    item_data=json_data,
)
