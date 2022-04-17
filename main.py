import json, os, uuid, sys

import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings


edfi_data = [
    {
        "id": "e313650d5b074fe0a4beb8973043ed29",
        "studentUniqueId": "604822",
        "birthDate": "2008-09-13",
        "firstName": "Lisa",
        "lastSurname": "Woods",
        "middleName": "Sybil",
        "personalTitlePrefix": "Ms",
        "identificationDocuments": [],
        "otherNames": [],
        "personalIdentificationDocuments": [],
        "visas": [],
        "_etag": "5249403375939998898",
    }
]

service_client = DataLakeServiceClient(
    account_url="{}://{}.dfs.core.windows.net".format("https", "dagster"),
    credential=os.getenv("AZURE_STORAGE_KEY"),
)
file_system_client = service_client.get_file_system_client(file_system="dagster")
directory_client = file_system_client.get_directory_client("dagster")

output = ""
for record in edfi_data:
    output = output + json.dumps(record) + "\r\n"

content_settings = ContentSettings(content_type="application/json")
path = f"edfi_api/base_edfi_students/school_year=2022/date_extracted=2022-04-04 03:08:26.492959/extract_type=records/001.json"
file_client = directory_client.create_file(path)
file_client.append_data(data=output, offset=0, length=len(output))
file_client.flush_data(len(output), content_settings=content_settings)
