import copy
import heapq
import sys


class PathFinding(object):
    graph = []
    start = -1
    end = -1
    tmp = []
    m = {}

    def __init__(self, maze):
        self.tmp = copy.deepcopy(maze)
        count = 2
        for i in range(len(self.tmp)):
            for j in range(len(self.tmp[i])):
                if self.tmp[i][j] != 1:
                    self.m[count] = (i, j)
                    self.tmp[i][j] = count
                    count += 1

        for i in range(count):
            self.graph.append([])
        for i in range(len(self.tmp)):
            for j in range(len(self.tmp[i])):
                if self.tmp[i][j] != 1:
                    if i - 1 >= 0 and self.tmp[i - 1][j] != 1:
                        self.graph[self.tmp[i][j]].append(self.tmp[i - 1][j])
                    if j - 1 >= 0 and self.tmp[i][j - 1] != 1:
                        self.graph[self.tmp[i][j]].append(self.tmp[i][j - 1])
                    if i + 1 < len(self.tmp) and self.tmp[i + 1][j] != 1:
                        self.graph[self.tmp[i][j]].append(self.tmp[i + 1][j])
                    if j + 1 < len(self.tmp[i]) and self.tmp[i][j + 1] != 1:
                        self.graph[self.tmp[i][j]].append(self.tmp[i][j + 1])

    def setStartEnd(self, startx, starty, endx, endy):
        self.start = self.tmp[startx][starty]
        self.end = self.tmp[endx][endy]
        # for i in range(len(maze)):
        #     for j in range(len(maze[i])):
        #         if maze[i][j] == startCharacter:  # start
        #             self.start = self.tmp[i][j]
        #         elif maze[i][j] == endCharacter:  # target
        #             self.end = self.tmp[i][j]

    def countDist(self, x, y):
        '''
        manhattan distance as the estimate function
        :param x:
        :param y:
        :return:
        '''
        tx = abs(self.m[x][0] - self.m[y][0])
        ty = abs(self.m[x][1] - self.m[y][1])
        return tx + ty

    def nodeToCoordinate(self, x):
        return self.m[x][0], self.m[x][1]

    def coordinateToNode(self, row, col):
        return self.tmp[row][col]

    def aStar(self):
        s = self.start
        t = self.end
        father = [-1] * len(self.graph)
        path = []
        d = [sys.maxsize] * len(self.graph)
        d[s] = 0
        heap = [[d[s], s]]  # A*
        visited = set()
        while heap:
            while heap:
                tmp = heapq.heappop(heap)
                now = tmp[1]
                if now not in visited:
                    break
            if now in visited:
                break
            visited.add(now)
            if now == t:
                break
            for i in self.graph[now]:
                if d[now] + 1 < d[i]:
                    father[i] = now
                    d[i] = d[now] + 1
                    heapq.heappush(heap, [d[i] + self.countDist(i, t) * 0.3, i])  # A*

        if t not in visited:
            return []
        i = t
        while i != -1:
            path.insert(0, i)
            i = father[i]

        # change node number to coordinate
        for i in range(len(path)):
            path[i] = self.nodeToCoordinate(path[i])
        return path


# maze will be a size of 65*40
# Testing
'''
maze = [[2, 1, 0, 1], [0, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 3]]
print(maze)
p = PathFinding(maze)
print(p.tmp)
print(p.graph)
p.setStartEnd(2, 0, 3, 3)  # use coordinate here
print(p.aStar())
# print PathFinding.aStar(g, cood, 0, 15)
'''