from datalab_api import DatalabClient
import pandas as pd

client = DatalabClient("http://aichemy-datalab.ch.ic.ac.uk:5001")

items = client.search_items(
    query="AB-AUTO_CAGES",
)

df = pd.DataFrame(items)
print(df)
