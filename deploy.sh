#!/usr/bin/env bash

set -o errexit
set -o pipefail

if [[ $(uname -s) != 'Darwin' ]]; then
	echo This script is meant to be run localy
	echo
	exit 1
fi

remote-sync --no-rsync
ssh bakunin.nl "cd /home/pha/stopnu_bot && ./setup.sh && sudo service uwsgi restart"

