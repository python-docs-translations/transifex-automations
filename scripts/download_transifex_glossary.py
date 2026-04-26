#!/usr/bin/env python3

import os
import sys
import time
import logging
import requests

level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

API_BASE = "https://rest.api.transifex.com"


def fail(msg: str):
    logger.error(msg)
    sys.exit(1)


def get_env(name: str, default=None, required=False):
    value = os.getenv(name, default)
    if required and not value:
        fail(f"Missing environment variable: {name}")
    return value


def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        fail(f"Invalid integer for {name}: {value}")


def request_export(token: str, glossary_id: str) -> str:
    url = f"{API_BASE}/glossaries_async_downloads"

    headers = {
        "accept": "application/vnd.api+json",
        "content-type": "application/vnd.api+json",
        "authorization": f"Bearer {token}",
    }

    payload = {
        "data": {
            "attributes": {
                "include_translation_comments": True,
            },
            "type": "glossaries_async_downloads",
            "relationships": {
                "glossary": {
                    "data": {
                        "type": "glossaries",
                        "id": glossary_id,
                    }
                }
            },
        }
    }

    r = requests.post(url, json=payload, headers=headers)
    if r.status_code not in (200, 201, 202):
        fail(f"Failed to request export: {r.status_code} {r.text}")

    data = r.json()
    return data["data"]["id"]


def is_csv_response(response: str) -> bool:
    content_type = response.headers.get("Content-Type", "")
    if "text/csv" in content_type or "application/csv" in content_type:
        return True
    return False


def download_glossary_content(
    token: str, download_id: str, timeout: int, interval: int
):
    url = f"{API_BASE}/glossaries_async_downloads/{download_id}"

    headers = {
        "accept": "application/vnd.api+json",
        "authorization": f"Bearer {token}",
    }

    start = time.time()

    while True:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            fail(f"Failed to check status: {r.status_code} {r.text}")

        if is_csv_response(r):
            return r.text

        elapsed = time.time() - start
        if elapsed > timeout:
            fail(f"Timeout waiting for download ({elapsed:.1f}s > {timeout}s)")

        time.sleep(interval)


def write_file(content: str, output: str):
    output_dir = os.path.dirname(output) or "."

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        fail(f"Failed to create output directory '{output_dir}': {e}")

    try:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        fail(f"Failed to write output file '{output}': {e}")


def main():
    token = get_env("TX_TOKEN", required=True)
    glossary_id = get_env("GLOSSARY_ID", required=True)
    output = get_env("OUTPUT_FILE", "glossary.csv")

    timeout = get_int_env("EXPORT_TIMEOUT", 300)
    interval = get_int_env("EXPORT_INTERVAL", 10)

    logger.info(f"Using timeout={timeout}s interval={interval}s")

    logger.info("Requesting export...")
    download_id = request_export(token, glossary_id)

    logger.info(f"Download ID: {download_id}")
    logger.info("Waiting for content to be available...")

    csv_content = download_glossary_content(token, download_id, timeout, interval)

    logger.info(f"Writing content to '{output}'")
    write_file(csv_content, output)
    logger.info("Output file written successfully.")


if __name__ == "__main__":
    main()
