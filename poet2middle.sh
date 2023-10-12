#!/bin/bash
# export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# if your python application needs to be run virtual environment, do not export PATH like above, it will override the virtual PATH
# a virtual environment value of PATH="/usr/app/playw-env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# 请先检查 input/古诗接龙.json
python3 break.py
python3 t2s_add.py


