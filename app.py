#When I wrote this, only God and I understood what I was doing
#Now, God only knows

import os
from flask import Flask, request
from flask_cors import CORS
from minio import Minio

app = Flask(__name__)

CORS(app)

mc = Minio("minio:9000", access_key="belastend", secret_key="belastend42", secure=False)

try:
    mc.make_bucket("frames")
    mc.make_bucket("fframes")
except:
    print("fuck")

@app.route("/getDetection", methods=['GET'])
def getDetection():
    objects = mc.list_objects_v2('fframes')
    if(len(list(objects))):
        x = b''
        z = str(request.args.get("id"))
        y = mc.get_object('fframes', z).stream(32*1024)
        for d in y:
            x += d
        mc.remove_object('fframes', z)
        return x
    return -1

@app.route("/getFrame", methods=['GET'])
def getFrame():
    objects = mc.list_objects_v2('frames')
    if(len(list(objects))):
        x = b''
        z = str(request.args.get("id"))
        y = mc.get_object('frames', z).stream(32*1024)
        for d in y:
            x += d
        mc.remove_object('frames', z)
        return x
    return -1

@app.route("/getNext", methods=['GET'])
def getNext():
    objects = mc.list_objects_v2('frames')
    if(len(list(objects))):
        #x = b''
        z = str(min(objects,key= lambda x: int(x.object_name.encode('utf-8'))).object_name)
        #y = mc.get_object('frames', z).stream(32*1024)
        #for d in y:
        #    x += d
        #mc.remove_object('frames', z)
        return z
    return str(-1)

@app.route("/setDetection", methods=['POST'])
def setDetection():
    f = request.files['file']
    counter = request.args.get("id")
    f.save('/tmp/n'+str(counter))
    mc.fput_object("fframes", str(counter), "/tmp/n"+str(counter), "text/plain")
    os.remove("/tmp/n"+str(counter))
    return "bombidibom"

@app.route("/addFrame", methods=['POST'])
def addFrame():
    f = request.files['file']
    counter = request.args.get("id")
    f.save('/tmp/o'+str(counter))
    mc.fput_object("frames", str(counter), "/tmp/o"+str(counter), "text/plain")
    os.remove("/tmp/o"+str(counter))
    return "works"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2438, debug=True)
