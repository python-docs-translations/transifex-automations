#!/usr/bin/env python

import configparser
import json
import os
import re
from argparse import ArgumentParser
from pathlib import Path

from transifex.api import transifex_api

ORG_SLUG = "python-doc"
PROJ_SLUG = "python-newest"


def _get_tx_token() -> str:
    """
    Try to get Transifex API token from some sources.
    First try TX_TOKEN environment variable, then ~/.transifexrc file.
    """
    token = ""
    if 'TX_TOKEN' in os.environ:
        token = os.environ['TX_TOKEN']
    else:
        config = configparser.ConfigParser()
        config.read(f"{os.path.expanduser('~')}/.transifexrc")
        for section in config.sections():
            if section in ["https://www.transifex.com", "https://app.transifex.com"]:
                token = config[section]["token"]
                break
    return token


def create_translation_project(new_project_version: str) -> str:
    """
    Creates a new Transifex project with versioned name based on python-newest
    project_slug = slug of the translation project being created
    project_name = name of the translation project being created 
    p.* = Reference to the current python-newest project
    r.* = Reference to a resource from from python-newest project  
    """
    p = PROJECT

    project_slug = 'python-' + new_project_version.replace('.', '')
    project_name = f'Python {new_project_version}'
    print(f'Creating project: {project_name}')

    versioned_project = transifex_api.Project.create(
        description=project_name,
        homepage_url=p.attributes.get('homepage_url'),
        instructions_url=p.attributes.get('instructions_url'),
        license=p.attributes.get('license'),
        long_description=p.attributes.get('long_description'),
        machine_translation_fillup=p.attributes.get('machine_translation_fillup'),
        name=project_name,
        private=p.attributes.get('private'),
        repository_url=p.attributes.get('repository_url'),
        slug=project_slug,
        tags=p.attributes.get('tags'),
        team=p.fetch('team'),
        organization=ORGANIZATION,
        source_language=p.fetch('source_language'),
        translation_memory_fillup=p.attributes.get('translation_memory_fillup'),
    )

    print(f'{project_slug} created')


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        'version',
        help='Python version currently assigned to python-newest (only major and minor, X.Y)'
    )
    args = parser.parse_args()

    transifex_api.setup(auth=_get_tx_token())
    ORGANIZATION = transifex_api.Organization.get(slug=ORG_SLUG)
    PROJECT = ORGANIZATION.fetch('projects').get(slug=PROJ_SLUG)
    RESOURCES = transifex_api.Resource.filter(project=PROJECT).all()

    project_version = args.version

    create_translation_project(project_version)
