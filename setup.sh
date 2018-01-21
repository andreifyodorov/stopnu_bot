#!/usr/bin/env bash

set -o errexit
set -o pipefail

app=$(basename $(pwd))

if [[ $(uname -a) == Darwin ]]; then
	echo
else
	virtualenv=$HOME/virtualenv/$app
	rm -rf $virtualenv
	mkdir -p $virtualenv
	virtualenv $virtualenv
	. $virtualenv/bin/activate
	pip install -r requirments.txt
fi