#!/bin/bash
echo Initializing the repo...
cd $(dirname "$(readlink -f "$0")")/../..

python -m _repo.scripts.init
