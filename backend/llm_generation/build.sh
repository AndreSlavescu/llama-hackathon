#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pip install -r "$SCRIPT_DIR/../requirements.txt"
cd "$SCRIPT_DIR/Liger-Kernel"
python3 -m pip install -e .[transformers] --user
cd ..
