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
                headTable[key] = [count,tableLink()] # 存放的是 key 在数据集中的总数，以及其在树中对应的节点

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

    def huntPrefix(self, nodeLink):
        pathSet = []
        #横向搜索
        while nodeLink.nodeLink != None:
            #纵向搜索
            path = []
            while nodeLink.nodeVal.parent != None: #没有到根节点
                path.append(nodeLink.nodeVal)
                nodeLink.nodeVal = nodeLink.nodeVal.parent
            if len(path) > 1: #只有一项
                pathSet.append(path)
            nodeLink = nodeLink.nodeLink
        return pathSet

    def buildFreqSet(self, pathSet, minSup=2):
        freqSet = {}
        for leaf, pathes in pathSet.items():
            nodeList = {}
            nodeFreq = 0
            for path in pathes:
                freq = 0
                for node in path:
                    #第零个是叶子节点,它的频率决定整个路径的频率
                    if freq == 0:
                        freq = node.freq
                        nodeFreq += freq
                    nodeList[node.name] = nodeList.get(node.name,0) + freq

            #剔除不满足条件的点
            validNode = []
            for key, val in nodeList.items():
                if val >= minSup:
                    validNode.append(key)
            #不仅仅有叶子节点,多条路径有共同节点

            if len(validNode) <= 1:
                continue
            #构建频繁项 每一项的支持节点必须是叶子
            # 第零个是支持项,及叶子节点
            nodeSet = []
            nodeSet.extend(validNode[1:])

            nodeTemp = validNode[1:].copy()
            while len(nodeTemp) > 1:
                nodeTemp = self.group(nodeTemp)
                nodeSet.extend(nodeTemp.copy())
            nodeSet.append(nodeFreq)

            freqSet[leaf] = nodeSet
        return freqSet

    def group(self, nodeGroup):
    # A:5--->B:5---->C:3--->D:3
    #        |----->D:2
    #这种情况没有考虑到,应该以最小的作为分割条件
        nodeVal = []
        length = len(nodeGroup)
        for i in range(length-1):
            for j in range(i+1,length, 1):
                val = set(nodeGroup[i]+nodeGroup[j])
                length = len(nodeVal)
                bFind = False
                if length >= 1:
                    for k in range(length):
                        if val == nodeVal[k]:
                            bFind = True
                            break
                if not bFind:
                    nodeVal.append(list(val))
        return nodeVal

    def calcSupport(self, fpGrowTree, headTable, minSup=2):
        pathSet = {}
        for key in headTable.keys():
            element = headTable[key]
            path = self.huntPrefix(element[1])
            if len(path) > 0:
                pathSet[key] = path
        freqSet = self.buildFreqSet(pathSet, minSup)

        #计算支持度
        for key, support in freqSet.items():
            den = headTable[key]
            mem = support[-1]
            for sup in support[:-1]:
                #men/den
                pass
        return freqSet