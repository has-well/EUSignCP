# Add library path to system vars
if [[ ! -v LD_LIBRARY_PATH ]]; then
  echo export LD_LIBRARY_PATH="$PWD/Modules" >> ~/.bashrc
  source ~/.bashrc
fi

# Install PIP and virual env
if [[ ! -d venv ]]; then
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python3 get-pip.py
  pip install virtualenv
  virtualenv -p python3 venv
  rm get-pip.py
fi

source venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

ps aux | grep gunicorn | grep EUSignCP | awk '{ print $2 }' | xargs kill -9

gunicorn -D -w 2 -b 0.0.0.0:5005 api:app
