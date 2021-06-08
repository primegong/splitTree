import turtle

class draw_Tree:
	def __init__(self,tree):
		self.turtleConfig()
		self.tree = tree

	def turtleConfig(self):
		turtle.setup(width=600,height=600)
		turtle.color("green")
		#设置画笔的宽度
		turtle.pensize(5)
		turtle.hideturtle()
		#设置画笔移动速度,画笔绘制的速度范围[0,10]整数，数字越大越快
		turtle.speed(10000)
		turtle.getscreen().tracer()
		turtle.right(90)# Turn turtle left by angle units.direction 调整画笔
		turtle.penup() 
		turtle.goto(0,200) 
		turtle.pendown() 

	def drawTree(self):
		#画递归树
		self.draw(self.tree)
		#保存屏幕
		ts = turtle.getscreen()
		ts.getcanvas().postscript(file="splitTree.eps")

	def draw(self, tree, brachLength=200, factor=0.6375):
		"""plist is list of pensize
			brachLength is length of branch
			f is factor by which branch is shortenedcfrom level to level.
			"""
		### 画当前节点
		turtle.circle(40)
		turtle.write(tree.data.componentName, align="center",  font=("Arial", 16, "normal"))

		#画子节点
		children = tree.children
		numChildren = len(children)
		if numChildren > 0: 
			angle = int(180/(numChildren+1))#angle is half of the angle between 2 branches
			for i, childNode in enumerate(children):
				if i == 0:
					turtle.left(90-angle)
				else:
					turtle.right(angle)
				turtle.forward(brachLength)
				self.draw(childNode, brachLength*factor, factor)
