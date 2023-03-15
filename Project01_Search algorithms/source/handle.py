# from curses import window
from faulthandler import disable
import math
import queue
from queue import PriorityQueue
from draw import *
from readFile import *


#------------------------------------------------------------------------------------------------------------
dr = [0, -1, 0, 1]
dc = [-1, 0, 1, 0]

MAX = 50
EDGE_WEIGHT = 1
MAX_DISTANCES = 10000

bonus_points = []
matrix = []

m = 0
n = 0

# set up path output
output_path = os.path.join(os.curdir,'output') #'..\\Output' 
os.makedirs(os.path.join(output_path,'level_1'),exist_ok=True)
os.makedirs(os.path.join(output_path,'level_2'),exist_ok=True)
os.makedirs(os.path.join(output_path,'level_3'),exist_ok=True)
os.makedirs(os.path.join(output_path,'advance'),exist_ok=True)

pathParent = ''

# suport to get route
visit = [[False]*MAX for _ in range(MAX)]
locationVisit = []
path = [[-1]*MAX for _ in range(MAX)]

def setUp(visit, path, locationVisit):
    for i in range(0, m):
        for j in range(0, n):
            visit[i][j] = False
    
    for i in range(0, m):
        for j in range(0, n):
            path[i][j] = -1

    locationVisit.clear()

def setUp2(visit, path):
    for i in range(0, m):
        for j in range(0, n):
            visit[i][j] = False
    
    for i in range(0, m):
        for j in range(0, n):
            path[i][j] = -1

# check in matrix
def checkInMatrix(r, c):
    return r in range(m) and c in range(n)

# export route
def Path(start, end):
    res = []

    if visit[end[0]][end[1]] == False:
        print("Error!")
        return res

    temp = end
    while True:
        res.append(temp)
        temp = path[temp[0]][temp[1]]
        if temp == start:
            res.append(temp)
            break

    res.reverse()
    return res


def distance(s, e):
    return abs(s[0] - e[0]) + abs(s[1] - e[1])


#------------------------------------------------------------------------------------------------------------
"""# Breath First Search 
"""
def BFS(start, end):
    q = queue.Queue()
    q.put(start)
    visit[start[0]][start[1]] = True

    while not q.empty():
        u = q.get(0)
        if (u == end):
            return

        for i in range(4):
            r = u[0] + dr[i]
            c = u[1] + dc[i]

            if checkInMatrix(r, c) and visit[r][c] == False and matrix[r][c] != 'x':
                visit[r][c] = True
                locationVisit.append((r, c))
                path[r][c] = u
                q.put((r, c))
    


def drawBFS(start, end):
    setUp(visit, path, locationVisit)
    BFS(start, end)
    route = Path(start, end)
    os.makedirs(os.path.join(pathParent,'bfs'),exist_ok=True)
    pathChild = pathParent + '\\' + 'bfs'
    pathOutTxt = pathChild + '\\' + 'bfs.txt'
    pathOutMp4 = pathChild + '\\' + 'bfs.mp4'
    outputTxt(route, pathOutTxt, len(route))
    drawByPygame(matrix, bonus_points, start, end, pathOutMp4, route, locationVisit)



#------------------------------------------------------------------------------------------------------------
"""# Depth First Search 
"""

def DFS(start, end):
    stack = []
    stack.append(start)
    visit[start[0]][start[1]] = True
    while len(stack) > 0:
        u = stack.pop()
        for i in range(4):
            r = u[0] + dr[i]
            c = u[1] + dc[i]

            if (r, c) == end:
                visit[r][c] = True
                path[r][c] = u
                return

            if checkInMatrix(r, c) and visit[r][c] == False and matrix[r][c] != 'x':
                visit[r][c] = True
                locationVisit.append((r, c))
                path[r][c] = u
                stack.append((r, c))


def drawDFS(start, end):
    setUp(visit, path, locationVisit)
    DFS(start, end)
    route = Path(start, end)
    os.makedirs(os.path.join(pathParent,'dfs'),exist_ok=True)
    pathChild = pathParent + '\\' + 'dfs'
    pathOutTxt = pathChild + '\\' + 'dfs.txt'
    pathOutMp4 = pathChild + '\\' + 'dfs.mp4'
    outputTxt(route, pathOutTxt, len(route))
    drawByPygame(matrix, bonus_points, start, end, pathOutMp4, route, locationVisit)



#------------------------------------------------------------------------------------------------------------
"""# Uniform Cost Search 
"""
def UCS(start, end):
    distances = [[MAX_DISTANCES]*MAX for _ in range(MAX)]
    distances[start[0]][start[1]] = 0

    pq = PriorityQueue()
    pq.put((0, (start)))

    while not pq.empty():
        du, u = pq.get()
        if (du != distances[u[0]][u[1]]):
            continue
        
        if u == end:
            visit[u[0]][u[1]] = True
            break

        for i in range(4):
            r = u[0] + dr[i]
            c = u[1] + dc[i]
            
            if checkInMatrix(r,c) and visit[r][c] == False and matrix[r][c] != 'x':
                locationVisit.append((r,c))
                
                if distances[r][c] > du + EDGE_WEIGHT:
                    distances[r][c] = du + EDGE_WEIGHT
                    pq.put((du + EDGE_WEIGHT, (r,c)))
                    path[r][c] = u
        
        visit[u[0]][u[1]] = True

def drawUCS(start, end):
    setUp(visit, path, locationVisit)
    UCS(start, end)
    route = Path(start, end)
    os.makedirs(os.path.join(pathParent,'ucs'),exist_ok=True)
    pathChild = pathParent + '\\' + 'ucs'
    pathOutTxt = pathChild + '\\' + 'ucs.txt'
    pathOutMp4 = pathChild + '\\' + 'ucs.mp4'
    outputTxt(route, pathOutTxt, len(route))
    drawByPygame(matrix, bonus_points, start, end, pathOutMp4, route, locationVisit)

# ------------------------------------------------------------------------------------------------------------
"""Heurictis
"""
def heuristic1(start, end):
      return abs(start[0] - end[0]) + abs(start[1] - end[1])

def heuristic2(start, end):
    return math.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)

#------------------------------------------------------------------------------------------------------------
"""# Greedy Best First Search using heuristic1
"""
def GBFS(start, end):
    stack = []
    stack.append(start)
    visit[start[0]][start[1]] = True

    while len(stack) > 0:
        u = stack.pop()

        abilityVisit = []
        for i in range(4):
            r = u[0] + dr[i]
            c = u[1] + dc[i]

            if (r, c) == end:
                visit[r][c] = True
                path[r][c] = u
                return

            if checkInMatrix(r, c) and visit[r][c] == False and matrix[r][c] != 'x':
                visit[r][c] = True
                locationVisit.append((r, c))
                path[r][c] = u
                abilityVisit.append((distance((r, c), end), (r, c)))
        abilityVisit.sort(key = lambda x: x[0])
        for i in range(len(abilityVisit) - 1, -1, -1):
            stack.append(abilityVisit[i][1])


def drawGBFS(start, end):
    setUp(visit, path, locationVisit)
    GBFS(start, end)
    route = Path(start, end)
    os.makedirs(os.path.join(pathParent,'gbfs_heuristic_1'),exist_ok=True)
    pathChild = pathParent + '\\' + 'gbfs_heuristic_1'
    pathOutTxt = pathChild + '\\' + 'gbfs_heuristic_1.txt'
    pathOutMp4 = pathChild + '\\' + 'gbfs_heuristic_1.mp4'
    outputTxt(route, pathOutTxt, len(route))
    drawByPygame(matrix, bonus_points, start, end, pathOutMp4, route, locationVisit)

# -----------------------------------------------------------------------------------------------------------
"""# Greedy Best First Search Using heuristic 2
"""
def GBFS2(start, end):
    stack = []
    stack.append(start)
    visit[start[0]][start[1]] = True
    locationVisit.append(start)
    while len(stack) > 0:
        u = stack.pop()

        abilityVisit = []
        for i in range(4):
            r = u[0] + dr[i]
            c = u[1] + dc[i]

            if (r, c) == end:
                visit[r][c] = True
                path[r][c] = u
                return

            if checkInMatrix(r, c) and visit[r][c] == False and matrix[r][c] != 'x':
                visit[r][c] = True
                locationVisit.append((r, c))
                path[r][c] = u
                abilityVisit.append((heuristic2((r, c), end), (r, c)))
        abilityVisit.sort(key = lambda x: x[0])
        for i in range(len(abilityVisit) - 1, -1, -1):
            stack.append(abilityVisit[i][1])


def drawGBFS2(start, end):
    setUp(visit, path, locationVisit)
    GBFS2(start, end)
    route = Path(start, end)
    os.makedirs(os.path.join(pathParent,'gbfs_heuristic_2'),exist_ok=True)
    pathChild = pathParent + '\\' + 'gbfs_heuristic_2'
    pathOutTxt = pathChild + '\\' + 'gbfs_heuristic_2.txt'
    pathOutMp4 = pathChild + '\\' + 'gbfs_heuristic_2.mp4'
    outputTxt(route, pathOutTxt, len(route))
    drawByPygame(matrix, bonus_points, start, end, pathOutMp4, route, locationVisit)

#------------------------------------------------------------------------------------------------------------
"""# A*
"""
def AStar(start, end):
    distances = [[MAX_DISTANCES]*MAX for _ in range(MAX)]
    distances[start[0]][start[1]] = 0

    pq = PriorityQueue()
    pq.put((0, (start)))

    while not pq.empty():
        _, u = pq.get()
        if u == end:
            visit[u[0]][u[1]] = True
            break
        
        for i in range(4):
            r = u[0] + dr[i]
            c = u[1] + dc[i]
            
            if checkInMatrix(r,c) and visit[r][c] == False and matrix[r][c] != 'x':
                old_distance = distances[r][c]
                new_distance = distances[u[0]][u[1]] + EDGE_WEIGHT
                locationVisit.append((r,c))
                
                if new_distance < old_distance:
                    distances[r][c] = new_distance
                    priority = new_distance + heuristic1((r,c), end)
                    pq.put((priority, (r,c)))
                    path[r][c] = u
        
        visit[u[0]][u[1]] = True


def drawAStar(start, end):
    setUp(visit, path, locationVisit)
    AStar(start, end)
    route = Path(start, end)
    os.makedirs(os.path.join(pathParent,'astar_heuristic_1'),exist_ok=True)
    pathChild = pathParent + '\\' + 'astar_heuristic_1'
    pathOutTxt = pathChild + '\\' + 'astar_heuristic_1.txt'
    pathOutMp4 = pathChild + '\\' + 'astar_heuristic_1.mp4'
    outputTxt(route, pathOutTxt, len(route))
    drawByPygame(matrix, bonus_points, start, end, pathOutMp4, route, locationVisit)

# -----------------------------------------------------------------------------------------------------------
def AStar2(start, end):
    distances = [[MAX_DISTANCES]*MAX for _ in range(MAX)]
    distances[start[0]][start[1]] = 0

    pq = PriorityQueue()
    pq.put((0, (start)))

    while not pq.empty():
        _, u = pq.get()
        if u == end:
            visit[u[0]][u[1]] = True
            break
        
        for i in range(4):
            r = u[0] + dr[i]
            c = u[1] + dc[i]
            
            if checkInMatrix(r,c) and visit[r][c] == False and matrix[r][c] != 'x':
                old_distance = distances[r][c]
                new_distance = distances[u[0]][u[1]] + EDGE_WEIGHT
                locationVisit.append((r,c))
                
                if new_distance < old_distance:
                    distances[r][c] = new_distance
                    priority = new_distance + heuristic2((r,c), end)
                    pq.put((priority, (r,c)))
                    path[r][c] = u
        
        visit[u[0]][u[1]] = True


def drawAStar2(start, end):
    setUp(visit, path, locationVisit)
    AStar2(start, end)
    route = Path(start, end)
    os.makedirs(os.path.join(pathParent,'astar_heuristic_2'),exist_ok=True)
    pathChild = pathParent + '\\' + 'astar_heuristic_2'
    pathOutTxt = pathChild + '\\' + 'astar_heuristic_2.txt'
    pathOutMp4 = pathChild + '\\' + 'astar_heuristic_2.mp4'
    outputTxt(route, pathOutTxt, len(route))
    drawByPygame(matrix, bonus_points, start, end, pathOutMp4, route, locationVisit)

#------------------------------------------------------------------------------------------------------------
"""# A* For Bonus Matrix
"""
def AStarForBonus(start, end, aPath):
    bonus = []
    res = 0
    def sortE(e):
        return abs(e['pos'][0] - start[0] + e['pos'][1] - start[1])

    for bo in bonus_points:
        temp = {}
        temp['pos'] = (bo[0], bo[1])
        temp['val'] = bo[2]
        bonus.append(temp)
    bonus.sort(key=sortE)
    
    cur = start
    while (cur != end):
        tCur = cur
        point = distance(cur, end)

        pCur = cur
        for bo in bonus:
            if bo['pos'] != cur:
                g = distance(cur, bo['pos'])
                h = distance(bo['pos'], end)    
                f = g + h + bo['val']

            if f < point:
                point = f
                pCur = bo['pos']
        
        for bo in bonus:
            if bo['pos'] == pCur:
                res += bo['val']
                bonus.remove(bo)

        cur = pCur
        
        if cur == tCur:
            AStar(cur, end)
            route = Path(cur, end)
            if route == None:
                return None
            else:
                aPath += route 
                res += len(route) - 1
            return res

        AStar(tCur, cur)
        route = Path(tCur, cur)
        setUp2(visit, path)
        if route == None:
            cur = tCur
        else:
            aPath += route
            res += len(route) - 1

    return res


def drawAStarBonus(start, end):
    setUp(visit, path, locationVisit)
    route = []
    res = AStarForBonus(start, end, route)
    os.makedirs(os.path.join(pathParent,'astarForBonus'),exist_ok=True)
    pathChild = pathParent + '\\' + 'astarForBonus'
    pathOutTxt = pathChild + '\\' + 'astarForBonus.txt'
    pathOutMp4 = pathChild + '\\' + 'astarForBonus.mp4'
    outputTxt(route, pathOutTxt, res)
    drawByPygame(matrix, bonus_points, start, end, pathOutMp4, route, locationVisit)


#------------------------------------------------------------------------------------------------------------
"""# Astar For Pickup Matrix
"""
def createPickupPoints(bonus_points):
    pickup_points = []
    for bo in bonus_points:
        temp = {}
        temp = (bo[0], bo[1])
        pickup_points.append(temp)
    return pickup_points

pickup_points = []
N_pickup_points = 0
def mapPickup(start, end, PathPickUp):
    s = start
    PP = []
    while len(pickup_points) != 0:
        MIN = heuristic1(s, pickup_points[0])
        Index = 0
        for i in range(1, len(pickup_points)):
            if (heuristic1(s, pickup_points[i])) < MIN:
                MIN = heuristic1(s, pickup_points[i])
                Index = i
        AStar(s, pickup_points[Index])
        PP = Path(s, pickup_points[Index])
        PathPickUp.extend(PP)
        setUp2(visit, path)
        s = pickup_points[Index]
        pickup_points.pop(Index)

    AStar(s, end)
    PP = Path(s, end)
    PathPickUp.extend(PP)

def drawPickUp(start, end):
    global pickup_points
    global N_pickup_points
    pickup_points = createPickupPoints(bonus_points)
    N_pickup_points = len(pickup_points)
    setUp(visit, path, locationVisit)
    route = []
    mapPickup(start, end, route)
    res = len(route) - 2*N_pickup_points # diem thuong bi lam lai 2 lan va co gia tri la 0
    os.makedirs(os.path.join(pathParent,'astarForPickup'),exist_ok=True)
    pathChild = pathParent + '\\' + 'astarForPickup'
    pathOutTxt = pathChild + '\\' + 'astarForPickup.txt'
    pathOutMp4 = pathChild + '\\' + 'astarForPickup.mp4'
    outputTxt(route, pathOutTxt, res)
    drawByPygame(matrix, bonus_points, start, end, pathOutMp4, route, locationVisit)


#------------------------------------------------------------------------------------------------------------
"""# handle levels input
"""
def getStartEnd():
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 'S':
                start = (i, j)

            elif matrix[i][j] == ' ':
                if (i == 0) or (i == len(matrix)-1) or (j == 0) or (j == len(matrix[0])-1):
                    end = (i, j)

            else:
                pass
    return start, end

# handle level 1
def handleInputLevel1(file_name: str, numInput):
    global bonus_points, matrix
    bonus_points, matrix  = read_file(file_name)

    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')

    global m
    m = len(matrix)  # chiều dài của matrix
    global n 
    n= len(matrix[0])  # chiều rộng của matrix
    start, end = getStartEnd()
    # set up path to output
    global pathParent
    pathParent = '.\output\level_1'
    os.makedirs(os.path.join(pathParent, numInput),exist_ok=True)
    pathParent = pathParent + '\\' + numInput
    # draw marix no bonus with 5 algorithm: dfs, bfs, ucs, gbfs, a*
    drawDFS(start, end)
    drawBFS(start, end)
    drawUCS(start, end)
    drawGBFS(start, end)
    drawGBFS2(start, end)
    drawAStar(start, end)
    drawAStar2(start, end)

# handle level 2
def handleInputLevel2(file_name: str, numInput):
    global bonus_points, matrix
    bonus_points, matrix  = read_file(file_name)

    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')

    global m
    m = len(matrix)  # chiều dài của matrix
    global n 
    n= len(matrix[0])  # chiều rộng của matrix
    start, end = getStartEnd()
    # set up path to output
    global pathParent
    pathParent = '.\output\level_2'
    os.makedirs(os.path.join(pathParent, numInput),exist_ok=True)
    pathParent = pathParent + '\\' + numInput
    # draw marix have bonus with algorithm: astar + heuristic
    drawAStarBonus(start, end)

# handle level 3
def handleInputLevel3(file_name: str, numInput):
    global bonus_points, matrix
    bonus_points, matrix  = read_file(file_name)

    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')

    global m
    m = len(matrix)  # chiều dài của matrix
    global n 
    n= len(matrix[0])  # chiều rộng của matrix
    start, end = getStartEnd()
    # set up path to output
    global pathParent
    pathParent = '.\output\level_3'
    os.makedirs(os.path.join(pathParent, numInput),exist_ok=True)
    pathParent = pathParent + '\\' + numInput
    # draw marix have pickup with algorithm: astar + heuristic
    drawPickUp(start, end)

# handle advance
def handleInputAdvance(file_name: str, numInput):
    global bonus_points, matrix
    bonus_points, matrix  = read_file(file_name)

    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')

    global m
    m = len(matrix)  # chiều dài của matrix
    global n 
    n= len(matrix[0])  # chiều rộng của matrix
    start, end = getStartEnd()
    # set up path to output
    global pathParent
    pathParent = '.\output\advance'
    os.makedirs(os.path.join(pathParent, numInput),exist_ok=True)
    pathParent = pathParent + '\\' + numInput