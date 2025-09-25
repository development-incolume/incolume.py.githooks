"""Script portado de Python2.7 para Python3."""
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "icecream",
#     "rich",
# ]
# ///

# ruff: noqa: E501 PLR2004 PTH123 S404 S607 SIM108

import re
import sys
from subprocess import check_output

import rich

issue_number, feature_number = None, None

# Collect the parameters
commit_msg_filepath = sys.argv[1]
if len(sys.argv) > 2:
    commit_type = sys.argv[2]
else:
    commit_type = ''

if len(sys.argv) > 3:
    commit_hash = sys.argv[3]
else:
    commit_hash = ''
rich.print(
    f'prepare-commit-msg: File: {commit_msg_filepath}\nType: {commit_type}\nHash: {commit_hash}'
)

# Figure out whrich.printh branch we're on
branch = (
    check_output([
        'git',
        'symbolic-ref',
        '--short',
        'HEAD',
    ])
    .strip()
    .decode()
)
rich.print(f"prepare-commit-msg: On branch '{branch}'")

# Populate the commit message with the issue #, if there is one
if branch.startswith('issue-'):
    rich.print("prepare-commit-msg: Oh hey, it's an issue branch.")
    result = re.match(r'issue-(.*)', branch)

    if result:
        issue_number = result.group(1)

with open(commit_msg_filepath, 'rb+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(
        f'ISSUE-{issue_number} {content}'.encode()
        if issue_number
        else f'{content}'.encode()
    )

# Populate the commit message with the feature #, if there is one
if branch.startswith('feature-'):
    rich.print("prepare-commit-msg: Oh hey, it's an feature branch.")
    result = re.match(r'feature-(.*)', branch)
    if result:
        feature_number = result.group(1)

with open(commit_msg_filepath, 'rb+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(
        f'FEATURE-{feature_number} {content}'.encode()
        if feature_number
        else f'{content}'.encode()
    )
