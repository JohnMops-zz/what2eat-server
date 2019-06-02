import json
from time import sleep

import requests

from Algo2 import Algo2

local = 'http://127.0.0.1:8080'
server = 'http://195.201.119.146:8080'
preview = '/get-preview-info'
nextAtt = '/get-next-att'
restart = '/restart-algo'
yesNo = '/send-yes-or-no'
runAlgo='/run-algo'


def testAlgoWithQuestions():
    algo = Algo2()
    while True:
        name = algo.getAtt()["name"]
        attImgURL=algo.getAtt()["img"]
        print(attImgURL)
        ans = input('got ' + name +'?\n')

        res = {'name':name, 'ans':ans}

        x = algo.respond(res)
        print(x)
        if x:
            print(algo.getRecPreview())
            break

def testURL(machine):
    if machine == 'local':
        machine = local
    else:
        if machine == 'server':
            machine = server

    jalgoId=requests.get(machine + runAlgo).json()
    algoId=jalgoId["algoId"]
    nextAttRes = requests.post(machine + nextAtt,json=jalgoId).json()

    print(nextAttRes)
    name=nextAttRes["nextAtt"]
    yes = json.dumps({"ans": "1", "name":name,"algoId":algoId})
    no = json.dumps({"ans": "0", "name": name,"algoId":algoId})
    ryesNo = requests.post(machine + yesNo, yes).json()
    print(yes)

    while ryesNo['areWeDone'] == False:
        nextAttRes = requests.post(machine + nextAtt, json=jalgoId).json()
        name = nextAttRes["nextAtt"]
        yes = json.dumps({"ans": "1", "name": name, "algoId": algoId})
        no = json.dumps({"ans": "0", "name": name, "algoId": algoId})
        ryesNo = requests.post(machine + yesNo, yes).json()
        print(yes)
        print(nextAttRes)

    rpreview = requests.post(machine + preview,json=jalgoId).json()
    print(rpreview)


def testURLwithQuestions(machine):
    if machine == 'local':
        machine = local
    elif machine == 'server':
        machine = server
    else:
        print("please enter server or local and not {}".format(machine))
        return

    jalgoId=requests.get(machine + runAlgo).json()
    algoId=jalgoId["algoId"]

    nextAttRes = requests.post(machine + nextAtt,json=jalgoId).json()
    print(nextAttRes)
    name=nextAttRes["nextAtt"]
    ans = input('got ' + name +'?\n')
    res = json.dumps({"ans": ans, "name":name,"algoId":algoId})

    ryesNo = requests.post(machine + yesNo, res).json()
    print(res)
    print(ryesNo)

    while ryesNo['areWeDone'] == False:
        nextAttRes=requests.post(machine + nextAtt, json=jalgoId).json()
        print(nextAttRes)
        name = nextAttRes["nextAtt"]
        ans = input('got ' + name + '?\n')
        res = json.dumps({"ans": ans, "name": name, "algoId": algoId})
        ryesNo = requests.post(machine + yesNo, res).json()
        print(ryesNo)

    rpreview = requests.post(machine + preview,json=jalgoId).json()
    print(rpreview)



# testAlgoWithQuestions()
testURL('local')
# testURLwithQuestions('server')