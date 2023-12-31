#!/bin/bash
# export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# if your python application needs to be run virtual environment, do not export PATH like above, it will override the virtual PATH
# a virtual environment value of PATH="/usr/app/playw-env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# 请先检查 input/古诗接龙.json
name=古诗接龙2
echo $name
python3 break.py -n $name $@

name2=${name}_break
echo $name2
python3 t2s_add.py -n $name2 $@

name3=${name2}_simple_add
echo $name3
# source ~/.bashrc
# please add alias below to your ~/.bashrc
# alias activate_playwenv='source /usr/app/playw-env/bin/activate'
# export PLAYWENV_PATH=/usr/app/playw-env
# activate_playwenv
# to create venv refer to https://docs.python.org/3/library/venv.html
# python3 -m venv /path/to/new/virtual/environment
if [ -f /usr/app/pinyin-env/bin/activate ];then
    source /usr/app/pinyin-env/bin/activate
elif [ -f ~/apps/venvs/pinyin/bin/activate ];then
    source ~/apps/venvs/pinyin/bin/activate    
fi
echo $PATH
pwd
pro_dir=$(dirname $([ -L $0 ] && readlink -f $0 || echo $0))
# pro_dir='/usr/app/enews/us'
# config_dir=$pro_dir/Configs
mkdir -p $pro_dir
# mkdir -p $config_dir
cd $pro_dir
pwd

python3 poet2html_middle.py -n $name3 $@

if [ -f /usr/app/pinyin-env/bin/activate ];then
    deactivate
elif [ -f ~/apps/venvs/pinyin/bin/activate ];then
    deactivate      
fi
echo $PATH


