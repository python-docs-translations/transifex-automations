#!/usr/bin/env python3
# Update versions.txt with latest Python versions and print them

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from packaging.version import parse
from pathlib import Path
import json
import re
import requests
import sys


def get_stable_from_versions(data: dict) -> list:
    """
    Extract bug-fixes and security-fixes Python versions
    from a dict containing all released versions.
    """
    return [k for k, v in data.items() if v["status"] in ["bugfix", "security"]]


def get_from_devguide() -> list:
    """
    Returns a list of bug-fix and security-fix releases from
    a JSON file in devguide, which is used to generate info
    on version.rst for https://devguide.python.org/versions/.

    Returns:
        A list containing the versions.

    Raises:
        JSONDecodeError: If an error occurs when parsing the data as JSON.
    """
    raw_root_url = "https://raw.githubusercontent.com/python/devguide/main"
    url = f"{raw_root_url}/include/release-cycle.json"

    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        exit(f"ERROR: Collect Python versions failed, no connection to: {url}")

    try:
        data = json.loads(r.content.decode(r.apparent_encoding))
        return get_stable_from_versions(data)
    except json.JSONDecodeError:
        sys.exit("ERROR: Unable to parse response as a JSON object")


def get_latest_version() -> str:
    """
    Returns the latest beta or release candidate version of Python,
    in the major.minor version format. If no version is found, or if the
    latest version is either alpha or stable, returns 'None'.

    This function scrapes the Python download page to gather version
    information and selects the latest one.
    Versions that are either alpha or stable are excluded from the results.

    A workaround for https://github.com/python/devguide/issues/998

    Returns:
        str: The latest beta or release candidate version of Python or 'None'
    """
    url = "https://www.python.org/downloads/source/"
    pattern = r"Python 3.[\d]+.[\d]+((rc|b)[\d]+)? "

    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        sys.exit(f"ERROR: Unable to collect data from: {url}")

    soup = BeautifulSoup(r.text, "html.parser")

    versions = []
    for item in soup.find_all("a"):
        m = re.match(pattern, item.get_text())
        if m:
            version = m.group().split(" ")[1]
            versions.append(version)

    latest = max(versions, default=None, key=lambda v: parse(v))

    if parse(latest).pre and parse(latest).pre[0] in ["b", "rc"]:
        latest = re.match(r"3.[\d]+", latest).group()
        return latest
    else:
        return None


def update_versions_file(versions_file: str):
    """
    Writes Python versions in *versions_file* using info gathered by
    the get_from_devguide() and get_latest_version() functions.
    """
    versions = get_from_devguide()
    latest = get_latest_version()
    if latest:
        versions.insert(0, latest)
    with open(versions_file, "w") as f:
        for item in versions:
            f.write(f"{item}\n")
    print("Contents stored:\n", "\n ".join(map(str, versions)))


def get_versions_from_file(file: str) -> list:
    """Read versions file and return then as a list."""
    versions = []
    try:
        with open(file, "r") as f:
            for line in f:
                versions.append(line.strip())
        return versions
    except OSError as e:
        sys.exit(f"ERROR: Failed to open versions file {file}. {e}")


def all(file):
    """List all versions in the version file."""
    print(get_versions_from_file(file))


def current(file):
    """List only the current version, latest listed in the version file."""
    print(get_versions_from_file(file)[0])


def others(file):
    """List all versions but the current in the version file."""
    print(get_versions_from_file(file)[1:])


def generate_pairs(file):
    """List versions in (current, previous) pairs"""
    versions = get_versions_from_file(file)
    version_pairs = [
        {"new": versions[i], "prev": versions[i + 1]} for i in range(len(versions) - 1)
    ]
    print(json.dumps(version_pairs))


def main():
    RUNNABLE_SCRIPTS = (
        "update_versions_file",
        "all",
        "current",
        "others",
        "generate_pairs",
    )

    parser = ArgumentParser()
    parser.add_argument("cmd", choices=RUNNABLE_SCRIPTS)
    options = parser.parse_args()

    script_path = Path(__file__)
    rootdir = script_path.parent.parent.absolute()
    versions_file = str(rootdir) + "/.github/versions.txt"

    eval(options.cmd)(versions_file)


if __name__ == "__main__":
    main()
