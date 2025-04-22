#!/usr/bin/env python
#
# This python file contains utility scripts to manage Python docs translation
# on Transifex.
#
# Inspired by django-docs-translations script by claudep.

from argparse import ArgumentParser
import os
from contextlib import chdir
from dataclasses import dataclass
from difflib import SequenceMatcher
from logging import info
from pathlib import Path
from subprocess import call
import sys
from tempfile import TemporaryDirectory
from typing import Self, Generator, Iterable
from warnings import warn

from polib import pofile
from transifex.api import transifex_api

LANGUAGE = os.getenv("LANGUAGE")
PROJECT_SLUG = 'python-newest'
VERSION = '3.13'

def fetch():
    """
    Fetch translations from Transifex, remove source lines.
    """
    if (code := call("tx --version", shell=True)) != 0:
        sys.stderr.write("The Transifex client app is required.\n")
        exit(code)
    lang = LANGUAGE
    _call(f'tx pull -l {lang} --minimum-perc=1 --force --skip')
    for file in Path().rglob('*.po'):
        _call(f'msgcat --no-location -o {file} {file}')

def _call(command: str):
    if (return_code := call(command, shell=True)) != 0:
        exit(return_code)

def recreate_tx_config():
    """
    Regenerate Transifex client config for all resources.
    """
    with TemporaryDirectory() as directory:
        with chdir(directory):
            _clone_cpython_repo(VERSION)
            _build_gettext()
            with chdir(Path(directory) / 'cpython/Doc/build'):
                _create_txconfig()
                _update_txconfig_resources()
                with open('.tx/config', 'r') as file:
                    contents = file.read()
        contents = contents.replace('./<lang>/LC_MESSAGES/', '')
        with open('.tx/config', 'w') as file:
            file.write(contents)
    warn_about_files_to_delete()

def warn_about_files_to_delete():
    files = list(_get_files_to_delete())
    if not files:
        return
    warn(f'Found {len(files)} file(s) to delete: {", ".join(files)}.')

def _get_files_to_delete():
    with open('.tx/config') as config_file:
        config = config_file.read()
    for file in Path().rglob('*.po'):
        if os.fsdecode(file) not in config:
            yield os.fsdecode(file)

def _clone_cpython_repo(version: str):
    _call(f'git clone -b {version} --single-branch https://github.com/python/cpython.git --depth 1')

def _build_gettext():
    _call("make -C cpython/Doc/ gettext")

def _create_txconfig():
    _call('sphinx-intl create-txconfig')

def _update_txconfig_resources():
    _call(
        f'sphinx-intl update-txconfig-resources --transifex-organization-name python-doc '
        f'--transifex-project-name={PROJECT_SLUG} --locale-dir . --pot-dir gettext'
    )

def _get_tx_token() -> str:
    if os.path.exists('.tx/api-key'):
        with open('.tx/api-key') as f:
            transifex_api_key = f.read()
    else:
        transifex_api_key = os.getenv('TX_TOKEN', '')
    return transifex_api_key

if __name__ == "__main__":
    RUNNABLE_SCRIPTS = ('fetch', 'recreate_tx_config', 'warn_about_files_to_delete')

    parser = ArgumentParser()
    parser.add_argument('cmd', choices=RUNNABLE_SCRIPTS)
    options = parser.parse_args()

    eval(options.cmd)()