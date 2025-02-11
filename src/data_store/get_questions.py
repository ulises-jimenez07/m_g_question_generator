"""Retrieves answers from the Vertex AI Search engine based on a given query."""

from utils import search

QUERY = "what is the difference between a tuple and a list?"


PROJECT_ID = ""
LOCATION = "global"
DATA_STORE_ID = ""  # Replace with your Datastore ID

answer = search(
    data_store_id=DATA_STORE_ID,
    query=QUERY,
    project_id=PROJECT_ID,
    location=LOCATION,
)

print(answer)
