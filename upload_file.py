from datalab_api import DatalabClient
from pathlib import Path
import shutil

FILE_PATH = "~/Downloads/14078250/nmr/AB-02-005/01/10"

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

    return zip_file_path


# Upload the file
def upload_file(file_path):
    # Get the absolute path of the file
    file_path = Path(file_path).expanduser().resolve()

    # Upload the file
    client.upload_file(
        item_id="AB-02-005-01_01",
        file_path=file_path,
    )


if __name__ == "__main__":
    # Zip the file
    zip_file_path = zip_file(FILE_PATH)

    # Upload the file
    upload_file(zip_file_path)
    # Remove the zip file
    zip_file_path.unlink()
