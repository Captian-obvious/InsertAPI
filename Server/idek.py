#IMPORTS
import base64,os,sys,rbxm,requests,robloxapi
from flask import Flask,request,jsonify
#APP DEFINITION
app = Flask(__name__)
#APP SCRIPT
#INDEX LANDING PAGE
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Insert API - LNDP</title>
            <link rel='icon' href='/images/favicon.ico'/>
            <link rel='stylesheet' href='/css/styles-main.css'/>
        </head>
        <body>
            <h1 class='red1 center ta_c'>Insert API Server:</h1>
            <p class='red1 center ta_c'>IDK what to put here. (Landing Page)</p>
        </body>
    </html>
    """
##end

#DOWNLOADER
@app.route('/api/')
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

#Assets
@app.route('/api/v1/asset/')
def compiler():
    return True
##end
#server stuff
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
                print('REQUEST_ERROR: '+str(r.status_code))
                class ret:
                    class Content:
                        ErrorMessage = r.status
                        STATUS_CODE = r.status_code
                    ##end
                    Success = False
                ##end
                return {'STATUS_CODE':r.status_code,'ERROR_MESSAGE':'REQUEST_ERROR: '+str(r.status_code)}
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

