import base64,os,sys,requests,robloxapi,time
from flask import Flask,request

app = Flask(__name__)

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
            r = requests.get(url)
            if (r.status_code==200):
                rawData = r.content
                asset = open('assets/v1/'+str(assetid), "wb")
                asset.write(bytearray(rawData))
                class ret:
                    Content = asset
                    Success = True
                ##end
                return ret
            else:
                print('REQUEST_ERROR: '+str(REQUEST.status_code))
                return {'STATUS_CODE':REQUEST.status_code,'ERROR_MESSAGE':'REQUEST_ERROR: '+str(REQUEST.status_code)}
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

#INDEX LANDING PAGE
@app.route('/')
def index():
    return """
    idk what to put here
    """
##end

#ASSET DOWNLOADER
@app.route('/download/')
def hello_world():
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
                    insertserver.downloadAsset(theid)
                ##endif
            ##endif
        ##endif
    ##endif
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>Insert Cloud API - Asset Downloader</title>
        <link rel='icon' href='/images/favicon.ico'/>
        <link rel='stylesheet' href='/css/styles-main.css'/>
        <link rel='stylesheet' href='/css/themes.css'/>
    </head>
    <body>
        <h1 class='red2'>InsertAPI Server: </h1>
        <h2 class='red1'>Download Asset Request Recieved.</h2>
        <p class='red1'>Asset Location: <a href='/assets/v1/"""+str(theid)+"""'>/assets/v1/"""+str(theid)+"""</a></p>
    </body>
</html>
"""
##end

#DOWNLOADER API.
@app.route('/v1/asset/')
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
                        data = asset.Content
                    else:
                        return str(asset)
                    ##endif
                ##endif
            ##endif
        ##endif
    ##endif
##end
