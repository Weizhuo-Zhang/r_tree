import copy
import math
import sys
import time
from Queue import PriorityQueue
start = int(round(time.time() * 1000))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

class Node:
    max_num = 12
    min_num = int(math.ceil(0.4 * max_num))
    def __init__(self):
        self.is_leaf = False
        self.predecessor = None
        self.successor = []
        self.left = sys.maxint
        self.right = -sys.maxint
        self.top = -sys.maxint
        self.bottom = sys.maxint

    def is_overflow(self):
        return len(self.successor) > self.max_num

    def is_underflow(self):
        return len(self.successor) < self.min_num

    def compute_perimeter(self):
        return self.top + self.right - self.left - self.bottom

    def copy_node(self, node):
        self.successor = node.successor
        self.left = node.left
        self.right = node.right
        self.bottom = node.bottom
        self.top = node.top

    def update_with_point(self, point):
         self.left = min(self.left, point.x)
         self.right = max(self.right, point.x)
         self.bottom = min(self.bottom, point.y)
         self.top = max(self.top, point.y)

    def update_with_node(self, node):
        self.left = min(self.left, node.left)
        self.right = max(self.right, node.right)
        self.bottom = min(self.bottom, node.bottom)
        self.top = max(self.top, node.top)

    def split(self):
        node_num = len(self.successor)
        new_node = Node()
        if self.is_leaf:
            x_q_global = PriorityQueue()
            y_q_global = PriorityQueue()
            for item in self.successor:
                x_q_global.put((item.x, item))
                y_q_global.put((item.y, item))

            x_q = []
            y_q = []
            while not x_q_global.empty():
                x_q.append(x_q_global.get()[1])
                y_q.append(y_q_global.get()[1])

            s1_x = Node()
            s2_x = Node()
            s1_y = Node()
            s2_y = Node()
            min_peri_x = sys.maxint
            min_peri_y = sys.maxint
            max_range = node_num - self.min_num
            for i in range(self.min_num, max_range):
                temp_s1_x = Node()
                temp_s2_x = Node()
                temp_s1_y = Node()
                temp_s2_y = Node()
                for count in range(0, i):
                    temp_item_x = x_q[count]
                    temp_item_y = y_q[count]
                    temp_s1_x.update_with_point(temp_item_x)
                    temp_s1_y.update_with_point(temp_item_y)
                    temp_s1_x.successor.append(temp_item_x)
                    temp_s1_y.successor.append(temp_item_y)
                for count in range(i, node_num):
                    temp_item_x = x_q[count]
                    temp_item_y = y_q[count]
                    temp_s2_x.update_with_point(temp_item_x)
                    temp_s2_y.update_with_point(temp_item_y)
                    temp_s2_x.successor.append(temp_item_x)
                    temp_s2_y.successor.append(temp_item_y)

                peri_x = temp_s1_x.compute_perimeter() + \
                         temp_s2_x.compute_perimeter()
                peri_y = temp_s1_y.compute_perimeter() + \
                         temp_s2_y.compute_perimeter()

                if peri_x < min_peri_x:
                    min_peri_x = peri_x
                    s1_x = temp_s1_x
                    s2_x = temp_s2_x
                if peri_y < min_peri_y:
                    min_peri_y = peri_y
                    s1_y = temp_s1_y
                    s2_y = temp_s2_y

            new_node.is_leaf = True
            new_node.predecessor = self.predecessor
            if min_peri_x < min_peri_y:
                self.copy_node(s1_x)
                new_node.copy_node(s2_x)
            else:
                self.copy_node(s1_y)
                new_node.copy_node(s2_y)
        else:
            x_left_q_g = PriorityQueue()
            x_right_q_g = PriorityQueue()
            y_bottom_q_g = PriorityQueue()
            y_top_q_g = PriorityQueue()
            for item in self.successor:
                x_left_q_g.put((item.left, item))
                x_right_q_g.put((item.right, item))
                y_bottom_q_g.put((item.bottom, item))
                y_top_q_g.put((item.top, item))

            x_left_q = []
            x_right_q = []
            y_bottom_q = []
            y_top_q = []
            while not x_left_q_g.empty():
                x_left_q.append(x_left_q_g.get()[1])
                x_right_q.append(x_right_q_g.get()[1])
                y_bottom_q.append(y_bottom_q_g.get()[1])
                y_top_q.append(y_top_q_g.get()[1])
            s1 = Node()
            s2 = Node()
            min_peri = sys.maxint
            max_range = node_num - self.min_num
            for i in range(self.min_num, max_range):
                s1_x_left = Node()
                s1_x_right = Node()
                s1_y_bottom = Node()
                s1_y_top = Node()
                for count in range(0, i):
                    x_left = x_left_q[count]
                    x_right = x_right_q[count]
                    y_bottom = y_bottom_q[count]
                    y_top = y_top_q[count]
                    s1_x_left.update_with_node(x_left)
                    s1_x_right.update_with_node(x_right)
                    s1_y_bottom.update_with_node(y_bottom)
                    s1_y_top.update_with_node(y_top)
                    s1_x_left.successor.append(x_left)
                    s1_x_right.successor.append(x_right)
                    s1_y_bottom.successor.append(y_bottom)
                    s1_y_top.successor.append(y_top)
                s2_x_left = Node()
                s2_x_right = Node()
                s2_y_bottom = Node()
                s2_y_top = Node()
                for count in range(i, node_num):
                    x_left = x_left_q[count]
                    x_right = x_right_q[count]
                    y_bottom = y_bottom_q[count]
                    y_top = y_top_q[count]
                    s2_x_left.update_with_node(x_left)
                    s2_x_right.update_with_node(x_right)
                    s2_y_bottom.update_with_node(y_bottom)
                    s2_y_top.update_with_node(y_top)
                    s2_x_left.successor.append(x_left)
                    s2_x_right.successor.append(x_right)
                    s2_y_bottom.successor.append(y_bottom)
                    s2_y_top.successor.append(y_top)
                peri_x_left = s1_x_left.compute_perimeter() + \
                              s2_x_left.compute_perimeter()
                peri_x_right = s1_x_right.compute_perimeter() + \
                               s2_x_right.compute_perimeter()
                peri_y_bottom = s1_y_bottom.compute_perimeter() + \
                                s2_y_bottom.compute_perimeter()
                peri_y_top = s1_y_top.compute_perimeter() + \
                             s2_y_top.compute_perimeter()

                if (peri_x_left < min_peri) and \
                        (peri_x_left <= peri_x_right) and \
                        (peri_x_left <= peri_y_bottom) and \
                        (peri_x_left <= peri_y_top):
                    min_peri = peri_x_left
                    s1 = s1_x_left
                    s2 = s2_x_left

                if (peri_x_right < min_peri) and \
                        (peri_x_right <= peri_x_left) and \
                        (peri_x_right <= peri_y_bottom) and \
                        (peri_x_right <= peri_y_top):
                    min_peri = peri_x_right
                    s1 = s1_x_right
                    s2 = s2_x_right

                if (peri_y_bottom < min_peri) and \
                        (peri_y_bottom <= peri_x_right) and \
                        (peri_y_bottom <= peri_x_left) and \
                        (peri_y_bottom <= peri_y_top):
                    min_peri = peri_y_bottom
                    s1 = s1_y_bottom
                    s2 = s2_y_bottom

                if (peri_y_top < min_peri) and \
                        (peri_y_top <= peri_x_right) and \
                        (peri_y_top <= peri_y_bottom) and \
                        (peri_y_top <= peri_x_left):
                    min_peri = peri_y_top
                    s1 = s1_y_top
                    s2 = s2_y_top

            new_node.predecessor = self.predecessor
            self.copy_node(s1)
            new_node.copy_node(s2)
        return new_node

    def handle_overflow(self):
        new_node = self.split()
        global root
        if root == self:
            root = Node()
            root.successor.append(new_node)
            root.successor.append(self)
            new_node.predecessor = root
            self.predecessor = root
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

    def choose_subtree(self, point):
        subtree = Node()
        min_increase = sys.maxint
        for child in self.successor:
            new_left = min(child.left, point.x)
            new_right = max(child.right, point.x)
            new_bottom = min(child.bottom, point.y)
            new_top = max(child.top, point.y)
            new_perimeter = new_top + new_right - new_bottom - new_left
            increase = new_perimeter - child.compute_perimeter()
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
                self.update_with_point(point)
        else:
            subtree = self.choose_subtree(point)
            subtree.insert(point)

    def intersect(self, rectangle):
        minx = max(self.left, rectangle.left)
        maxx = min(self.right, rectangle.right)
        miny = max(self.bottom, rectangle.bottom)
        maxy = min(self.top, self.top)
        if (minx > maxx) or (miny > maxy):
            return False
        else:
            return True

    def answer_query(self, rectangle):
        count = 0
        if self.is_leaf:
            if (self.left >= rectangle.left) and \
                    (self.right <= rectangle.right) and \
                    (self.bottom >= rectangle.bottom) and \
                    (self.top <= rectangle.top):
                count = len(self.successor)
            else:
                for point in self.successor:
                    if (point.x >= rectangle.left) and \
                            (point.x <= rectangle.right) and \
                            (point.y >= rectangle.bottom) and \
                            (point.y <= rectangle.top):
                        count += 1
        else:
            for node in self.successor:
                if node.intersect(rectangle):
                    count += node.answer_query(rectangle)
        return count

data_file = open('../data/dataset.txt')
data = data_file.readlines()
data_file.close()

root = Node()
root.is_leaf = True
#i = 0
for line in data[1:]:
#    i += 1
#    print i
    line = line.split()
    line = map(eval, line)
    point = Point(line[1], line[2])
    root.insert(point)

end = int(round(time.time() * 1000))
print 'Build the tree: {0}ms'.format(end - start)

query_file = open('../data/test_query.txt')
query = query_file.readlines()
query_file.close()

result = ''

start = int(round(time.time() * 1000))
for line in query:
    line = line.split()
    line = map(eval, line)
    rectangle = Rectangle(line[0], line[1], line[2], line[3])
    result += '{0}\n'.format(root.answer_query(rectangle))

end = int(round(time.time() * 1000))
print 'Answer the query total: {0}ms'.format(end - start)
print 'Answer the query average: {0}ms'.format((end - start) * 1.0 / len(query))

print result
result_file = open('result.txt', 'w')
result_file.write(result)
result_file.close()
