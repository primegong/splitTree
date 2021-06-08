import _init_paths
import os
from recursionTree import *
from objParser import *
from utils import *
from drawTree import *


def readObj(obj_file):
	parser = OBJ_PARSER(obj_file)
	triangles, face, vertices = parser.get_triangles()
	normals = parser.get_normals()
	return triangles, normals

def readComponent(componentPath, labels):
	####1. 计算每个component的 3D box 和 体积
	componentFile = os.listdir(componentPath)
	buildingComponents = dict([(key,[]) for key in labels])
	for compFile in componentFile:
		for label in labels:
			if label in compFile:
				#数据读取
				objFile = componentPath + '/' + compFile
				triangles, normals = readObj(objFile)
				#计算3D bounding box
				bboxes3D = getBbox(triangles)
				volume = getVolume(bboxes3D)
				componentName = os.path.splitext(compFile)[0] 
				buildingComponents[label].append([componentName, triangles, bboxes3D, volume])
	return buildingComponents
		

def splitTreeConstruction(buildingComponents, labels):  
	### 1. 构建Split Tree
	#1.1 根节点
	allTriangles = []
	for label, components in buildingComponents.items():
		if len(components) == 0:
			continue
		for [componentName, triangles, bboxes3D, volume] in components:
			allTriangles.extend(triangles)
	bbox = getBbox(allTriangles)
	label = labels[0]
	volume = getVolume(bbox)
	nodeItem = TreeNode(label, bbox, volume, label)
	root = Recursion_Tree(nodeItem)


	#2.2 对components按照空间连通性和类别分组，并插入根节点上
	# 屋顶、立面
	for label, components in buildingComponents.items():
		if 'roof' in label or 'fence' in label:
			nodeTriangles = []
			for [componentName, triangles, bboxes3D, volume] in components:
				nodeTriangles.extend(triangles)
			bbox = getBbox(nodeTriangles)
			volume = getVolume(bbox)
			nodeItem = TreeNode(label, bbox, volume, label)
			childNode = Recursion_Tree(nodeItem)
			if root.isSubNode(childNode):
				root.insertSubNode(childNode) 
	
	
	# 2.3 递归插入component中的部件
	print('inserting subNode...')
	for label, components in buildingComponents.items():
		if len(components) == 0:
			continue
		#按体积降序，从最大的开始
		components = sorted(components,key=lambda components: components[-1], reverse=True)
		for [componentName, triangles, bboxes3D, volume] in components:
			#查找父节点，并插入
			nodeItem = TreeNode(componentName, bboxes3D, volume, label)
			childNode = Recursion_Tree(nodeItem)
			if root.isSubNode(childNode):
				root.insertSubNode(childNode)     
	return root

def treeDisplay(tree, labels):
	colors = randomColor(labels)
	colorDict = {key:get_colour_name(value)[0] for key,value in zip(labels, colors)}
	p = show_Tree(tree, colorDict)
	p.showTree()

def ruleLabeling(tree):
	#1. Top-down phase performs a level order comparison of same-label nodes:
	# including the node properties as well as the topology of the subtrees


	#2.  Bottom-up phase: comparE parents of same-label root nodes.


	return repeatingSubtrees, nonRepeatingsubtrees

def patternDiscovery(tree):

	return pattern



def main(labels, componentPath):
	#1. Components segmentation
	buildingComponents = readComponent(componentPath, labels)

	#2. Split tree construction
	sTree = splitTreeConstruction(buildingComponents, labels)
	#print the splitTree
	treeDisplay(sTree, labels)

	# #3. Rule Labling: o identify repeating and non-repeating subtrees
	# repeatingSubtrees, nonRepeatingsubtrees = ruleLabeling(sTree)

	# #4. pattern discovery 
	# pattern = patternDiscovery(sTree)


if __name__ == "__main__":
	labels = ['building', 'roof', 'fence']
	componentPath = 'building2-1/components'
	main(labels, componentPath)




	