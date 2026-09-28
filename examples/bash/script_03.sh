#!/bin/sh

COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2
SHA1=$3

P=$(git status --porcelain | awk '/A\s+content\/articles\// { print $2; }')
if [ "$P" != "" ]
then
        A=$(echo $P | \
                xargs basename -s .rst | \
                cut -d'_' -f2- | \
                awk '{ print "📝️ " $0; }'
        )

        if test -z "$COMMIT_SOURCE"
        then
                /usr/bin/perl -i.bak -pe "print \"$A\n\" if !\$first_line++" "$COMMIT_MSG_FILE"
        fi
fi
