#!/bin/bash
if [ ! ./WholeComponent/venv/Scripts/activate ]; then
echo "started to create virtual environment"
python3 -m venv WholeComponent/venv
source ./WholeComponent/venv/Scripts/activate
echo "started to install required libraries"
pip install -r ./WholeComponent/requirements.txt --no-cache-dir
call deactivate
echo "finished installing libraries"

fi


echo "activating virtual environment"
source ./WholeComponent/venv/Scripts/activate
cd WholeComponent
launcher.sh
deactivate
cd ..