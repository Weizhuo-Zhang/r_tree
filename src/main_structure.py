import math
import sys
import time
from Queue import PriorityQueue

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
    max_num = 4
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

    def reset_position(self):
        self.left = sys.maxint
        self.right = -sys.maxint
        self.top = -sys.maxint
        self.bottom = sys.maxint

    def compute_perimeter(self):
        return self.top + self.right - self.left - self.bottom

    def copy_node(self, node):
        self.successor = node.successor
        self.left = node.left
        self.right = node.right
        self.bottom = node.bottom
        self.top = node.top
        if not self.is_leaf:
            for child in node.successor:
                child.predecessor = self

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

    def split_node(self):
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

            s1 = Node()
            s2 = Node()
            min_peri = sys.maxint
            for i in range(self.min_num, node_num - self.min_num):
                temp_s1_x = Node()
                temp_s1_y = Node()
                for count in range(0, i):
                    temp_s1_x.update_with_point(x_q[count])
                    temp_s1_y.update_with_point(y_q[count])
                    temp_s1_x.successor.append(x_q[count])
                    temp_s1_y.successor.append(y_q[count])
                temp_s2_x = Node()
                temp_s2_y = Node()
                for count in range(i, node_num):
                    temp_s2_x.update_with_point(x_q[count])
                    temp_s2_y.update_with_point(y_q[count])
                    temp_s2_x.successor.append(x_q[count])
                    temp_s2_y.successor.append(y_q[count])
                peri_x = temp_s1_x.compute_perimeter() + \
                         temp_s2_x.compute_perimeter()

                peri_y = temp_s1_y.compute_perimeter() + \
                         temp_s2_y.compute_perimeter()

                if (peri_x < min_peri) and (peri_x <= peri_y):
                    min_peri = peri_x
                    s1 = temp_s1_x
                    s2 = temp_s2_x
                    continue

                if (peri_y < min_peri) and (peri_y <= peri_x):
                    min_peri = peri_y
                    s1 = temp_s1_y
                    s2 = temp_s2_y
                    continue

            new_node.is_leaf = True
            self.copy_node(s1)
            new_node.copy_node(s2)

#            s1_x = Node()
#            s2_x = Node()
#            s1_y = Node()
#            s2_y = Node()
#            min_peri_x = sys.maxint
#            min_peri_y = sys.maxint
#            max_range = node_num - self.min_num
#            for i in range(self.min_num, max_range):
#                temp_s1_x = Node()
#                temp_s2_x = Node()
#                temp_s1_y = Node()
#                temp_s2_y = Node()
#                for count in range(0, i):
#                    temp_item_x = x_q[count]
#                    temp_item_y = y_q[count]
#                    temp_s1_x.update_with_point(temp_item_x)
#                    temp_s1_y.update_with_point(temp_item_y)
#                    temp_s1_x.successor.append(temp_item_x)
#                    temp_s1_y.successor.append(temp_item_y)
#                for count in range(i, node_num):
#                    temp_item_x = x_q[count]
#                    temp_item_y = y_q[count]
#                    temp_s2_x.update_with_point(temp_item_x)
#                    temp_s2_y.update_with_point(temp_item_y)
#                    temp_s2_x.successor.append(temp_item_x)
#                    temp_s2_y.successor.append(temp_item_y)
#
#                peri_x = temp_s1_x.compute_perimeter() + \
#                         temp_s2_x.compute_perimeter()
#                peri_y = temp_s1_y.compute_perimeter() + \
#                         temp_s2_y.compute_perimeter()
#
#                if peri_x < min_peri_x:
#                    min_peri_x = peri_x
#                    s1_x = temp_s1_x
#                    s2_x = temp_s2_x
#                if peri_y < min_peri_y:
#                    min_peri_y = peri_y
#                    s1_y = temp_s1_y
#                    s2_y = temp_s2_y
#
#            new_node.is_leaf = True
#            new_node.predecessor = self.predecessor
#            if min_peri_x < min_peri_y:
#                self.copy_node(s1_x)
#                new_node.copy_node(s2_x)
#            else:
#                self.copy_node(s1_y)
#                new_node.copy_node(s2_y)
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
            for i in range(self.min_num, node_num - self.min_num):
                s1_x_left = Node()
                s1_x_right = Node()
                s1_y_bottom = Node()
                s1_y_top = Node()
                for count in range(0, i):
                    s1_x_left.update_with_node(x_left_q[count])
                    s1_x_right.update_with_node(x_right_q[count])
                    s1_y_bottom.update_with_node(y_bottom_q[count])
                    s1_y_top.update_with_node(y_top_q[count])
                    s1_x_left.successor.append(x_left_q[count])
                    s1_x_right.successor.append(x_right_q[count])
                    s1_y_bottom.successor.append(y_bottom_q[count])
                    s1_y_top.successor.append(y_top_q[count])
                s2_x_left = Node()
                s2_x_right = Node()
                s2_y_bottom = Node()
                s2_y_top = Node()
                for count in range(i, node_num):
                    s2_x_left.update_with_node(x_left_q[count])
                    s2_x_right.update_with_node(x_right_q[count])
                    s2_y_bottom.update_with_node(y_bottom_q[count])
                    s2_y_top.update_with_node(y_top_q[count])
                    s2_x_left.successor.append(x_left_q[count])
                    s2_x_right.successor.append(x_right_q[count])
                    s2_y_bottom.successor.append(y_bottom_q[count])
                    s2_y_top.successor.append(y_top_q[count])
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
                    continue

                if (peri_x_right < min_peri) and \
                        (peri_x_right <= peri_x_left) and \
                        (peri_x_right <= peri_y_bottom) and \
                        (peri_x_right <= peri_y_top):
                    min_peri = peri_x_right
                    s1 = s1_x_right
                    s2 = s2_x_right
                    continue

                if (peri_y_bottom < min_peri) and \
                        (peri_y_bottom <= peri_x_right) and \
                        (peri_y_bottom <= peri_x_left) and \
                        (peri_y_bottom <= peri_y_top):
                    min_peri = peri_y_bottom
                    s1 = s1_y_bottom
                    s2 = s2_y_bottom
                    continue

                if (peri_y_top < min_peri) and \
                        (peri_y_top <= peri_x_right) and \
                        (peri_y_top <= peri_y_bottom) and \
                        (peri_y_top <= peri_x_left):
                    min_peri = peri_y_top
                    s1 = s1_y_top
                    s2 = s2_y_top
                    continue

            self.copy_node(s1)
            new_node.copy_node(s2)
        return new_node

    def handle_overflow(self):
        new_node = self.split_node()
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
            parent.reset_position()
            for child in parent.successor:
                parent.update_with_node(child)
            parent.successor.append(new_node)
            new_node.predecessor = parent
            if parent.is_overflow():
                parent.handle_overflow()
            else:
                parent.update_with_node(new_node)

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
        self.update_with_point(point)
        if self.is_leaf:
            self.successor.append(point)
            if self.is_overflow():
                self.handle_overflow()
#            else:
#                self.update_with_point(point)
        else:
            subtree = self.choose_subtree(point)
            subtree.insert(point)

#    def intersect(self, rectangle):
#        minx = max(self.left, rectangle.left)
#        maxx = min(self.right, rectangle.right)
#        miny = max(self.bottom, rectangle.bottom)
#        maxy = min(self.top, self.top)
#        if (minx > maxx) or (miny > maxy):
#            return False
#        else:
#            return True
#
#    def answer_query(self, rectangle):
#        count = 0
#        if self.is_leaf:
#            for p in self.successor:
#                if (p.x >= rectangle.left) and \
#                        (p.x <= rectangle.right) and \
#                        (p.y >= rectangle.bottom) and \
#                        (p.y <= rectangle.top):
#                    count += 1
#            if (self.left >= rectangle.left) and \
#                    (self.right <= rectangle.right) and \
#                    (self.bottom >= rectangle.bottom) and \
#                    (self.top <= rectangle.top):
#                count = len(self.successor)
#            else:
#                for p in self.successor:
#                    if (p.x >= rectangle.left) and \
#                            (p.x <= rectangle.right) and \
#                            (p.y >= rectangle.bottom) and \
#                            (p.y <= rectangle.top):
#                        count += 1
#        else:
#            for node in self.successor:
#                if node.intersect(rectangle):
#                    count += node.answer_query(rectangle)
#        return count

def crossLine(left, right, y, bottom, top, x):
    return (bottom <= y) and (top >= y) and (left <= x) and (right >= x)

def include_rec(node, rectangle):
    if node.left <= rectangle.left and node.right >=rectangle.right and \
        node.bottom <= rectangle.bottom and node.top >= rectangle.top:
        return True
    else:
        return False


def intersect(node, rectangle):
    if (math.fabs((node.left + node.right)-(rectangle.left + rectangle.right)) \
            < (rectangle.right + node.right - rectangle.left - node.left)) \
            and (math.fabs((node.top + node.bottom) - (rectangle.top + \
            rectangle.bottom)) < (rectangle.top + node.top - rectangle.bottom \
            - node.bottom)):
        return True
    return False
#    return crossLine(node.left, node.right, node.bottom, rectangle.bottom, rectangle.top, rectangle.left) \
#       or crossLine(node.left, node.right, node.bottom, rectangle.bottom, rectangle.top, rectangle.right) \
#         or crossLine(node.left, node.right, node.top, rectangle.bottom, rectangle.top, rectangle.left) \
#           or crossLine(node.left, node.right, node.top, rectangle.bottom, rectangle.top, rectangle.right) \
#             or crossLine(rectangle.left, rectangle.right, rectangle.bottom, node.bottom, node.top, node.left) \
#               or crossLine(rectangle.left, rectangle.right, rectangle.bottom, node.bottom, node.top, node.right) \
#                 or crossLine(rectangle.left, rectangle.right, rectangle.top, node.bottom, node.top, node.left) \
#                   or crossLine(rectangle.left, rectangle.right, rectangle.top, node.bottom, node.top, node.right)


def answer_query(node, rectangle):
    count = 0
    if node.is_leaf:
        for p in node.successor:
             if (p.x >= rectangle.left) and \
                     (p.x <= rectangle.right) and \
                     (p.y >= rectangle.bottom) and \
                     (p.y <= rectangle.top):
                 count += 1
    else:
        for child in node.successor:
            if intersect(child, rectangle):
                count += answer_query(child, rectangle)
    return count


data_file = open('../data/dataset.txt')
data = data_file.readlines()
data_file.close()

query_file = open('../data/test_query.txt')
query = query_file.readlines()
query_file.close()


ss_start = int(round(time.time() * 1e6))

count_time = 0
count_test = 0
for line in data:
    count_test += 1


ss_end = int(round(time.time() * 1e6))
print 'Sequential-scan benchmark: {0}us'.format(ss_end - ss_start)

build_start = int(round(time.time()))
root = Node()
root.is_leaf = True
#i = 0
for line in data[1:]:
#    i += 1
#    print i
    line = line.split()
    line = map(eval, line)
    point = Point(line[1], line[2])
    if line[0] == 27094:
        pass
    root.insert(point)
build_end = int(round(time.time()))
print 'build: {0}s'.format(build_end - build_start)

#start = int(time.time())
#root = Node()
#root.is_leaf = True
##i = 0
#for line in data[1:]:
#    #    i += 1
#    #    print i
#    line = line.split()
#    line = map(eval, line)


def search(node):
    count = 0
    if node.is_leaf:
        count = len(node.successor)
    else:
        for item in node.successor:
            count += search(item)
    return count

#print 'count: {0}'.format(search(root))

result = ''

q_time = 0.0
for line in query:
    line = line.split()
    line = map(eval, line)
    rectangle = Rectangle(line[0], line[1], line[2], line[3])
    q_start = int(round(time.time() * 1e6))
    result += '{0}\n'.format(answer_query(root, rectangle))
    q_end = int(round(time.time() * 1e6))
    q_time += q_end - q_start

print 'Answer the query total: {0}us'.format(q_time)
print 'Answer the query average: {0}us'.format((q_time) * 1.0 / len(query))
#print 'test time: {0}us'.format(test_time)

result_file = open('result.txt', 'w')
result_file.write(result)
result_file.close()
