#!/usr/bin/env python3

import json
import os
import requests
import time

organization_slug = "python-doc"
glossary_slug = "python_global"

token = os.getenv("TX_TOKEN")

# Create a glossary download action
create_url = "https://rest.api.transifex.com/glossaries_async_downloads"
create_headers = {
    "accept": "application/vnd.api+json",
    "content-type": "application/vnd.api+json",
    "authorization": f"Bearer {token}",
}
create_payload = {
    "data": {
        "attributes": {"include_translation_comments": True},
        "relationships": {
            "glossary": {
                "data": {
                    "id": f"o:{organization_slug}:g:{glossary_slug}",
                    "type": "glossaries",
                }
            }
        },
        "type": "glossaries_async_downloads",
    }
}
create_response = requests.post(
    create_url, data=json.dumps(create_payload), headers=create_headers, timeout=30
)
create_response.raise_for_status()
download_id = create_response.json()["data"]["id"]

# Wait for the download to be ready
status_url = f"https://rest.api.transifex.com/glossaries_async_downloads/{download_id}"
status_headers = {
    "accept": "application/vnd.api+json",
    "authorization": f"Bearer {token}",
}
while True:
    status_response = requests.get(
        status_url, headers=status_headers, allow_redirects=False, timeout=30
    )
    status_response.raise_for_status()
    if status_response.status_code == requests.codes.SEE_OTHER:
        break

    status = status_response.json()["data"]["attributes"]["status"]
    match status:
        case "pending" | "processing":
            time.sleep(1.0)
        case _:
            print(status_response.json())
            raise

# Download
location_url = status_response.headers["Location"]
csv_response = requests.get(url=location_url)
with open(f"{glossary_slug}.csv", "wb") as f:
    f.write(csv_response.content)
