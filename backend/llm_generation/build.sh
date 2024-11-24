#!/bin/bash

pip install -r ../requirements.txt
cd Liger-Kernel
python3 -m pip install -e .[transformers] --user
cd ..
