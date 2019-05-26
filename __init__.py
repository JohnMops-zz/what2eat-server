import sys
import os
from time import sleep

from flask import Flask, request, jsonify, render_template

import json

from .Algo2 import Algo2

app = Flask(__name__)
global algo
algo = Algo2()


@app.route('/')
def index():
      return render_template('page.html')

@app.route('/restart-algo',methods=['GET'])
def restart():
    global algo #global algo in order to refer to the global var and not a local one
    del algo
    algo = Algo2()
    return ""

@app.route('/send-yes-or-no',methods=['POST'])
def sendYesOrNo():
    data = request.data.decode('utf-8')

    res = json.loads(data)
    print("server: call to algo.respond with:"+str(res))
    res = algo.respond(res)
    return jsonify(
        areWeDone=res
        ) # return json

@app.route('/get-next-att',methods=['GET'])
def getNextAtt():
    attRes=algo.getAtt()
    name=attRes["name"]
    relRecs=attRes["relRecs"]
    attImgUrl=attRes["img"]
    print("The server sent: "+name)
    print("Relevant recipes: "+str(relRecs))
    return jsonify(
        nextAtt=name,
        numOfRelevantDishes=relRecs,
        nextAttImage=attImgUrl
        ) # return json

@app.route('/get-preview-info',methods=['GET'])
def getPreviewInfo():
    return jsonify(
        recPreviewInfo=algo.getRecPreview()
    )

if __name__ == '__main__':

    app.run(host='127.0.0.1',port='80')
    # app.run(host='10.200.203.231',port=5005)