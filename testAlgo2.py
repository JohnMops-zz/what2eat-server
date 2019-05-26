import json

import requests

from Algo2 import Algo2

local = 'http://127.0.0.1:5000'
server = 'http://132.145.27.181'
preview = '/get-preview-info'
nextAtt = '/get-next-att'
restart = '/restart-algo'
yesNo = '/send-yes-or-no'


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

    requests.get(machine + restart)
    nextAttRes = requests.get(machine + nextAtt).json()
    print(nextAttRes)
    name=nextAttRes["nextAtt"]
    yes = json.dumps({"ans": "1", "name":name})
    no = json.dumps({"ans": "0", "name": name})
    ryesNo = requests.post(machine + yesNo, yes).json()
    print(yes)
    print(ryesNo)

    while ryesNo['areWeDone'] == False:
        nextAttRes=requests.get(machine + nextAtt).json()
        print(nextAttRes)
        name = nextAttRes["nextAtt"]
        yes = json.dumps({"ans": "1", "name":name})
        no =  json.dumps({"ans": "0", "name":name})
        ryesNo = requests.post(machine + yesNo, yes).json()
        print(ryesNo)

    rpreview = requests.get(machine + preview).json()
    print(rpreview)

# testAlgoWithQuestions()
testURL(local)