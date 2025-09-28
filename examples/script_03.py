"""Script is designed in order to produce lightweight.

prefixing of commit message
depending on current branch name (e.g. Jira ticket number).

by Roman Gorbatenko
"""

import re
import sys
from pathlib import Path
from subprocess import check_output  # noqa: S404

commit_msg_filepath = sys.argv[1]
branch = (
    check_output(['git', 'symbolic-ref', '--short', 'HEAD'])  # noqa: S607
    .decode('utf-8')
    .strip()
)

regex = r'^[A-Z]{1,9}-[0-9]{1,9}'

found_obj = re.match(regex, branch)

if found_obj:
    prefix = found_obj.group(0)
    with Path(commit_msg_filepath).open('r+', encoding='utf-8') as f:
        commit_msg = f.read()
        if commit_msg.find(prefix) == -1:
            f.seek(0, 0)
            f.write(f'[{prefix}] {commit_msg}')
