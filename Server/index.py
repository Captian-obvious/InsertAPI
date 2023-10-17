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
    </html>
    """
##end

