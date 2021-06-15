import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

class show_Tree:
	def __init__(self, tree, colors = None):
		self.tree = tree
		self.colors = colors

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


	def showTree(self, saveFile):
		tree = self.tree
		#构建窗口
		_, xStart, yStart, radius, width, disVec = self.creatWindow()
		#画图
		self.draw(tree, xStart, yStart,  radius, width, disVec)
		#保存
		f = plt.gcf()
		plt.legend()
		#窗口最大化再保存比较清楚
		plt.show()
		f.savefig(saveFile)
		plt.close()


	def creatWindow(self, radius = 300):
		'''
		———————— O ————————
		————O————  ————O————
		-O--O--O-  -O--O--O- 

		radius = 2  #节点的半径
		nodeInterval = 4 * radius #定义为两个节点之间的距离,即--
		'''
		
		#定义节点间距
		nodeInterval = 1 * radius

		# 定义图幅长宽，默认为正方形图幅，height=width
		tree = self.tree
		treeWidth = self.getNumLeafs(tree)
		treeDepth = self.getMaxDepth(tree)
		width = (treeWidth + 1) * nodeInterval
		height = width
		aspect = height/width
		fig = plt.figure(figsize=(11, 11*aspect))
		plt.xlim(0, width)
		plt.ylim(0, height)

		#定义层间距
		disVec = height/(treeDepth+1)
		#给定根节点坐标
		xStart = int(width/2)
		yStart = height - disVec 
		return fig, xStart, yStart, radius, width, disVec

	def draw(self, tree, xStart, yStart, radius, width, disVec, j=0):
		#先画当前节点 
		self.drawNode(tree, xStart, yStart, radius)
		#如果有子节点，递归画子节点
		children = tree.children
		numChildren = len(children) 
		if numChildren > 0: 
			childBrachWidth = width/(numChildren)
			for i, childNode in enumerate(children):
				xEnd = width * j + childBrachWidth * (i + 0.5)
				yEnd = yStart - disVec
				self.drawEdge(xStart, yStart, xEnd,yEnd)
				self.draw(childNode, xEnd, yEnd, radius, childBrachWidth, disVec, i)
	
	def drawNode(self, node, x, y, radius=20):
		name = node.data.componentName
		color = self.colors[node.data.label]
		plt.scatter(x,y,s = radius, c=color, edgecolors=color, marker="o")
		plt.text(x-radius/3, y-radius, name, fontsize=13)

	def drawEdge(self, xStart, yStart, xEnd, yEnd):
		x = (xStart, xEnd)
		y = (yStart, yEnd)
		plt.plot(x,y,'g-')
