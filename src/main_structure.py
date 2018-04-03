from Queue import PriorityQueue

class point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

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

data_file = open('data/dataset.txt')
num_point = data_file.read()
data = data_file.readlines()
data_file.close()

x_q = PriorityQueue()
y_q = PriorityQueue()
# for line in