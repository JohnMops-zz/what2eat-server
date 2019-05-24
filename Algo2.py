import csv
import os
import threading


class Algo2():

    def __init__(self):
        self.lock= threading.Lock()

        self.dataDir="datamock/10recs/"

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

        self.RECS_THRESHOLD=5
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

        return

    # return the next attribute information

    def getAtt(self):
        self.lock.acquire()

        name = self.getNextAtt()
        #img = self.getAttImg(name)
        #RR = self.getRR()

        att = {'name':name,
         #      'img': img,
         #      'RR': RR
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
                            else: yes += 1
                            j += 1
                    self.giniRates[i] = self.calcGini(yes,no)
                else:
                    self.giniRates[i] = -1
                i += 1
        except:
            print("cant find data.csv file")
        finally:
            self.data_file.close()

        max_i = self.giniRates.index(max(self.giniRates))
        return self.attsNameArr[max_i]


    def getAttImg(self, name):
        pass

    def getRR(self):
        pass

    # ans = {name(the name of the att that was answer), ans(y/n}
    def respond(self,ans):
        self.lock.acquire()

        self.lock.release()
        return self.areWeDone()

    def areWeDone(self):
        pass


    def recPreview(self):
        return [{},{}]