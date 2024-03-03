@echo off
if not exist .\WholeComponent\venv\Scripts\activate (
echo "started to create virtual environment"
python3 -m venv WholeComponent\venv
call .\WholeComponent\venv\Scripts\activate
echo "started to install required libraries"
pip install -r .\WholeComponent\requirements.txt --no-cache-dir
call deactivate
echo "finished installing libraries"
) else (
rem 
)

echo "activating virtual environment"
call call .\WholeComponent\venv\Scripts\activate.bat
cd WholeComponent
call launcher.bat
call deactivate
cd ..