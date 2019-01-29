import numpy as np
from operator import itemgetter

class fpTree(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.child = {}   #name:fpTree
        self.freq = 1
        self.name = name
        self.link = None

    def inc(self):
        self.freq += 1
        return

class tableLink(object):
    def __init__(self):
        self.nodeLink = None
        self.nodeVal = None

class fpGrowth(object):

    def genFpTree(self, dataSet, minFreq):
        for data in dataSet:
            data.sort()

        elementCount = {}
        for val in dataSet:
            for v in val:
                elementCount[v] = elementCount.get(v,0) + 1

        headTable = {}
        for key, count in elementCount.items():
            if elementCount[key] >= minFreq:
                headTable[key] = [count,tableLink()]

        freqElement = set(headTable.keys())

        fpGrowthTree = fpTree(None, 'Null')
        for val in dataSet:
            validElement = {}
            for v in val:
                if v in freqElement:
                    validElement[v] = headTable[v][0] #为后面排序
            if len(validElement) > 0:
                orderElement = [v[0] for v in sorted(validElement.items(), key=lambda p:p[1], reverse=True)]
                self.updateTree(orderElement, fpGrowthTree, headTable)
        return fpGrowthTree, headTable

    def updateTree(self, items, inTree, headTable):
        if items[0] in inTree.child:
            inTree.child[items[0]].inc()
        else:
            inTree.child[items[0]] = fpTree(inTree, items[0])
            if headTable[items[0]][1].nodeLink == None:
                headTable[items[0]][1].nodeLink = tableLink()
                headTable[items[0]][1].nodeVal = inTree.child[items[0]]
            else:
                self.updateHeader(headTable[items[0]][1], inTree.child[items[0]])
        if len(items) > 1:
            self.updateTree(items[1:], inTree.child[items[0]], headTable)

        return

    def updateHeader(self, nodeLink, node):
        while nodeLink.nodeLink != None:
            nodeLink = nodeLink.nodeLink
        nodeLink.nodeLink = tableLink()
        nodeLink.nodeVal = node
        return

    def calcSupport(self, fpGrowTree, headTable):

        return