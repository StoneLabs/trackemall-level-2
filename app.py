#When I wrote this, only God and I understood what I was doing
#Now, God only knows

import os
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

@app.route("/getDetection", methods=['GET'])
def getDetection():
    dirc = os.listdir("/tmp/trackemall/predictions/")
    if(len(dirc)):
        id = + str(request.args.get("id"))
        try:
            f = open("/tmp/trackemall/predictions/" + id, "r")
            #os.remove("/tmp/n/" + id) ONLY FOR LIVE USAGE
            return f
        except: #if there aren't enough frames rendered yet
            return "-1"
    return "-1"

@app.route("/getFrame", methods=['GET'])
def getFrame():
    dirc = os.listdir("/tmp/trackemll/frames/")
    if(len(dirc)):
        id = str(request.args.get("id"))
        f = open("/tmp/trackemall/frames/" + id, "r")
        os.remove("/tmp/trackemall/frames/" + id)
        return f
    return "-1"

@app.route("/getNext", methods=['GET'])
def getNext():
    dirc = os.listdir("/tmp/trackemall/frames/")
    if(len(dirc)):
        return str(min(dirc))
    return "-1"

@app.route("/setDetection", methods=['POST'])
def setDetection():
    f = request.files['file']
    counter = request.args.get("id")
    f.save('/tmp/trackemall/predictions/'+ str(counter))
    return "top"

@app.route("/addFrame", methods=['POST'])
def addFrame():
    f = request.files['file']
    counter = request.args.get("id")
    x = open("/tmp/trackemall/frames/"+str(counter), "w")
    x.write("")
    x.close()
    f.save('/tmp/trackemall/frames/'+str(counter))
    return "top"

if __name__ == '__main__':
    try:
        os.mkdir("/tmp/trackemall/frames/", 777)
        os.mkdir("/tmp/trackemall/predictions/", 777)
    except:
        print("you're either smart or pretty fucked..")
    app.run(host='0.0.0.0', port=2438, debug=True)
