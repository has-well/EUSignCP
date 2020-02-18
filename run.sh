export LD_LIBRARY_PATH="$PWD/Modules"

[ ! -d "venv" ] && virtualenv -p python3 venv

source venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

python3 api.py
