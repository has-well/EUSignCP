import io
from flask import Flask, request, jsonify, send_file, url_for
from EUSignCP import *

T, F = True, False # R style
EU_OCSP_SETTINGS = {'bUseOCSP': T, 'bBeforeStore': T, 'szAddress': '193.111.173.6', 'szPort': '443'}
EU_LDAP_SETTINGS = {'bUseLDAP': T, 'szAddress': 'ca.ksystems.com.ua', 'szPort': '389', 'bAnonymous': T}#, 'szUser': '', 'szPassword': ''}

EU_FILE_STORE_SETTINGS = {'szPath': './Modules/cert', 'bCheckCRLs': T, 'bAutoRefresh': T, 'bOwnCRLsOnly': F,
                          'bFullAndDeltaCRLs': F, 'bAutoDownloadCRLs': T, 'bSaveLoadedCerts':T, 'dwExpireTime': 86400}

EULoad()
intF = EUGetInterface()
intF.Initialize()
intF.SetFileStoreSettings(pszPath=EU_FILE_STORE_SETTINGS)
intF.SetOCSPSettings(bUseOCSP=EU_OCSP_SETTINGS)
intF.SetLDAPSettings (bUseLDAP=EU_LDAP_SETTINGS)


app = Flask(__name__)

@app.route('/')
def main():
    resp = 'Entry poins for binary POST:<br>'
    resp += 'http://' + request.host + url_for('GetSignsCount') + '<br>'
    resp += 'http://' + request.host + url_for('GetSignerInfo') + '<br>'
    resp += 'http://' + request.host + url_for('GetDataFromSignedData') + '<br>'
    resp += 'http://' + request.host + url_for('VerifyDataInternal') + '<br>'
    return resp


@app.route('/GetSignsCount', methods=['POST'])
def GetSignsCount():
    signedbin = request.stream.read()
    signs_count = []
    try:
        intF.GetSignsCount(None, signedbin, len(signedbin), signs_count)
    except Exception as e:
        return jsonify({'Error': repr(e)})
    return jsonify(signs_count)


@app.route('/GetSignerInfo', methods=['POST'])
def GetSignerInfo():
    signedbin = request.stream.read()
    signer_info = {}
    try:
        intF.GetSignerInfo(0, None, signedbin, len(signedbin), signer_info, None)
    except Exception as e:
        return jsonify({'Error': repr(e)})
    return jsonify(signer_info)


@app.route('/GetDataFromSignedData', methods=['POST'])
def GetDataFromSignedData():
    signedbin = request.stream.read()
    unsignedbin = []
    try:
        intF.GetDataFromSignedData(None, signedbin, len(signedbin), unsignedbin)
    except Exception as e:
        return jsonify({'Error': repr(e)})
    return send_file(io.BytesIO(unsignedbin[0]), mimetype='application/octet-stream')


@app.route('/VerifyDataInternal', methods=['POST'])
def VerifyDataInternal():
    signedbin = request.stream.read()
    data = {}
    sign = {}
    try:
        intF.VerifyDataInternal(None, signedbin, len(signedbin), data, sign)
    except Exception as e:
        return jsonify({'Error': repr(e)})
    return jsonify([data, sign])

#intF.Finalize()
#EUUnload()