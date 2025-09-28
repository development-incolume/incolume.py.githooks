"""Script examplo."""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pathlib",
# ]
# ///
import re
import sys
from pathlib import Path
from subprocess import check_output  # noqa: S404

commit_msg_filepath = sys.argv[1]

branch = check_output(['git', 'symbolic-ref', '--short', 'HEAD']).strip()  # noqa: S607
regex = r'(feature|hotfix)\/(\w+-\d+)'
if re.match(regex, branch):
    issue = re.match(regex, branch).group(2)
    with Path(commit_msg_filepath).open('r+', encoding='utf-8') as fh:
        commit_msg = fh.read()
        fh.seek(0, 0)
        fh.write(f'[{issue}] {commit_msg}')
elif branch not in {'master', 'dev'}:
    print('Incorrect branch name')  # noqa: T201
    sys.exit(1)
