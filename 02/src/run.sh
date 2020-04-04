# create env
python3 -m venv ./

#activate
source ./bin/activate

pip3 install -r requirements.txt
jupyter notebook --no-browser --port 9999 textmining.ipynb