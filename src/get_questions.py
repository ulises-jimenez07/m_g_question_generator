from utils import search

query = "what is the difference between a tuple and a list?"


PROJECT_ID = ""
LOCATION = "global"
answer = search(
    data_store_id="",
    query=query,
    project_id=PROJECT_ID,
    location=LOCATION,
)

print(answer)
