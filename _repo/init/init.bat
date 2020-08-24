@echo off
echo Initializing the repo...
set script_dir=%~dp0
set script_dir=%script_dir:~0, -1%
cd %script_dir%\..\..

py -m _repo.scripts.init
