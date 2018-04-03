import sys
from Queue import PriorityQueue

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    max_num = 3
    min_num = 0.4 * max_num
    def __init__(self):
        self.is_leaf = False
        self.predecessor = None
        self.successor = []
        self.left = 0.0
        self.right = 0.0
        self.top = 0.0
        self.bottom = 0.0

    def is_overflow(self):
        return len(self.successor) > self.max_num

    def is_underflow(self):
        return len(self.successor) < self.min_num

    def is_root(self):
        return None == self.predecessor

    def split(self):
        pass
        #return new_node

    def handle_overflow(self):
        new_node = self.split()
        if self.is_root():
            global root
            root = Node()
            root.successor.append(new_node)
            root.successor.append(self)
            root.left = min(self.left, new_node.left)
            root.right = max(self.right, new_node.right)
            root.bottom = min(self.bottom, new_node.bottom)
            root.top = max(self.top, new_node.top)
        else:
            parent = self.predecessor
            parent.successor.append(new_node)
            for child in parent.successor:
                parent.left = min(child.left, parent.left)
                parent.right = max(child.right, parent.right)
                parent.bottom = min(child.bottom, parent.bottom)
                parent.top = max(child.top, parent.top)
            if parent.is_overflow():
                parent.handle_overflow()

    def choose_substree(self, point):
        subtree = Node()
        min_increase = sys.maxint
        for child in self.successor:
            new_left = min(child.left, point.x)
            new_right = max(child.right, point.x)
            new_bottom = min(child.bottom, point.y)
            new_top = max(child.top, point.y)
            perimeter = child.top + child.right - child.bottom - child.left
            new_perimeter = new_top + new_right - new_bottom - new_left
            increase = new_perimeter - perimeter
            if increase < min_increase:
                min_increase = increase
                subtree = child
        return subtree

    def insert(self, point):
        if self.is_leaf:
            self.successor.append(point)
            if self.is_overflow():
                self.handle_overflow()
        else:
            subtree = self.choose_subtree(point)
            subtree.insert(point)

data_file = open('../data/dataset.txt')
data = data_file.readlines()
data_file.close()

root = Node()
x_q = PriorityQueue()
y_q = PriorityQueue()
i = 0
for line in data[1:]:
    i += 1
    if 15 == i:
        break

    line = line.split()
    line = map(eval, line)
    point = Point(line[1], line[2])
    x_q.put((point.x, point))
    y_q.put((point.y, point))

print 'Queue**************************8'
while not x_q.empty():
    print(x_q.get()[1].x)

