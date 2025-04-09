from datalab_api import DatalabClient
from config import DATA_DIR, QUANTITY, UNIT, COLLECTION_ID
import os
import logging
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

client = DatalabClient("http://aichemy-datalab.ch.ic.ac.uk:5001")


def get_synthesis_constituents(precursor_combination, quantity, unit):
    """
    Get synthesis constituents from the precursor combination.
    Precursor combination is like "A1" to "U34". Separetes the letters and numbers
    then returns the synthesis constituents as a list.
    """

    # Split the precursor into letters and numbers
    tritopic = "".join(filter(str.isalpha, precursor_combination))
    ditopic = "".join(filter(str.isdigit, precursor_combination))

    synthesis_constituents = [
        {
            "item": {
                "chemform": None,
                "immutable_id": None,
                "item_id": "AB-precursor-{}".format(precursor),
                "type": "samples",
            },
            "quantity": quantity,
            "unit": unit,
        }
        for precursor in [tritopic, ditopic]
    ]

    logging.debug(
        "Synthesis constituents for precursor %s: %s",
        precursor_combination,
        synthesis_constituents,
    )
    return synthesis_constituents


def create_entry(combination_map_dict):
    """
    Create an entry in the Datalab with the given combination map dictionary.
    """
    # Get the item ID from the combination map dictionary
    item_id = "{}_{}_{}".format(
        combination_map_dict["experiment_code"],
        combination_map_dict["plate_number"],
        combination_map_dict["formulation_number"],
    )
    logging.debug("Creating entry with item ID: %s", item_id)

    # Get the synthesis constituents from the combination map dictionary
    synthesis_constituents = get_synthesis_constituents(
        combination_map_dict["precursor_combination"],
        QUANTITY,
        UNIT,
    )

    # Create the entry in the Datalab
    json_data = {
        "name": item_id,
        "description": combination_map_dict["precursor_combination"],
        "synthesis_constituents": synthesis_constituents,
    }
    client.create_item(
        item_id=item_id,
        collection_id=COLLECTION_ID,
        item_data=json_data,
    )
    logging.info("Entry created with item ID: %s", item_id)


with open(
    os.path.join(DATA_DIR, "precursor_combination_map_to_exp_data.json"), "r"
) as f:
    combination_map_dict = json.load(f)

for key, entry in combination_map_dict.items():
    create_entry(entry)
