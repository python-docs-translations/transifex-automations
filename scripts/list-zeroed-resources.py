"""
List resources with zero word count

When pushing source strings from POT files to Transifex,
now and then it fails silently and updates a resource
with zero strings. This is only known when download the
updated PO file with broken state (zero strings)
"""

import argparse
import os
import re
import sys
import requests

def validate_project_slug(slug: str) -> str:
    """Validates project name as 'python-newest' or 'python-3Y' (e.g. python-314)."""
    pattern = r"^(python-newest|python-3\d+)$"
    if not re.match(pattern, slug):
        raise argparse.ArgumentTypeError(
            f"Invalid project name: '{slug}'. Expected 'python-newest' or a versioned name like 'python-314'."
        )
    return slug


def main():
    parser = argparse.ArgumentParser(
        description="List resources with word_count == 0 in a Transifex project."
    )
    parser.add_argument(
        "project",
        type=validate_project_slug,
        help="Project slug in Transifex (e.g.: python-newest or python-314)",
    )
    parser.add_argument(
        "--org",
        default="python-doc",
        help="Organization slug in Transifex (default: python-doc)",
    )

    args = parser.parse_args()

    api_token = os.getenv("TX_TOKEN")
    project_id = f"o:{args.org}:p:{args.project}"

    url = f"https://rest.api.transifex.com/resources?filter[project]={project_id}"
    headers = {
        "accept": "application/vnd.api+json",
        "authorization": f"Bearer {api_token}",
    }

    zero_word_resources = []
    current_url = url


    try:
        while current_url:
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            payload = response.json()

            resources = payload.get("data", [])

            for item in resources:
                attributes = item.get("attributes", {})
                if attributes.get("word_count") == 0:
                    zero_word_resources.append(item)

            # Pagination (if there are more pages)
            current_url = payload.get("links", {}).get("next")

    except requests.exceptions.RequestException as err:
        print(f"ERROR: failed to query Transifex API: {err}")
        sys.exit(1)

    if zero_word_resources:
        print(
            f"\nERROR: Found {len(zero_word_resources)} resource(s) with word_count equals 0 in project '{args.project}':"
        )
        for res in zero_word_resources:
            slug = res.get("attributes", {}).get("slug", "N/A")
            res_id = res.get("id", "N/A")
            print(f" - {slug}")

        sys.exit(1)


if __name__ == "__main__":
    main()
