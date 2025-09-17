#!/bin/bash

MESSAGE=$(cat "$1")
COMMITFORMAT='^(((Merge|Bumping|Revert)|(bugfix|build|chore|ci|docs|feat|feature|fix|other|perf|refactor|revert|style|test)(\(.*\))?\!?: #[0-9]+) .*(\n.*)*)$'

RED="\033[0;91m"
YELLOW="\033[0;93m"
GREEN="\033[0;92m"
DEFAULT="\033[0m"

if ! [[ "$MESSAGE" =~ $COMMITFORMAT ]]; then
  echo -e "${RED}"
  echo "Your commit was rejected due to the invalid commit message..."
  echo ""
  echo "Please use the following format:"
  echo "<type>(optional scope): #id-issue <description>"
  echo ""
  echo "types: feature/feat, fix, chore, refactor, docs, style, test, perf, ci, build and revert"
  echo ""
  echo "Examples:"
  echo "    #1 -> git commit -m 'feature: #1234 feature example comment'"
  echo "    #2 -> git commit -m 'feat(docs): #1234 feature example comment'"
  echo "    #3 -> git commit -m 'fix(ui): #4321 bugfix example comment'"
  echo "    #4 -> git commit -m 'fix!: #4321 chore example comment with possible breaking change'"
  echo "    #5 -> git commit -m 'chore!: #4321 chore example comment with possible breaking change'"
  echo "    #6 -> git commit -m 'refactor(chore)!: #4321 chore example comment with possible breaking change'"
  echo "    #7 -> git commit -m 'chore(fix)!: #4321 drop support for Python 2.6' -m 'BREAKING CHANGE: Some features not available in Python 2.7-.'"
  echo -e "${YELLOW}"
  echo ">> More details on docs/user_guide/CONVENTIONAL_COMMITS.md or https://www.conventionalcommits.org/pt-br/v1.0.0/"
  echo -e "${DEFAULT}"
  exit 1
fi

echo -e "${GREEN}"
echo "Commit message is validated [OK]"
echo -e "${DEFAULT}"
