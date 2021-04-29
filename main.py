import sys
sys.setrecursionlimit(100000)
class Node:
    def __init__(self, key, parent):
        self.key = key
        self.left = None
        self.right = None
        self.color = 'r'
        self.parent = parent
    def getSibling(self):
        if self == None or self.parent == None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left
    def getAunt(self):
        if self == None:
            return None
        return self.parent.getSibling()
    def hasTwoChildren(self):
        return (self.right != None) and (self.left != None)
    def child(self):
        return self.right if self.right != None else self.left
    def hasTwoBlackChildren(self):
        return (self.child() == None) or (self.hasTwoChildren() and (self.left.color == 'b' and self.right.color == 'b')) or (self.child().color == 'b')
    def kill(self): # replace node with its only child, then kill it
        if self != None:
            if self.child() != None:
                self.child().parent = self.parent
            if self == self.parent.left:
                self.parent.left = self.child()
            else:
                self.parent.right = self.child()
class RBT:
    def __init__(self):
        self.root = None
    def initSearch(self, node, key):
        if node == None:
            return None
        if node.key == key:
            return node
        if node.key > key:
            return self.initSearch(node.left, key)
        return self.initSearch(node.right, key)
    def initMin(self, node):
        if node.left == None:
            return node
        return self.initMin(node.left)
    def min(self):
        if self.root.left == None:
            return self.root
        return self.initMin(self.root.left)
    def initMax(self, node):
        if node.right == None:
            return node
        return self.initMax(node.right)
    def max(self):
        if self.root.right == None:
            return self.root
        return self.initMax(self.root.right)
    def predecessor(self, node):
        if node.left != None:
            return self.initMax(node.left)
        par = node.parent
        while par != None and node == par.left:
            node = par
            par = par.parent
        return par
    def successor(self, node):
        if node.right != None:
            return self.initMin(node.right)
        par = node.parent
        while par != None and node == par.right:
            node = par
            par = par.parent
        return par
    def search(self, key):
        if self.root == None:
            return None
        if self.root.key == key:
            return self.root
        if self.root.key > key:
            return self.initSearch(self.root.left, key)
        return self.initSearch(self.root.right, key)
    def rotate(self, node, direction):
        if direction == "left":
            node.right.parent = node.parent
            if node == self.root:
                self.root = node.right
            elif node == node.parent.left:
                node.parent.left = node.right
            else:
                node.parent.right = node.right
            right_child = node.right
            node.right = right_child.left
            if node.right != None:
                node.right.parent = node
            right_child.left = node
            node.parent = right_child
        else:
            node.left.parent = node.parent
            if node == self.root:
                self.root = node.left
            elif node == node.parent.left:
                node.parent.left = node.left
            else:
                node.parent.right = node.left
            left_child = node.left
            node.left = left_child.right
            if node.left != None:
                node.left.parent = node
            left_child.right = node
            node.parent = left_child
    def fixup(self, node):
        if node == self.root:
            node.color = 'b'
            return
        if node.parent.color == 'r':
            if node.getAunt() == None or node.getAunt().color == 'b':
                ggrandpa = node.parent.parent.parent
                if ggrandpa != None:
                    if node.parent.parent == ggrandpa.left:
                        is_left_child = True
                    else:
                        is_left_child = False
                if node == node.parent.left and node.parent == node.parent.parent.left:
                    self.rotate(node.parent.parent, "right")
                elif node == node.parent.right and node.parent == node.parent.parent.right:
                    self.rotate(node.parent.parent, "left")
                elif node == node.parent.right and node.parent == node.parent.parent.left:
                    grandpa = node.parent.parent
                    self.rotate(node.parent, "left")
                    self.rotate(grandpa, "right")
                else:
                    grandpa = node.parent.parent
                    self.rotate(node.parent, "right")
                    self.rotate(grandpa, "left")
                if ggrandpa == None:
                    self.root.color = 'b'
                    self.root.left.color = 'r'
                    self.root.right.color = 'r'
                elif is_left_child == True:
                    ggrandpa.left.color = 'b'
                    ggrandpa.left.left.color = 'r'
                    ggrandpa.left.right.color = 'r'
                else:
                    ggrandpa.right.color = 'b'
                    ggrandpa.right.left.color = 'r'
                    ggrandpa.right.right.color = 'r'
            else:
                node.parent.color = 'b'
                node.getAunt().color = 'b'
                node.parent.parent.color = 'r'
                return self.fixup(node.parent.parent)
        else:
            return
    def initInsert(self, node, key):
        if node.key > key:
            if node.left == None:
                newNode = Node(key, node)
                node.left = newNode
                return newNode
            return self.initInsert(node.left, key)
        if node.right == None:
            newNode = Node(key, node)
            node.right = newNode
            return newNode
        return self.initInsert(node.right, key)
    def insert(self, key):
        if self.root == None:
            newNode = Node(key, None)
            newNode.color = 'b'
            self.root = newNode
            return newNode
        if self.root.key > key:
            if self.root.left == None:
                newNode = Node(key, self.root)
                self.root.left = newNode
                return newNode
            newNode = self.initInsert(self.root.left, key)
        else:
            if self.root.right == None:
                newNode = Node(key, self.root)
                self.root.right = newNode
                return newNode
            newNode = self.initInsert(self.root.right, key)
        self.fixup(newNode)
    def BFS(self):
        output = []
        output.append(str(self.root.key) + self.root.color)
        Q = []
        Q.append(self.root)
        cur = 0
        while len(Q) != cur:
            v = Q[cur]
            cur += 1
            if v.left != None:
                output.append(str(v.left.key) + v.left.color)
                Q.append(v.left)
            if v.right != None:
                output.append(str(v.right.key) + v.right.color)
                Q.append(v.right)
        print(*output)
    def doubleBlackCycle(self, child):
        nil = None
        if child.key == None:
            nil = child
        while(True):
            sib = child.getSibling()
            if sib != None and sib.color == 'r': # case 1
                if child == child.parent.left:
                    self.rotate(child.parent, "left")
                else:
                    self.rotate(child.parent, "right")
                child.parent.color = 'r'
                sib.color = 'b'
            else:
                if sib == None or sib.hasTwoBlackChildren(): # case 2
                    if sib != None:
                        sib.color = 'r'
                    if child != self.root:
                        if child.parent.color == 'r':
                            child.parent.color = 'b'
                            break
                        else:
                            child = child.parent
                            child.color = 'd'
                    else:
                        child.color = 'b'
                        break
                else:
                    if child == child.parent.left:
                        if (sib.right == None or sib.right.color == 'b') and (sib.left != None and sib.left.color == 'r'): # case 3: goal is to have child.parent, sib and sib.child() [which is red] in a line
                            sib.left.color == 'b'
                            sib.color = 'r'
                            self.rotate(sib, "right")
                            sib = sib.parent
                        # case 4
                        self.rotate(child.parent, "left")
                        sib.color = sib.left.color
                        sib.right.color = 'b'
                        sib.left.color = 'b'
                        break
                    else:
                        if (sib.left == None or sib.left.color == 'b') and (sib.right != None and sib.right.color == 'r'): # case 3: goal is to have child.parent, sib and sib.child() [which is red] in a line
                            sib.right.color == 'b'
                            sib.color = 'r'
                            self.rotate(sib, "left")
                            sib = sib.parent
                        # case 4
                        self.rotate(child.parent, "right")
                        sib.color = sib.right.color
                        sib.left.color = 'b'
                        sib.right.color = 'b'
                        break
        nil.kill()
    def initDelete(self, node):
        if node.color == 'r':
            node.kill()
        else:
            if node.child() == None:
                node.key = None
                node.color = 'd' # double black
                self.doubleBlackCycle(node)
            else:
                if node.child().color == 'r':
                    node.child().color == 'b'
                    node.kill()
                else:
                    child = node.child()
                    node.kill()
                    child.color = 'd' # double black
                    self.doubleBlackCycle(child)
    def delete(self, key):
        node = self.search(key)
        if node != None:
            if node.hasTwoChildren():
                if self.successor(node) != None and self.successor(node).color == 'r':
                    node.key = self.successor(node).key
                    self.initDelete(self.successor(node))
                elif self.predecessor(node) != None and self.predecessor(node).color == 'r':
                    node.key = self.predecessor(node).key
                    self.initDelete(self.predecessor(node))
                elif self.predecessor(node) != None:
                    node.key = self.predecessor(node).key
                    self.initDelete(self.predecessor(node))
                else:
                    node.key = self.predecessor(node).key
                    self.initDelete(self.predecessor(node))
            else:
                self.initDelete(node)
x = RBT()
while(True):
    try:
        op = list(input().split())
        if op[0] == "insert":
            x.insert(int(op[1]))
        elif op[0] == "delete":
            x.delete(int(op[1]))
        elif op[0] == "print":
            x.BFS()
    except:
        break