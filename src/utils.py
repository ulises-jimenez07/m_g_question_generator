from google.cloud import storage
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine as ds


def create_data_store(
    project_id: str, location: str, data_store_name: str, data_store_id: str
):

    client_options = ClientOptions(
        api_endpoint=f"{location}-discoveryengine.googleapis.com"
    )

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
        response = operation.result(timeout=90)
    except:
        print("[ PROCESS ]long-running operation")
    else:
        print(f"[ SUCCESS ] Datastore {data_store_name} created.")


def import_documents(
    project_id: str,
    location: str,
    data_store_id: str,
    gcs_uri: str,
):

    client_options = ClientOptions(
        api_endpoint=f"{location}-discoveryengine.googleapis.com"
    )

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
        response = operation.result()
    except:
        print("[ FAILED ] Operation failed")
    else:
        print(f"[ SUCCESS ] Documents imported.")


def create_engine(
    project_id: str, location: str, data_store_name: str, data_store_id: str
):

    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )
    client = ds.EngineServiceClient(client_options=client_options)

    config = ds.Engine.SearchEngineConfig(
        search_tier="SEARCH_TIER_ENTERPRISE", search_add_ons=["SEARCH_ADD_ON_LLM"]
    )

    engine = ds.Engine(
        display_name=data_store_name,
        solution_type="SOLUTION_TYPE_SEARCH",
        industry_vertical="GENERIC",
        data_store_ids=[data_store_id],
        search_engine_config=config,
    )

    request = ds.CreateEngineRequest(
        parent=ds.DataStoreServiceClient.collection_path(
            project_id, location, "default_collection"
        ),
        engine=engine,
        engine_id=engine.display_name,
    )

    try:
        operation = client.create_engine(request=request)
        response = operation.result(timeout=90)
    except:
        print("[ PROCESS ]long-running operation")
    else:
        print(f"[ SUCESS ] Vertex Search App created.")


def search(data_store_id: str, query: str, project_id: str, location: str):

    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
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

    response = client.search(request)

    top_response = ""

    try:
        for r in response.results[0].document.derived_struct_data.get(
            "extractive_segments"
        ):
            top_response = r.get("content")
            break
    except:
        top_response = "No answer found"
    finally:
        return top_response
