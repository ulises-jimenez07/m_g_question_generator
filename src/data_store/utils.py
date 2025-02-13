"""Utilities for interacting with Vertex AI Discovery Engine Data Stores."""

from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import (  # Import more specific exceptions
    DeadlineExceeded,
    GoogleAPIError,
    InternalServerError,
    ResourceExhausted,
)
from google.cloud import discoveryengine as ds


def create_data_store(project_id: str, location: str, data_store_name: str, data_store_id: str):
    """Creates a data store."""

    client_options = ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")

    client = ds.DataStoreServiceClient(client_options=client_options)

    data_store = ds.DataStore(
        display_name=data_store_name,
        industry_vertical=ds.IndustryVertical.GENERIC,
        content_config=ds.DataStore.ContentConfig.CONTENT_REQUIRED,
    )

    operation = client.create_data_store(
        request=ds.CreateDataStoreRequest(
            parent=client.collection_path(project_id, location, "default_collection"),
            data_store=data_store,
            data_store_id=data_store_id,
        )
    )

    try:
        operation.result(timeout=90)
        print(f"[ SUCCESS ] Datastore {data_store_name} created.")
    except GoogleAPIError as e:  # Catch Google API specific errors
        print(f"[ PROCESS ] Google API Error: {e}")  # More specific message
        if e.code == 409:  # Example: Check for specific error code (e.g., already exists)
            print("[ PROCESS ] Datastore might already exist.")
    except DeadlineExceeded as e:
        print(f"[ PROCESS ] Operation timed out: {e}")
    except InternalServerError as e:
        print(f"[ PROCESS ] Internal Server Error: {e}")
    except ResourceExhausted as e:
        print(f"[ PROCESS ] Resource Exhausted: {e}")


def import_documents(
    project_id: str,
    location: str,
    data_store_id: str,
    gcs_uri: str,
):
    """Imports documents into a data store."""

    client_options = ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")

    client = ds.DocumentServiceClient(client_options=client_options)

    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    source_documents = [f"{gcs_uri}/*"]

    request = ds.ImportDocumentsRequest(
        parent=parent,
        gcs_source=ds.GcsSource(input_uris=source_documents, data_schema="content"),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=ds.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    try:
        operation = client.import_documents(request=request)
        operation.result()
        print("[ SUCCESS ] Documents imported.")
    except GoogleAPIError as e:
        print(f"[ FAILED ] Google API operation failed: {e}")
    except DeadlineExceeded as e:
        print(f"[ FAILED ] Operation timed out: {e}")
    except InternalServerError as e:
        print(f"[ FAILED ] Internal Server Error: {e}")
    except ResourceExhausted as e:
        print(f"[ FAILED ] Resource Exhausted: {e}")


def create_engine(project_id: str, location: str, data_store_name: str, data_store_id: str):
    """Creates a search engine."""

    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com") if location != "global" else None
    )
    client = ds.EngineServiceClient(client_options=client_options)

    config = ds.Engine.SearchEngineConfig(search_tier="SEARCH_TIER_ENTERPRISE", search_add_ons=["SEARCH_ADD_ON_LLM"])

    engine = ds.Engine(
        display_name=data_store_name,
        solution_type="SOLUTION_TYPE_SEARCH",
        industry_vertical="GENERIC",
        data_store_ids=[data_store_id],
        search_engine_config=config,
    )

    request = ds.CreateEngineRequest(
        parent=ds.DataStoreServiceClient.collection_path(project_id, location, "default_collection"),
        engine=engine,
        engine_id=engine.display_name,
    )

    try:
        operation = client.create_engine(request=request)
        operation.result(timeout=90)
        print("[ SUCCESS ] Vertex Search App created.")
    except GoogleAPIError as e:
        print(f"[ PROCESS ] Google API Error: {e}")
    except DeadlineExceeded as e:
        print(f"[ PROCESS ] Operation timed out: {e}")
    except InternalServerError as e:
        print(f"[ PROCESS ] Internal Server Error: {e}")
    except ResourceExhausted as e:
        print(f"[ PROCESS ] Resource Exhausted: {e}")


def search(data_store_id: str, query: str, project_id: str, location: str):
    """Performs a search."""

    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com") if location != "global" else None
    )

    client = ds.SearchServiceClient(client_options=client_options)

    serving_config = client.serving_config_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        serving_config="default_config",
    )

    content_search_spec = {
        "extractive_content_spec": {
            "max_extractive_answer_count": 3,
            "max_extractive_segment_count": 3,
            "return_extractive_segment_score": True,
        },
    }

    request = ds.SearchRequest(
        serving_config=serving_config,
        query=query,
        query_expansion_spec={"condition": "AUTO"},
        spell_correction_spec={"mode": "AUTO"},
        content_search_spec=content_search_spec,
        page_size=1,
    )

    try:
        response = client.search(request)
        for r in response.results[0].document.derived_struct_data.get("extractive_segments"):
            return r.get("content")
    except (IndexError, AttributeError, KeyError) as e:
        print(f"[ FAILED ] Could not extract content: {e}")
    except GoogleAPIError as e:
        print(f"[ FAILED ] Search request failed: {e}")
    except DeadlineExceeded as e:
        print(f"[ FAILED ] Search timed out: {e}")
    except InternalServerError as e:
        print(f"[ FAILED ] Internal Server Error during search: {e}")
    except ResourceExhausted as e:
        print(f"[ FAILED ] Search request exhausted resources: {e}")
    return "No answer found"
