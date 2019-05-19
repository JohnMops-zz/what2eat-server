import unittest
from unittest import TestCase

from Algo import Algo

class TestAlgo(unittest.TestCase):
    def setUp(self):
        self.algo = Algo()

    def test_getAttImage(self):
        att='all purpose flour'
        resLink=self.algo.getAttImage(att)
        link='https://www.dollargeneral.com/media/catalog/product/cache/image/700x700/e9c3970ab036de70892d86c6d221abfe/c/v/cv_all_purpose_flour_00822801_2_.jpg'
        self.assertEqual(link,resLink,'wrong link check links file')



    # def test_calcGini(self):
    #     self.fail()
    #
    # def test_ReadSpecificLine(self):
    #     self.fail()
    #
    # def test_AreWeFinish(self):
    #     self.fail()
    #
    # def test_AND(self):
    #     self.fail()
    #
    # def test_getNumOfRelevantDishes(self):
    #     self.fail()
    #
    # def test_calcTheNextAtt(self):
    #     self.fail()
    #
    # def test_respon(self):
    #     self.fail()
    #
    # def test_getNextAtt(self):
    #     self.fail()
    #
    # def test_getNextAttImage(self):
    #     self.fail()
    #
    # def test_getRecipesId(self):
    #     self.fail()
    #
    # def test_getRecipesUrls(self):
    #     self.fail()
    #
    # def test_getPreviewInfo(self):
    #     self.fail()

if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
