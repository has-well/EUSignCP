import io

from flask import Flask, request, jsonify, send_file, url_for
from EUSignCP import EULoad, EUUnload, EUGetInterface


app = Flask(__name__)


@app.route('/')
def main():
    resp = 'Entry poins for binary POST:<br>'
    resp += 'http://' + request.host + url_for('GetSignsCount') + '<br>'
    resp += 'http://' + request.host + url_for('GetSignerInfo') + '<br>'
    resp += 'http://' + request.host + url_for('GetDataFromSignedData') + '<br>'
    return resp


@app.route('/GetSignsCount', methods=['POST'])
def GetSignsCount():
    signedbin = request.stream.read()
    EULoad()
    intF = EUGetInterface()
    intF.Initialize()
    signs_count = []
    try:
        intF.GetSignsCount(None, signedbin, len(signedbin), signs_count)
    except Exception as e:
        return jsonify(e)
    intF.Finalize()
    EUUnload()
    return jsonify(signs_count)


@app.route('/GetSignerInfo', methods=['POST'])
def GetSignerInfo():
    signedbin = request.stream.read()
    EULoad()
    intF = EUGetInterface()
    intF.Initialize()
    signer_info = {}
    try:
        intF.GetSignerInfo(0, None, signedbin, len(signedbin), signer_info, None)
    except Exception as e:
        return jsonify(e)
    intF.Finalize()
    EUUnload()
    return jsonify(signer_info)


@app.route('/GetDataFromSignedData', methods=['POST'])
def GetDataFromSignedData():
    signedbin = request.stream.read()
    EULoad()
    intF = EUGetInterface()
    intF.Initialize()
    unsignedbin = []
    try:
        intF.GetDataFromSignedData(None, signedbin, len(signedbin), unsignedbin)
    except Exception as e:
        return jsonify(e)
    intF.Finalize()
    EUUnload()
    return send_file(io.BytesIO(unsignedbin[0]), mimetype='application/octet-stream')


