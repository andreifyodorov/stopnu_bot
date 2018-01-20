#!/usr/bin/env bash

set -o errexit
set -o pipefail

if [[ $(uname -s) != 'Darwin' ]]; then
	echo This script is meant to be run localy
	echo
	exit 1
fi

. .ve.stopnu_bot/bin/activate

# run ssh tunnel
ssh -N -R 8080:localhost:5000 bakunin.nl &
trap "kill %1" EXIT

# run local server
FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run