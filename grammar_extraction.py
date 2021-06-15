import _init_paths
import os
from recursionTree.recursionTree import *
from readData.objParser import *
from utils import *
from recursionTree.drawTree import *
from cluster.cluster import *

def readObj(obj_file):
	parser = OBJ_PARSER(obj_file)
	triangles, face, vertices = parser.get_triangles()
	normals = parser.get_normals()
	return triangles, normals

def readComponent(componentPath, labels):
	####1. 计算每个component的 3D box 和 体积
	componentFile = os.listdir(componentPath)
	# buildingComponents = dict([(key,[]) for key in labels])
	buildingComponents = {}
	for compFile in componentFile:
		for label in labels:
			if label in compFile:
				#数据读取
				objFile = componentPath + '/' + compFile
				triangles, normals = readObj(objFile)
				componentName = os.path.splitext(compFile)[0] 
				buildingComponents[componentName] = triangles
	return buildingComponents
		

def splitTreeConstruction(buildingComponents, labels):  
	####预处理： 找到局部坐标系 #####
	allTriangles = []
	for componentName, triangles in buildingComponents.items():
		if len(triangles) == 0:
			continue
		allTriangles.extend(triangles)
	# rotationMatrix = getLocalXYZ(allTriangles)
	# orientedAllTriangles = transformation(allTriangles, rotationMatrix)
	orientedAllTriangles = allTriangles
	
	### 1. 构建Split Tree 的根节点
	bbox = getBbox(orientedAllTriangles)
	label = labels[0]
	componentName = label
	volume = getVolume(bbox)
	nodeItem = TreeNode(componentName, bbox, volume, label)
	root = Recursion_Tree(nodeItem)


	
	
	#3 递归插入部件
	print('inserting subNode...')
	### 3.1 计算box和体积
	for componentName, triangles in buildingComponents.items():
		### 转换到局部坐标
		# orientedTriangles = transformation(triangles, rotationMatrix)
		orientedTriangles = triangles
		bbox = getBbox(orientedTriangles)
		volume = getVolume(bbox)
		label = [lb for lb in labels if lb in componentName][0]
		buildingComponents[componentName] = [triangles, bbox, volume, label]
	##### 3.2 按照体积从大到小排列 ：all components are placed in a list sorted by decreasing volume of their bounding boxes
	sortedBuildingComponents = dict(sorted(buildingComponents.items(), key=lambda kv: kv[1][-2], reverse=True))
	#####3.3 递归插入子节点######
	for componentName, value in sortedBuildingComponents.items():
		[triangles, bbox, volume, label] = value
		# if len(triangles) == 0:
		# 	continue
		#查找父节点，并插入
		nodeItem = TreeNode(componentName, bbox, volume, label)
		childNode = Recursion_Tree(nodeItem)
		root.insertSubNode(childNode)  

	# 4 计算 the parameters of split operations #######

	return root

def treeDisplay(tree, labels, saveFile):
	colors = randomColor(labels)
	colorDict = {key:get_colour_name(value)[0] for key,value in zip(labels, colors)}
	p = show_Tree(tree, colorDict)
	p.showTree(saveFile)

def ruleLabeling(tree):
	#1. Top-down phase performs a level order comparison of same-label nodes:
	# including the node properties as well as the topology of the subtrees
	repeatedSubtrees = tree.findDiplicateSubtrees()
	
	# ### 显示重复子树
	# i  = 0
	# for stringConsequence, treeList in repeatedSubtrees.items():
	# 	for repeatedSubtree in treeList:
	# 		labelName = stringConsequence.split(',')
	# 		labels = list(set(labelName))
	# 		saveFile = 'repeatedTree' + str(i+1) + '.png'
	# 		treeDisplay(repeatedSubtree, labels, saveFile)
	# 		i+=1

	#2.  Bottom-up phase: comparE parents of same-label root nodes.
	
	return repeatedSubtrees

def patternDiscovery(rTree):
	##identify the pattern of repetition of the grammar rules.
	# grammarRules = 

	return grammarRules



def main(labels, componentPath):
	#stage1. Components segmentation
	print('stage1 : reading Components segments ......')
	buildingComponents = readComponent(componentPath, labels)

	#stage2. Split tree construction
	print('stage2 : Split tree construction ......')
	sTree = splitTreeConstruction(buildingComponents, labels)
	#print the splitTree
	saveFile = 'sTree' + '.png'
	# treeDisplay(sTree, labels, saveFile)

	#stage3. Rule Labling: identify repeating and non-repeating subtrees
	print('stage3. Rule Labling: identify repeating subtrees ......')
	repeatingSubtrees = ruleLabeling(sTree)

	# stage4. pattern discovery:  identify the pattern of repetition of the grammar rules.
	print('stage4. pattern discovery : grammar rules extraction ......')
	# for rTree in repeatingSubtrees:
	# 	pattern = patternDiscovery(rTree)


if __name__ == "__main__":
	labels = ['building', 'rooftop', 'railing', 'roofplane', 'pillar']
	componentPath = 'building2-1/components'
	main(labels, componentPath)
	