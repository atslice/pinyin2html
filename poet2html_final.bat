@echo off

cd J:\AppsWindows\Coding\WinPython\WPy64-310111-venv\pinyin\Scripts

activate.bat

set name=古诗接龙1
REM # name=古诗接龙2
REM name2=${name}_break
REM name3=${name2}_simple_add
REM name4=${name3}_pinyin
set name2=%name%_break
set name3=%name2%_simple_add
set name4=%name3%_pinyin
echo %name4%

python poet2html_final.py -n %name4%

REM deactivate.bat

pause



