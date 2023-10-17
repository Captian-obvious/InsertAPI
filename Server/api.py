import os,sys,requests
from flask import Flask,request

app = Flask(__name__)

@app.route('/api/')

def getRequest():
    return request
##end

def getParams(url):
    if (len(url.split('?'))>1):
        query = url.split('?')[1]
        params = query.split('&')
        return params
    ##endif
##end

class insertserver:
    class downloader:
        def downloadAsset(assetid):
            url = 'https://assetdelivery.roblox.com/v1/asset/?id='+str(assetid)
            request = requests.get(url)
            if (request.status_code==200):
                rawData = request.content
                f = open('assets/v1/'+str(assetid), "wb")
                f.write(str(rawData))
                return {'Asset': f, 'Success': True}
            else:
                return {'Success':False,'StatusCode': requests.status_code, 'ErrorMessage': requests.status}
            ##endif
        ##end
    ##end
    class compiler:
        def compileAsset(asset):
            data = asset
            return str(jsonify(data))
        ##end
    ##end
##end

def download():
    theid = None
    asset_type = None
    myQuery = getParams(str(request.url))
    if (myQuery!=None):
        idq = str(myQuery[0])
        tyq = None
        if (len(myQuery)>1):
            tyq = str(myQuery[1])
        ##endif
        if (idq!=None):
            if (tyq==None or tyq=='type=model'):
                theid = int(idq.split('=')[1])
                asset_type = 'rbxm'
                if (theid!=None):
                    asset = insertserver.downloader.downloadAsset(theid)
                    if (asset.Success!=False):
                        data = asset.Asset
                        return str(insertserver.compiler.compileAsset(data))
                    else:
                        return str(asset)
                    ##endif
                ##endif
            ##endif
        ##endif
    ##endif
##end

