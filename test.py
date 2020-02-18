import requests
from pathlib import Path


filename = '3188718600R19K2A.xlsx.p7s'
with open(filename, 'rb') as f:
    filebin = f.read()

r = requests.post('http://localhost:5005/GetSignsCount', data=filebin)
print(r.json())

r = requests.post('http://localhost:5005/GetSignerInfo', data=filebin)
print(r.json())

r = requests.post('http://localhost:5005/GetDataFromSignedData', data=filebin)
Path(filename[:-4]).write_bytes(r.content)
print(r.status_code)
