import sys
import Queue
import heapq
import copy
from time import time

class Board:
    def __init__(self,inp,path=[],count=0):
        self.values=inp
        self.path=path
        self.count=count

    def getNextMoves(self):
        moves=[]
        i,j=self.getHole()
        if i!=0:
            moves.append(self.swapUp(i,j))
        if i!=(len(self.values)-1):
            moves.append(self.swapDown(i,j))
        if j!=0:
            moves.append(self.swapLeft(i,j))
        if j!=(len(self.values)-1):
            moves.append(self.swapRight(i,j))
        return moves

    def getHole(self):
        for i in range(len(self.values)):
            for j in range(len(self.values)):
                if self.values[i][j]==0:
                    return i,j

    def swapUp(self,i,j):
        swapped=copy.deepcopy(self.values)
        swapped[i][j]=swapped[i-1][j]
        swapped[i-1][j]=0
        new_state=Board(swapped,self.path+["Up"],self.count+1)
        return new_state

    def swapDown(self,i,j):
        swapped=copy.deepcopy(self.values)
        swapped[i][j]=swapped[i+1][j]
        swapped[i+1][j]=0
        new_state=Board(swapped,self.path+["Down"],self.count+1)
        return new_state

    def swapLeft(self,i,j):
        swapped=copy.deepcopy(self.values)
        swapped[i][j]=swapped[i][j-1]
        swapped[i][j-1]=0
        new_state=Board(swapped,self.path+["Left"],self.count+1)
        return new_state

    def swapRight(self,i,j):
        swapped=copy.deepcopy(self.values)
        swapped[i][j]=swapped[i][j+1]
        swapped[i][j+1]=0
        new_state=Board(swapped,self.path+["Right"],self.count+1)
        return new_state

    def toOneDList(self):
        oneDList=[]
        for i in range(len(self.values)):
            for j in range(len(self.values)):
                oneDList.append(self.values[i][j])

        return oneDList

    def getPosition(self,digit):
            for i in range(len(self.values)):
                for j in range(len(self.values)):
                    if self.values[i][j]==digit:
                        return i,j

    def manhattan_distance(self):
        distance=0
        goal=[[0,1,2],[3,4,5],[6,7,8]]
        for i in range(len(goal)):
            for j in range(len(goal)):
                if goal[i][j]==0:
                    continue

                x,y=self.getPosition(goal[i][j])
                distance+=(abs(i-x)+abs(j-y))
        return distance

    def getCost(self):
        return self.count + self.manhattan_distance()

class NPuzzleSolve:
    def __init__(self,method,inp):
        self.method=method
        self.initial_state=Board(inp)
        self.goal=self.setGoal()
        self.start()

    def start(self):
        if self.method=="bfs":
            self.solveBFS()
        elif self.method=="dfs":
            self.solveDFS()
        elif self.method=="ast":
            self.solveAST()
        elif self.method=="ida":
            self.solveIDA()

    def solveBFS(self):
        q=Queue.Queue()
        checked=set()
        q.put(self.initial_state)
        checked.add(tuple(self.initial_state.toOneDList()))
        moves=0
        while not (q.empty()):
            current_state=q.get()
            print current_state.toOneDList()
            if current_state.values==self.goal:
                print len(checked)
                print current_state.path
                break
            for i in current_state.getNextMoves():
                if tuple(i.toOneDList()) not in checked:
                    q.put(i)
                    checked.add(tuple(i.toOneDList()))
            moves+=1
        print q.qsize()

    def solveDFS(self):
        stack=[]
        checked=set()
        stack.append(self.initial_state)
        checked.add((tuple(self.initial_state.toOneDList())))
        moves=0
        while stack:
            current_state=stack.pop()
            if current_state.values==self.goal:
                print len(checked)
                print current_state.path
                break
            for i in reversed(current_state.getNextMoves()):
                if tuple(i.toOneDList()) not in checked:
                    stack.append(i)
                    checked.add(tuple(i.toOneDList()))
            moves+=1
        print moves
        print len(stack)

    def solveAST(self):
        q=[]
        checked=set()
        heapq.heappush(q,(self.initial_state.getCost(),self.initial_state))
        checked.add(tuple(self.initial_state.toOneDList()))
        moves=0
        while q:
            current_state=heapq.heappop(q)[1]
            print current_state.values
            if current_state.values==self.goal:
                print len(checked)
                print current_state.path
                print current_state.getCost()
                break
            for i in current_state.getNextMoves():
                if tuple(i.toOneDList()) not in checked:
                    heapq.heappush(q,(i.getCost(),i))
                    checked.add(tuple(i.toOneDList()))
            moves+=1
        print moves
        print len(q)


    def solveIDA(self):
        next_limit=self.initial_state.getCost()
        above_limit=[]
        soln=None
        while True:
            q=[]
            checked=set()
            limit=next_limit
            q.append(self.initial_state)
            while q:
                current_state=q.pop()
                if current_state.values==self.goal:
                    soln=current_state
                    break
                for i in current_state.getNextMoves():
                    if (i.getCost(),tuple(i.toOneDList()),) not in checked and i.getCost()<=limit:
                        q.append(i)
                        checked.add((i.getCost(),tuple(i.toOneDList())),)
                    elif i.getCost()>limit:
                        above_limit.append(i.getCost())
                        print i.getCost()

            print above_limit
            next_limit=min(above_limit)

            if soln:
                print soln.path
                break


    def setGoal(self):
        values=range(9)
        goal=[values[i:i+3] for i in range(0,9,3)]
        return goal

if __name__=="__main__":
    '''
    args=sys.argv
    print type(args[3])
    inp=list(args[3].split(','))
    print inp'''

    temp=[0,1,3,4,2,5,7,8,6]
#    temp=[1,2,5,3,4,0,6,7,8]
#    temp=[1,2,5,4,0,7,6,3,8]
    start=time()
    t=[temp[i:i+3] for i in range(0,9,3)]
    solve=NPuzzleSolve("bfs",t)
    end=time()
    print end-start
