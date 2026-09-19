"""
List resources with zero word count

When pushing source strings from POT files to Transifex,
now and then it fails silently and updates a resource
with zero strings. This is discovered only when an
updated PO file with a broken state (zero strings) is downloaded.
"""

import argparse
import os
import re
import sys
from transifex.api import transifex_api
from transifex.api.jsonapi import exceptions


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

    # Add annotation only on GitHub Action environment
    annotation = ""
    if os.getenv("CI"):
        annotation = "::error "

    args = parser.parse_args()

    if not (api_token := os.getenv("TX_TOKEN")):
        print(
            f"{annotation}Please set TX_TOKEN environment variable with a Transifex API Token."
        )
        sys.exit(1)

    try:
        transifex_api.setup(auth=api_token)
        ORGANIZATION = transifex_api.Organization.get(slug=args.org)
    except exceptions.JsonApiException:
        print(
            f"{annotation}Transifex auth failed. Is TX_TOKEN set with a valid API token? Do you have access to the organization?"
        )
        sys.exit(1)

    PROJECT = ORGANIZATION.fetch("projects").get(slug=args.project)
    RESOURCES = transifex_api.Resource.filter(project=PROJECT).all()

    zero_word_resources = []
    for resource in RESOURCES:
        if resource.attributes.get("word_count") == 0:
            zero_word_resources.append(resource.attributes.get("slug"))

    if zero_word_resources:
        print(
            f"{annotation}Found {len(zero_word_resources)} resource(s) with word_count equals 0 in project '{args.project}':"
        )
        for resource_slug in zero_word_resources:
            print(f"{annotation}- {resource_slug}")
        sys.exit(1)


if __name__ == "__main__":
    main()
