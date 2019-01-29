from algorithm import learn
from utilit import utilit

if '__main__' == __name__:
    tool = utilit.utilit()
    fpAlg = learn.fpGrowth()

    dataSet = tool.genTestData()
    fpTree, header = fpAlg.genFpTree(dataSet, 2)
    print(header)
    print(fpTree)
