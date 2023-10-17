#IMPORTS
import base64,os,sys,rbxm,requests,robloxapi
from flask import Flask,request
#APP DEFINITION
app = Flask(__name__)
#APP SCRIPT
#INDEX
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
    
##end

#API Primary
@app.route('/api/v1/asset/')
def compiler():

##end

