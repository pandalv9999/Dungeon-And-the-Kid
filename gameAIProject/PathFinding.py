import heapq
import sys


class PathFinding(object):

    @staticmethod
    def countDist(coordinate, x, y):
        '''
        manhattan distance as the estimate function
        :param coordinate:
        :param x:
        :param y:
        :return:
        '''
        tx = abs(coordinate[x][0] - coordinate[y][0])
        ty = abs(coordinate[x][1] - coordinate[y][1])
        return tx + ty

    @staticmethod
    def nodeToCoordinate(coordinate, x):
        return coordinate[x][0], coordinate[x][1]

    @staticmethod
    def coordinateToNode(x, y):
        '''
        still wonder how to do this
        :param x:
        :param y:
        :return:
        '''
        return None

    @staticmethod
    def aStar(graph, coordinate, s, t):
        '''
        use PathFinding.aStar(graph, coordinate, startnode, targetnode) to use this function
        :param graph: the graph structure of the game board, represented as adjacent list
        :param coordinate: the map of converting node's number to coordinate
        :param s: the start point's number
        :param t: the end point's number
        :return:
        '''
        father = [-1] * len(graph)
        path = []
        d = [sys.maxsize] * len(graph)
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
            for i in graph[now]:
                if d[now] + 1 < d[i]:
                    father[i] = now
                    d[i] = d[now] + 1
                    heapq.heappush(heap, [d[i] + PathFinding.countDist(coordinate, i, t) * 0.3, i])  # A*
        i = t
        while i != -1:
            path.insert(0, i)
            i = father[i]
        print path

        # change node number to coordinate
        for i in range(len(path)):
            path[i] = PathFinding.nodeToCoordinate(coordinate, path[i])
        return path


# Testing

graph = [[1, 4, 5], [0, 4, 5, 6, 2, 13], [1, 5, 6, 7, 3], [2, 6, 7], [4, 9], [1, 2, 4], [], [3, 2], [4, 5, 9, 12],
         [5, 8, 13, 10], [15], [], [], [], [], []]
cood = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3], [3, 0], [3, 1],
        [3, 2], [3, 3]]
print PathFinding.aStar(graph, cood, 0, 15)
