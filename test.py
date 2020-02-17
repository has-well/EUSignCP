import json
import base64
from EUSignCP import EULoad, EUUnload, EUGetInterface

with open('Modules/cert/CAs.json') as cert:
    certs = json.load(cert)

binfile = open('3188718600R19K2A.xlsx.p7s', 'rb').read()
infile = open('signed.pdf', 'rb').read()

EULoad()
inf = EUGetInterface()
inf.Initialize()

try:

    signs = []
    #inf.GetSignsCount(pszSign=None, pbSign=binfile, dwSignLength=len(binfile), pdwCount=signs)
    inf.GetFileSignsCount(pszFileNameWithSign='statut.pdf', pdwCount=signs)
    print('Signs:', signs)
    signer = []
    cert = []
    inf.GetFileSignerInfo(dwSignIndex=0, pszFileNameWithSign='3188718600R19K2A.xlsx.p7s', ppInfo=signer, ppbCertificate=None)
    #signer = base64.b64decode(signer[0])
    print(signer)
    print(cert)
finally:
    inf.Finalize()

EUUnload()



#
