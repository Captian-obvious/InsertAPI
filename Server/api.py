#MODULES & FLASK
import base64,compiler,os,sys,requests,robloxapi
from flask import Flask,request

#DEFINE APP
app = Flask(__name__)

#DEFINE ROUTES / VIEWS

#INDEX / LANDING PAGE
@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>Insert Cloud API - Welcome</title>
        <link rel='icon' href='/images/favicon.ico'/>
        <link rel='stylesheet' href='/css/styles-main.css'/>
    </head>
    <body>
	<div id='page_content' class='center ta_c a_up_fade'>
	    <h1 class='red1 center ta_c'>Welcome!</h1>
	    <h2 class='red1 center ta_c'>Welcome to the Insert Cloud landing page!</h2>
	    <h3 class='red1 center ta_c'>Here you will find links to the apiReference documents</h3>
	    <p class='red1 center ta_c'></p>
	</div>
    </body>
</html>
"""
##end

#APP PAGES
@app.route('/api/')
def api():
    assetid = None
    myQuery = getParams(request.url)
    if (myQuery!=None):
        idq = myQuery[0]
        if (idq!=None):
            assetid = int(idq.split('=')[1])
            if (assetid!=None):
                insertserver.downloadAsset(assetid)
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
	<div id='page_content' class='center ta_c'>
	    <h1 class='red1 center ta_c'>Insert Cloud API: Asset Downloader</h1>
	    <h2 class='red2 center ta_c'>Download Asset Request Recieved.</h2>
	    
	</div>
    </body>
</html>
"""
##end
@app.route('/api/v1/asset/')
def asset():
    assetid = None
    myQuery = getParams(request.url)
    if (myQuery!=None):
        idq = myQuery[0]
        if (idq!=None):
            assetid = int(idq.split('=')[1])
            if (assetid!=None):
                asset = insertserver.downloadAsset(assetid)
                if (asset!=None and asset.Success==True):
                    return asset.Content
                ##endif
            ##endif
        ##endif
    ##endif
##end
@app.route('/docs/')
def docs():
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>Insert Cloud API - API Reference</title>
        <link rel='icon' href='/images/favicon.ico'/>
        <link rel='stylesheet' href='/css/styles-main.css'/>
    </head>
    <body>
	<div id='page_content' class='center ta_c a_up_fade'>
	    <h1 class='red1 center ta_c'>Welcome!</h1>
	    <h2 class='red1 center ta_c'>Welcome to the Insert Cloud API Reference documents!</h2>
	</div>
    </body>
</html>
"""
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
    def downloadAsset(assetid):
        url = 'https://assetdelivery.roblox.com/v1/asset/?id='+str(assetid)
        r = requests.get(url)
        if (r.status_code==200):
            rawData = r.content
            asset = open('api/assets/v1/'+str(assetid), "wb")
            asset.write(bytearray(rawData))
            assetDC = open('api/assets/v1/'+str(assetid),'rb')
            assetData = bytearray(assetDC.read())
            class ret:
                Content = assetData
                Success = True
            ##end
            return ret
        else:
            print('REQUEST_ERROR: '+str(r.status_code))
            return {'STATUS_CODE':r.status_code,'ERROR_MESSAGE':'REQUEST_ERROR: '+str(r.status_code)}
        ##endif
    ##end
    def compileAsset(asset):
        data = asset.Content
        return compiler.compileAsset(data)
    ##end
##end
