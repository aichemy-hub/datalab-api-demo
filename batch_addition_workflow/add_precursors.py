from datalab_api import DatalabClient
import os
import logging
import json
from config import COLLECTION_ID

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

client = DatalabClient("http://aichemy-datalab.ch.ic.ac.uk:5001")

with open("precursors.json", "r") as f:
    precursors = json.load(f)

# add tritopic and ditopic precursors to Datalab


def add_precursors(precursor_type):
    """
    Add precursors to Datalab.
    """
    for key, val in precursors[precursor_type].items():
        client.create_item(
            item_id="AB-precursor-{}".format(key),
            collection_id=COLLECTION_ID,
            item_data={
                "description": "{} precursor".format(precursor_type),
                "name": val,
            },
        )
        logging.info("Created precursor %s", val)


for precursor_type in precursors.keys():
    add_precursors(precursor_type)
