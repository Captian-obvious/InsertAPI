import base64,os,sys,requests
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
