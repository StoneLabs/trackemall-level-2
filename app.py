#When I wrote this, only God and I understood what I was doing
#Now, God only knows

import os
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

@app.route("/getDetection", methods=['GET'])
def getDetection():
    dirc = os.listdir("/tmp/n/")
    if(len(dirc)):
        id = + str(request.args.get("id"))
        f = open("/tmp/n/" + id, "r")
        #os.remove("/tmp/n/" + id) ONLY FOR LIVE
        return f
    return "-1"

@app.route("/getFrame", methods=['GET'])
def getFrame():
    dirc = os.listdir("/tmp/o/")
    if(len(dirc)):
        id = str(request.args.get("id"))
        f = open("/tmp/o/" + id, "r")
        os.remove("/tmp/o/" + id)
        return f
    return "-1"

@app.route("/getNext", methods=['GET'])
def getNext():
    dirc = os.listdir("/tmp/o/")
    if(len(dirc)):
        return str(min(dirc))
    return "-1"

@app.route("/setDetection", methods=['POST'])
def setDetection():
    f = request.files['file']
    counter = request.args.get("id")
    f.save('/tmp/n/'+ str(counter))
    return "top"

@app.route("/addFrame", methods=['POST'])
def addFrame():
    f = request.files['file']
    counter = request.args.get("id")
    f.save('/tmp/o/'+ str(counter))
    return "top"

if __name__ == '__main__':
    try:
        os.mkdir("/tmp/n/", 777)
        os.mkdir("/tmp/o/", 777)
    except:
        print("already there")
    app.run(host='0.0.0.0', port=2438, debug=True)
