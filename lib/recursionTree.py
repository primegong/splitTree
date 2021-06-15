from utils import *
import copy 


class TreeNode:
    def __init__(self,componentName, bbox, volume, label):
        self.componentName = componentName
        self.bbox = bbox
        self.volume = volume
        self.label = label

class Recursion_Tree:
    def __init__(self, data:TreeNode, children:list = []):
        self.data = data
        self.children = copy.deepcopy(children) #### 深拷贝！！！，否则所有节点的children指向同一个地址

    def insertSubNode(self, child):
        flag = -1
        if len(self.children) == 0: ##如果无儿子，当前节点就是所求父节点，插入新的节点
            self.children.append(child)
            return
        for childrenNode in self.children: #如果有儿子，就计入下一层判断儿子中是否有满足条件的节点
            if childrenNode.isSubNode(child):   
                childrenNode.insertSubNode(child)
                flag = 1
                break
        if flag == -1:
            self.children.append(child)
        

    def isSubNode(self, newItem):
        sign = False
        bbox = newItem.data.bbox
        overlapVolume = getOverlapVolume(self.data.bbox, bbox)
        if overlapVolume/newItem.data.volume>0.9:
            sign = True
        return sign
	
    def getNumLeafs(self, tree):
        numLeafs = 0
        children = tree.children
        numChildren = len(children)
        if numChildren > 0:
            for childNode in children:
                branchNumLeafs = self.getNumLeafs(childNode)
                numLeafs += branchNumLeafs
        else:
            numLeafs += 1
        return numLeafs

    def getMaxDepth(self, tree):
        ''' 如果只有根节点，最大深度为1;
		    如果有子节点，maxDepth = 1 + getHeight(child), 1 为根节点自身深度
			遍历所有子节点，取最深的那个深度

		'''
        maxDepth = 0
        children = tree.children
        numChildren = len(children)
        if numChildren > 0:
            for childNode in children:
                branchDepth = 1 + self.getMaxDepth(childNode)
                if branchDepth > maxDepth:
                    maxDepth = branchDepth
        else:
            maxDepth = 1
        return maxDepth

    def findDiplicateSubtrees(self):
        ''' 1. Encodes a tree to a single string.
            2. Find diplicate subtrees.
        '''
        repeatedSubtrees, subtrees = {}, set()

        def trav(tree, cur = ''):

            if not tree:
                return

            children = tree.children
            numChildren = len(children)
            if numChildren:
                ####前序或者后序遍历都可以保证序列唯一，中序遍历不行。本次采用后续遍历
                for child in children:
                    res = trav(child)
                    cur += res
                    cur += ','
                cur += str(tree.data.componentName)

                if cur in subtrees:
                    # 如果重复，就添加
                    repeatedSubtrees[cur] = tree
                else:
                    subtrees.add(cur)
            else:
                cur = tree.data.componentName
            return cur

        ##### 二叉树的序列化

        trav(self)
        print(subtrees)
        return list(repeatedSubtrees.values())
                
