#IMPORTS
import base64,os,sys,rbxm,requests,robloxapi
from flask import Flask,request
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
    </head>
    <body>
        <h1 class='red1 center ta_c'>InsertAPI Server: </h1>
        <h2 class='red3 center ta_c'>Download Asset Request Recieved.</h2>
        <p class='red1 center ta_c'>Asset Location: <a href='/api/assets/v1/"""+str(theid)+"""'>/api/assets/v1/"""+str(theid)+"""</a></p>
    </body>
</html>
"""
##end

#PARSER
@app.route('/api/v1/asset/')
def Parse():
    
##end

#server stuff
class insertserver:
    def downloadAsset(assetid):
        url = 'https://assetdelivery.roblox.com/v1/asset/?id='+str(assetid)
        r = requests.get(url)
        if (r.status_code==200):
            rawData = r.content
            asset = open('api/assets/v1/'+str(assetid), "wb")
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
    def compileAsset(asset):
        data = asset.Content
    ##end
##end
