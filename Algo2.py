import csv
import json
import os
import threading
import traceback


class Algo2():

    def __init__(self):
        self.lock= threading.Lock()

        self.dataDir="datamock/1000recs/"

        self.__location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        try:
            self.data_file = open(os.path.join(self.__location__, self.dataDir+'data.csv'))
        except:
            print("cant find data.csv file")
        finally:
            self.data_file.close()

        try:
            self.attsName_file = open(os.path.join(self.__location__, self.dataDir+'attsName.csv'))
            self.attsNameArr = self.attsName_file.readline().split(',')
        except:
            print("cant find attsName.csv file")
        finally:
            self.attsName_file.close()

        try:
            self.recids_file = open(os.path.join(self.__location__, self.dataDir+'recids.csv'))
            self.recidsArr = self.recids_file.readline().split(',')
        except:
            print("cant find recids.csv file")
        finally:
            self.recids_file.close()

        self.RECS_THRESHOLD=2
        self.ATTS_NUM=len(self.attsNameArr)
        self.RECS_NUM=len(self.recidsArr)

        # init empty gini rates list
        self.giniRates=[None]*self.ATTS_NUM

        # init RR(=Relevant Recipes) list
        self.RR=[1]*self.RECS_NUM
        # init RA(=Relevant Attributes) list
        self.RA=[1]*self.ATTS_NUM

        # the number of relevant attribute we currently have
        self.relAttsNum=self.ATTS_NUM
        self.relRecsNum=self.RECS_NUM

        self.ansable = False
        self.currentAtt = None

        return

    # return the next attribute information

    def getAtt(self):
        self.lock.acquire()

        name = self.getNextAtt()
        img = self.getAttImg(name)
        relRecs = self.relRecsNum

        att = {'name':name,
              'img': img,
              'relRecs': relRecs
               }

        self.lock.release()
        return att

    def calcGini(self,yes,no):
        return 1 - (yes / self.relRecsNum) ** 2 - (no / self.relRecsNum) ** 2

    # logical calculations
    def getNextAtt(self):
        try:
            self.data_file = open(os.path.join(self.__location__, self.dataDir+'data.csv'),encoding="utf-8")
            self.data_file.seek(0)
            self.data_reader = csv.reader(self.data_file, delimiter=',')

            i = 0
            for row in self.data_reader:
                if self.RA[i]:
                    yes = 0
                    no = 0
                    j = 0
                    for cell in row:
                        if self.RR[j]:
                            if cell == '0':
                                no += 1
                            else:
                                yes += 1
                        j += 1
                    self.giniRates[i] = self.calcGini(yes,no)
                else:
                    self.giniRates[i] = -1
                i += 1
        except Exception:
            print("cant find data.csv file")
            traceback.print_exc()
        finally:
            self.data_file.close()

        self.maxAtt_i = self.giniRates.index(max(self.giniRates))

        # update the current att name for sync purposes
        self.currentAtt = self.attsNameArr[self.maxAtt_i]

        # enable the option to receive answer
        self.ansable = True

        return self.attsNameArr[self.maxAtt_i]

    def getAttImg(self, name):
        urlsFile='smallImagesUrl.json'
        with open(os.path.join(self.__location__,urlsFile),'r') as imagesFile:
            urls=json.load(imagesFile)
            return(urls[self.currentAtt])

    # ans = {name(the name of the att that was answer), ans(y/n}
    def respond(self, res):

        if not self.ansable:
            print("The algo get respond before calling to getatt")
            return "The algo get respond before calling to getatt"
        if res["name"] != self.currentAtt:
            print("The respond is out of sync")
            return "The respond is out of sync"

        self.lock.acquire()

        # update the number of the
        self.relAttsNum -= 1

        # turn off the relevant att index
        self.RA[self.maxAtt_i] = 0

        try:
            self.data_file = open(os.path.join(self.__location__, self.dataDir+'data.csv'),encoding="utf-8-sig")
            if res['ans'] == "0":
                reverseRow = list(map((lambda x: 1 if x == 0 else 0),
                                      [int(x) for x in
                                       self.readSpecificLine(self.maxAtt_i, self.data_file).split(',')]))
                self.RR = self.AND(self.RR, reverseRow)
                print("ans is 0 ")
            elif res['ans'] == "1":
                attRow = list(map(int, self.readSpecificLine(self.maxAtt_i, self.data_file).split(',')))
                self.RR = self.AND(self.RR, attRow)

            else:
                return "ERROR: the ans is not 1/0"


            self.relRecsNum=sum(self.RR)

        except Exception:
            print("Error: Respond()!!@!$!@$@#")
            traceback.print_exc()
        finally:
            self.data_file.close()
            self.lock.release()

        return self.areWeDone()

    def areWeDone(self):
        if self.relRecsNum<=self.RECS_THRESHOLD:
            return True
        return False

    def readSpecificLine(self, lineNumber, file):
        file.seek(0)
        for i, line in enumerate(file):
            if i == lineNumber:
                return line
        return "ERROR: LINE #" + str(lineNumber) + " DOESN'T FOUND"

    # AND operator that work with 2 arrays
    def AND(self,A, B):
        leng = len(A)
        for i in range(0, leng):
            if A[i] == 1 & B[i] == 1:
                A[i] = 1
            else:
                A[i] = 0
        return A

    def getRecipesId(self):
        recIds=[]
        for i in range(self.RECS_NUM):
            if(self.RR[i]):
                recIds.append(self.recidsArr[i])
        return recIds

    def getRecPreview(self):

        #if we are not finish return an empty list
        if not self.areWeDone():
            print("ERROR: calling to recPreview before we done")
            return []
        allRecipeURL='https://www.allrecipes.com/recipe/'
        recIds=self.getRecipesId()
        relJson=[]
        preFile='recPreview.json'
        with open(os.path.join(self.__location__, preFile), 'r',encoding="utf-8") as previewFile:
            for rec in previewFile:
                recipe=json.loads(rec)
                rid = str(recipe['id'])
                recipe['recipeURL']=allRecipeURL+rid
                for id in recIds:
                    if rid==id:
                        relJson.append(recipe)
        return relJson