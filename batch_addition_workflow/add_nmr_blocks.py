from datalab_api import DatalabClient
from config import DATA_DIR, QUANTITY, UNIT, COLLECTION_ID
import os
import logging
import json
from pathlib import Path
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

client = DatalabClient("http://aichemy-datalab.ch.ic.ac.uk:5001")


# File must be .zip before uploading so zip it
def zip_file(file_path):
    # Get the absolute path of the file
    file_path = Path(file_path).expanduser().resolve()

    # Create a zip file with the same name as the original file
    zip_file_path = file_path.with_suffix(".zip")

    # Zip the file
    shutil.make_archive(
        zip_file_path.with_suffix(""), "zip", str(file_path.parent), str(file_path.name)
    )
    logging.info("Zipped file: %s", zip_file_path)
    return zip_file_path


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


def add_nmr_block(combination_map_dict):
    """
    Add an NMR block to the Datalab with the given combination map dictionary.
    """
    item_id = "{}_{}_{}".format(
        combination_map_dict["experiment_code"],
        combination_map_dict["plate_number"],
        combination_map_dict["formulation_number"],
    )

    file_path = DATA_DIR + combination_map_dict["NMR_data_path"]

    zip_file_path = zip_file(file_path)
    file_id = upload_file(zip_file_path, item_id)
    # Remove the zip file
    zip_file_path.unlink()
    # Create the NMR block with the file
    block = client.create_data_block(
        item_id=item_id,
        block_type="nmr",
        file_ids=file_id,
        display=False,
    )
    logging.info("NMR block created for item: %s", item_id)


with open(
    os.path.join(DATA_DIR, "precursor_combination_map_to_exp_data.json"), "r"
) as f:
    combination_map_dict = json.load(f)

for key, entry in combination_map_dict.items():
    # Add NMR block for each entry in the combination map dictionary
    add_nmr_block(entry)
