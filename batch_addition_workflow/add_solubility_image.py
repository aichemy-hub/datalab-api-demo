from datalab_api import DatalabClient
from config import DATA_DIR
import os
import logging
import json
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

client = DatalabClient("http://aichemy-datalab.ch.ic.ac.uk:5001")


# Upload file
def upload_file(file_path, item_id):
    # Get the absolute path of the file
    file_path = Path(file_path).expanduser().resolve()

    # Upload the file
    client_response = client.upload_file(
        item_id=item_id,
        file_path=file_path,
    )
    logging.info("File uploaded for item: %s", item_id)
    return client_response["file_id"]


def add_turbidity_image_block(combination_map_dict):
    """
    Add an turbidity data block to the Datalab with the given combination map dictionary.
    """
    item_id = "{}_{}_{}".format(
        combination_map_dict["experiment_code"],
        combination_map_dict["plate_number"],
        combination_map_dict["formulation_number"],
    )

    file_path = (
        DATA_DIR
        + combination_map_dict["turbidity_data_path"]
        + "/"
        + "vision_selection.png"
    )
    logging.info("file_path: %s", file_path)
    # Check file exists
    if not os.path.exists(file_path):
        logging.error("File does not exist: %s", file_path)
        return

    file_id = upload_file(file_path, item_id)

    block = client.create_data_block(
        item_id=item_id,
        block_type="media",
        file_ids=file_id,
        display=False,
    )
    logging.info("Turbidity image media block created for item: %s", item_id)


with open(
    os.path.join(DATA_DIR, "precursor_combination_map_to_exp_data.json"), "r"
) as f:
    combination_map_dict = json.load(f)

for key, entry in combination_map_dict.items():
    # Add NMR block for each entry in the combination map dictionary
    add_turbidity_image_block(entry)
