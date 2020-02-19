import sys
sys.path.append('../')
import io

import requests
from pathlib import Path

from EUSignCP import *

# Load digital sign library
EULoad()
intF = EUGetInterface()
intF.Initialize()

tmp = {}
intF.GetFileStoreSettings(tmp)
print(tmp)
tmp = {}
intF.GetOCSPSettings(tmp)
print(tmp)
tmp = {}
intF.GetLDAPSettings(tmp)
print(tmp)

filename = '3188718600R19K2A.xlsx.p7s'
with open(filename, 'rb') as f:
    filebin = f.read()


def GetSignsCount(signedbin):
    signs_count = []
    try:
        intF.GetSignsCount(None, signedbin, len(signedbin), signs_count)
    except Exception as e:
        return repr(e)
    return signs_count

#print('OK', GetSignsCount(filebin))


def GetSignerInfo(signedbin):
    signer_info = {}
    try:
        intF.GetSignerInfo(0, None, signedbin, len(signedbin), signer_info, None)
    except Exception as e:
        return repr(e)
    return signer_info

#print('OK', GetSignerInfo(filebin).get('pszSubjFullName'))


def GetDataFromSignedData(signedbin):
    unsignedbin = []
    try:
        intF.GetDataFromSignedData(None, signedbin, len(signedbin), unsignedbin)
    except Exception as e:
        return repr(e)
    return unsignedbin[0]

#Path(filename[:-4]).write_bytes(GetDataFromSignedData(filebin))
#print('OK')


def VerifyDataInternal(signedbin):
    data = {}
    sign = {}
    try:
        intF.VerifyDataInternal(None, signedbin, len(signedbin), data, sign)
    except Exception as e:
        return repr(e)
    return [data, sign]

print('OK', VerifyDataInternal(filebin))

intF.Finalize()
EUUnload()

'''
import requests
import re
import time
for i in range(1, 150):
    r = requests.get('https://czo.gov.ua/ca-registry-details', params={'type': 0, 'id': i})
    certs = re.findall('/download/cacertificates/.+\.cer', r.text)
    for ce in certs:
        ce = re.sub('\s', '', ce)
        resp = requests.get('https://czo.gov.ua' + ce)
        with open('../Modules/cert/' + link.split('/')[-1], 'wb') as f:
            f.write(resp.content)
        print(ce.split('/')[-1]) 
'''