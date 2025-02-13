"""This script creates a Vertex AI Datastore and imports documents from GCS."""

from utils import (
    create_data_store,
    create_engine,
    import_documents,
)

PROJECT_ID = ""
LOCATION = "global"

DATA_STORE_NAME = "mg-ai-questions"
DATA_STORE_ID = f"{DATA_STORE_NAME}-id"
GCS_URI = "gs://bucket"

# Create Data Store
create_data_store(
    project_id=PROJECT_ID,
    location=LOCATION,
    data_store_name=DATA_STORE_NAME,
    data_store_id=DATA_STORE_ID,
)

# Import Documents
import_documents(
    project_id=PROJECT_ID,
    location=LOCATION,
    data_store_id=DATA_STORE_ID,
    gcs_uri=(GCS_URI),
)

# Create Vertex Search Engine App
create_engine(
    project_id=PROJECT_ID,
    location=LOCATION,
    data_store_name=DATA_STORE_NAME,
    data_store_id=DATA_STORE_ID,
)
