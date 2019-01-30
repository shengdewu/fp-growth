from algorithm import learn
from utilit import utilit

if '__main__' == __name__:
    tool = utilit.utilit()
    fpAlg = learn.fpGrowth()

    dataSet = tool.genTestData()
    minSup = 2
    fpTree, header = fpAlg.genFpTree(dataSet, minSup)
    print(header)
    print(fpTree)

    support = fpAlg.calcSupport(fpTree, header, minSup)

    print(support)
