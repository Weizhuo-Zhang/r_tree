from Queue import PriorityQueue

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    m = 3
    min_m = 0.4 * 3
    def __init__(self):
        self.is_leaf = False
        self.predecessor = None
        self.successor = []
        self.left = 0.0
        self.right = 0.0
        self.top = 0.0
        self.down = 0.0

data_file = open('../data/dataset.txt')
data = data_file.readlines()
data_file.close()

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

