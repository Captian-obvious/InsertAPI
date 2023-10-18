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
    insertserver.downloader.downloadAsset(theid)
##end

#Assets
@app.route('/api/v1/asset/')
def compiler():

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
                print('REQUEST_ERROR: '+str(REQUEST.status_code))
                class ret:
                    class Content:
                        ErrorMessage = REQUEST.status
                        STATUS_CODE = REQUEST.status_code
                    ##end
                    Success = False
                ##end
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

