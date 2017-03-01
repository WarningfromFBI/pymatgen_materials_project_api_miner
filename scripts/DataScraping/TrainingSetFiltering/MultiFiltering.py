import scripts.DataScraping.TrainingSetFiltering.FilteringFunctions as ff
filterDictionary = {1: ''}

def multiFilter(keys, XFrame, crystalsys = 'monoclinic', thresh = 25):

    for key in keys:
        if(key == 1):
            [XFrame, discard] = ff.FilterByComplexity(thresh, Frame = XFrame)
        elif(key == 2):
            [XFrame, discard] = ff.filterByInitialLithium(Frame = XFrame)
            print(XFrame.shape)
        elif(key == 3):
            [XFrame, discard] = ff.FilterByPreservedCrystalSys(Frame = XFrame)
            print(XFrame.shape)
        elif(key == 4):
            [XFrame, discard] = ff.FilterByCrystalSys(crystalsys, Frame = XFrame)

    return XFrame
