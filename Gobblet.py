from graphics import *
from enum import Enum
import random as rn
import copy
import math
numID = 1
def hash(x , y):
    x+=1
    y+=1
    return ((x*x)+(3*x)+(2*x*y)+(y*y))/2
    
def mapcopy(m):
    new ={}
    for key in m.keys():
        new[copy.deepcopy(key)]=m[key].deepcopy()
    return new

def twodcopy(tda):
    new=[]
    for i in range(0,len(tda)):
        new.append([])
        for j in range(0,len(tda[i])):
            new[i].append(tda[i][j].deepcopy())
    return new

def nextmove(turn):
    if turn=="comp":
        return "human"
    else:
        return "comp"

def scorecomparitor(compare, s1, s2):
    if compare=="max":
        if (s1>s2):
            return s1
        else:
            return s2
    else:
        if (s1<s2):
            return s1
        else:
            return s2

class Peicesize(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2
    XLARGE = 3

class GridPos:
    def __init__(self, row, col):
        self.row=row
        self.col=col
        self.peices=[]
    def realCirCoords(self):
        if(self.row <= 3 ):
            return [50 + (self.col*100), 50 + (self.row*100)]
        else:
            return [100 + 100*self.col,500] 
    def realRangeCoords(self):
        if(self.row <= 3):
            return [[(self.row)*100, (self.row+1)*100],[(self.col)*100, (self.col+1)*100]]
        else:
            return [[450, 550],[50+(self.col)*100, 50+(self.col+1)*100]]
    def addPeice(self, peice):
        #print(self.peices)
        if (self.peices==[]):
            self.peices.insert(0,peice)
        else:
            if (self.peices[0].size.value < peice.size.value):
                self.peices.insert(0,peice)
            else:
                return "illegal move"
        peice.x=self.row
        peice.y=self.col
        peice.circle=Circle(Point(self.realCirCoords()[0],self.realCirCoords()[1]),10+peice.size.value*10)
        peice.circle.setFill(peice.color)
    def getPeice(self):
        if not (self.peices==[]):
            return self.peices.pop(0)
        else:
            return None
    def deepcopy(self):
        new = GridPos(copy.deepcopy(self.row), copy.deepcopy(self.col))
        for peice in self.peices:
            new.peices.append(peice.deepcopy())
        return new

class Peice:
    def __init__(self, size, color, x, y):
        self.size=size
        self.color=color
        self.x=x
        self.y=y
        self.circle = Circle(Point(GridPos(self.x,self.y).realCirCoords()[0],GridPos(self.x,self.y).realCirCoords()[1]),10+self.size.value*10)
        self.circle.setFill(self.color)
        global numID
        self.key = numID
        numID+=1
    def draw(self,win):
        self.circle.draw(win)
    def undraw(self):
        self.circle.undraw()
    def deepcopy(self):
        new = Peice(copy.deepcopy(self.size),copy.deepcopy(self.color),copy.deepcopy(self.x), copy.deepcopy(self.y))
        return new

class Game():
    def __init__(self, window):
        self.window = window
        self.selected=None
        col1 = Line(Point(100, 0), Point(100, 400))
        col1.setWidth(5)
        col1.draw(self.window)
        col2 = Line(Point(200, 0), Point(200, 400))
        col2.setWidth(5)
        col2.draw(self.window)
        col3 = Line(Point(300, 0), Point(300, 400))
        col3.setWidth(5)
        col3.draw(self.window)
        row1 = Line(Point(0, 100), Point(400, 100))
        row1.setWidth(5)
        row1.draw(self.window)
        row2 = Line(Point(0, 200), Point(400, 200))
        row2.setWidth(5)
        row2.draw(self.window)
        row3 = Line(Point(0, 300), Point(400, 300))
        row3.setWidth(5)
        row3.draw(self.window)
        boarder = Line(Point(0, 425), Point(400, 425))
        darkbrown = color_rgb(139,69,19)
        boarder.setFill(darkbrown)
        boarder.setWidth(50)
        boarder.draw(self.window)
        self.hpeicelib = {}
        self.tilelib = {}
        for i in range(0,6):
            for j in range(0,4):
                 if (i<=3):
                     self.tilelib[hash(i,j)] =GridPos(i,j)
                 else:
                     if (j<=2):
                         self.tilelib[hash(i,j)] =GridPos(i,j)
        for size in Peicesize:
            for k in range(0,3):
                currpeice = Peice(size, "blue", 4,k)
                self.hpeicelib[currpeice.key] = currpeice
                self.tilelib[hash(4,k)].addPeice(currpeice)
        for key in self.hpeicelib.keys():
            self.hpeicelib[key].draw(self.window)
        for size in Peicesize:
            for k in range(0,3):
                currpeice = Peice(size,"orange",5,k)
                self.hpeicelib[currpeice.key] = currpeice
                self.tilelib[hash(5,k)].addPeice(currpeice)
    def humanTurn(self):
        move=False
        while (not move):
            click = self.window.getMouse()
            #print(click)
            if self.selected == None:
                for g in range(0,5):
                     for h in range(0,4):
                         if g <= 3:
                             curr=self.tilelib[hash(g,h)]
                             if((curr.realRangeCoords()[0][0]<=click.getY() and curr.realRangeCoords()[0][1]>=click.getY())
                               and (curr.realRangeCoords()[1][0]<=click.getX() and curr.realRangeCoords()[1][1]>=click.getX())):
                                       self.selected = curr.getPeice()
                                       if self.selected==None:
                                           continue
                                       self.selected.undraw()
                                       #print(self.selected.x, self.selected.y)
                         else:
                             if h<=2:
                                 curr=self.tilelib[hash(g,h)]
                                 if((curr.realRangeCoords()[0][0]<=click.getY() and curr.realRangeCoords()[0][1]>=click.getY())
                                   and (curr.realRangeCoords()[1][0]<=click.getX() and curr.realRangeCoords()[1][1]>=click.getX())):
                                           self.selected = curr.getPeice()
                                           if self.selected==None:
                                               continue
                                           self.selected.undraw()
                                           #print(self.selected.x, self.selected.y)
                continue
            else:
                for i in range(0,4):
                    for j in range(0,4):
                        curr=self.tilelib[hash(i,j)]
                        if((curr.realRangeCoords()[0][0]<=click.getY() and curr.realRangeCoords()[0][1]>=click.getY())
                           and (curr.realRangeCoords()[1][0]<=click.getX() and curr.realRangeCoords()[1][1]>=click.getX())):
                               if (curr.peices==[] or curr.peices[0].size.value < self.selected.size.value):
                                   #print("here")
                                   print(self.selected.x, self.selected.y)
                                   #print(i,j)
                                   curr.addPeice(self.selected)
                                   #print(self.selected.x, self.selected.y)
                                   self.selected.draw(self.window)
                                   self.selected = None
                                   move = True
    def compTurn(self):
        move=False
        while(not move):
            if (not self.tilelib[hash(5,0)].peices==[]) and (not self.tilelib[hash(5,1)].peices==[]) and (not self.tilelib[hash(5,2)].peices==[]):
                selcol = rn.randint(0,2)
                ##print(selcol)
                selrow = 5
            else:
                selcol = rn.randint(0,3)
                selrow = rn.randint(0,3)
            while(self.tilelib[hash(selrow,selcol)].peices==[] or (self.tilelib[hash(selrow,selcol)].peices!=[] and self.tilelib[hash(selrow,selcol)].peices[0].color=="blue")):
                if selrow==5:
                    selcol=((selcol + rn.randint(1,2))%3)
                else:
                    selcol=((selcol + rn.randint(1,3))%4)
                    selrow=((selrow + rn.randint(1,3))%4)
            self.selected = self.tilelib[hash(selrow,selcol)].getPeice()
            self.selected.undraw()
            putcol = rn.randint(0,3)
            putrow = rn.randint(0,3)
            while (self.tilelib[hash(putrow,putcol)].addPeice(self.selected) == "illegal move"):
                    putcol=((putcol+ rn.randint(1,3))%4)
                    putrow=((putrow+ rn.randint(1,3))%4)
                    ##print(putrow, putcol)
            self.tilelib[hash(putrow,putcol)].addPeice(self.selected)
            self.selected.draw(self.window)
            self.selected = None
            move = True
    def compTurn2(self, depth):
        state = State(self)
        if not state.isgameover()[0]: 
            result = state.minmax(state,0, depth, "human")
            #print(str(result[0]), str(result[1]))
            self.selected = self.tilelib[hash(result[1][0][0],result[1][0][1])].getPeice()
            self.selected.undraw()
            self.tilelib[hash(result[1][1][0],result[1][1][1])].addPeice(self.selected)
            self.selected.draw(self.window)
            self.selected = None
    def compTurn3(self, depth):
        state = State(self)
        if not state.isgameover()[0]: 
            result = state.minmax(state,0, depth, "comp")
            #print(str(result[0]), str(result[1]))
            self.selected = self.tilelib[hash(result[1][0][0],result[1][0][1])].getPeice()
            self.selected.undraw()
            self.tilelib[hash(result[1][1][0],result[1][1][1])].addPeice(self.selected)
            self.selected.draw(self.window)
            self.selected = None

class State:
    def __init__(self, game=None, tilemap = {}, human=[[]], comp=[[]]):
        self.next=[]
        if not (game==None):
            self.tilemap=game.tilelib
            self.comp=[game.tilelib[hash(5,i)].peices for i in range (0,3)]
            self.human=[game.tilelib[hash(4,i)].peices for i in range (0,3)]
        else:
            self.tilemap=tilemap
            self.human=human
            self.comp=comp
        self.moves={}
        self.movelookup={}
        self.parent=None
        self.nextbest=None
        self.nextbestmove=None
        self.movefrom=None
    def print(self):
        toprint=[]
        for i in range(0,4):
            toprint.append([])
            for j in range(0,4):
                if(self.tilemap[hash(i,j)].peices==[]):
                    toprint[i].append("N:0")
                elif(self.tilemap[hash(i,j)].peices[0].color == "blue"):
                    toprint[i].append(str("B:" + str(self.tilemap[hash(i,j)].peices[0].size.value)))
                elif(self.tilemap[hash(i,j)].peices[0].color == "orange"):
                    toprint[i].append(str("O:" + str(self.tilemap[hash(i,j)].peices[0].size.value)))   
        for k in range(0,4):
            print(str(toprint[k])+"\n")
        hprint=[]
        cprint=[]
        for m in range(0,3):
            if(self.human[m]==[]):
                hprint.append("N:O")
            elif(self.human[m][0].color == "blue"):
                hprint.append(str("B:" + str(self.human[m][0].size.value)))
            if(self.comp[m]==[]):
                cprint.append("N:O")
            elif(self.comp[m][0].color == "orange"):
                cprint.append(str("O:" + str(self.comp[m][0].size.value)))
        print("Human: "+str(hprint))
        print("Comp: "+str(cprint))
    def findNext(self, turn):
        canmove=[]
        if (turn == "comp"):
            for i in range(0,3):
                #print( "he")
                if not(self.tilemap[hash(5,i)].peices==[]):
                    #print("re")
                    if(self.tilemap[hash(5,i)].peices[0].color=="orange"):
                        canmove.append([5,i])
            for j in range(0,4):
                for k in range(0,4):
                    if not(self.tilemap[hash(j,k)].peices==[]):
                        if(self.tilemap[hash(j,k)].peices[0].color=="orange"):
                            canmove.append([j,k])
            #print(str(canmove))
            for item in canmove:
                for m in range(0,4):
                    for n in range(0,4):
                        if(self.tilemap[hash(m,n)].peices==[]) or (self.tilemap[hash(m,n)].peices[0].size.value<self.tilemap[hash(item[0],item[1])].peices[0].size.value):
                            temp=State(None,mapcopy(self.tilemap),twodcopy(self.human),twodcopy(self.comp))
                            #print(temp.tilemap[hash(item[0],item[1])].peices)
                            peice = temp.tilemap[hash(item[0],item[1])].getPeice()
                            if item[0]==4:
                                temp.human[item[1]].pop(0)
                            if item[0]==5:
                                temp.comp[item[1]].pop(0)                                                       
                            #print(temp.tilemap[hash(item[0],item[1])].peices)
                            temp.tilemap[hash(m,n)].addPeice(peice)
                            self.moves[hash(hash(item[0],item[1]), hash(m,n))]=temp
                            self.movelookup[hash(hash(item[0],item[1]),hash(m,n))]=[[item[0],item[1]],[m,n]]
                            self.next.append(temp)
                            temp.movefrom=[[item[0],item[1]],[m,n]]
                        """elif(self.tilemap[hash(m,n)].peices[0].size.value<self.tilemap[hash(item[0],item[1])].peices[0].size.value):
                           temp=State(None,mapcopy(self.tilemap),twodcopy(self.human),twodcopy(self.comp))
                           #print(temp.tilemap[hash(item[0],item[1])].peices)
                           peice = temp.tilemap[hash(item[0],item[1])].getPeice()
                           if item[0]==4:
                                temp.human[item[1]].pop(0)
                           if item[0]==5:
                                temp.comp[item[1]].pop(0)                                                       
                           #print(temp.tilemap[hash(item[0],item[1])].peices)
                           temp.tilemap[hash(m,n)].addPeice(peice)
                           self.moves[hash(hash(item[0],item[1]), hash(m,n))]=temp
                           self.movelookup[hash(hash(item[0],item[1]), hash(m,n))]=[[item[0],item[1]],[m,n]]
                           self.next.append(temp)"""
        if (turn == "human"):
            for i in range(0,3):
                if not(self.tilemap[hash(4,i)].peices==[]):
                    canmove.append([4,i])
            for j in range(0,4):
                for k in range(0,4):
                    if not(self.tilemap[hash(j,k)].peices==[]):
                        if(self.tilemap[hash(j,k)].peices[0].color=="blue"):
                            canmove.append([j,k])
            for item in canmove:
                for m in range(0,4):
                    for n in range(0,4):
                        if(self.tilemap[hash(m,n)].peices==[] or self.tilemap[hash(m,n)].peices[0].size.value<self.tilemap[hash(item[0],item[1])].peices[0].size.value):
                            temp=State(None,mapcopy(self.tilemap),twodcopy(self.human),twodcopy(self.comp))
                            #print(temp.tilemap[hash(item[0],item[1])].peices)
                            peice = temp.tilemap[hash(item[0],item[1])].getPeice()
                            if item[0]==4:
                                temp.human[item[1]].pop(0)
                            if item[0]==5:
                                temp.comp[item[1]].pop(0)                                                       
                            #print(temp.tilemap[hash(item[0],item[1])].peices)
                            temp.tilemap[hash(m,n)].addPeice(peice)
                            self.moves[hash(hash(item[0],item[1]), hash(m,n))]=temp
                            self.movelookup[hash(hash(item[0],item[1]), hash(m,n))]=[[item[0],item[1]],[m,n]]
                            self.next.append(temp)
                            temp.movefrom=[[item[0],item[1]],[m,n]]
                        """elif(self.tilemap[hash(m,n)].peices[0].size.value<self.tilemap[hash(item[0],item[1])].peices[0].size.value):
                           temp=State(None,mapcopy(self.tilemap),twodcopy(self.human),twodcopy(self.comp))
                           #print(temp.tilemap[hash(item[0],item[1])].peices)
                           peice = temp.tilemap[hash(item[0],item[1])].getPeice()
                           if item[0]==4:
                                temp.human[item[1]].pop(0)
                           if item[0]==5:
                                temp.comp[item[1]].pop(0)                                                       
                           #print(temp.tilemap[hash(item[0],item[1])].peices)
                           self.moves[hash(hash(i,j), hash(m,n))]=temp
                           self.movelookup[hash(hash(i,j), hash(m,n))]=[[i,j],[m,n]]
                           temp.tilemap[hash(m,n)].addPeice(peice)
                           self.next.append(temp)"""
        #print(str(self.movelookup))
    def score(self):
        score=0
        inarow=0
        diagonal1=0
        diagonal2=0
        jinarow=[]
        cpeice=0
        hpeice=0
        for i in range(0,4):
            inarow=0
            for j in range(0,4):
                jinarow.append(0)
                if not self.tilemap[hash(i,j)].peices==[]:
                    if(self.tilemap[hash(i,j)].peices[0].color == "blue"):
                        hpeice+=1
                        score+=(self.tilemap[hash(i,j)].peices[0].size.value)
                        inarow+=1
                        jinarow[j]+=1
                        if(i==j):
                            diagonal1+=1
                        if(j==3-i):
                            diagonal2+=1
                    elif(self.tilemap[hash(i,j)].peices[0].color == "orange"):
                        cpeice-=1
                        score-=(self.tilemap[hash(i,j)].peices[0].size.value)
                        inarow-=1
                        if(i==j):
                            diagonal1-=1
                        if(j==3-i):
                            diagonal2-=1
                        jinarow[j]-=1
            score+=inarow
        score+=diagonal1 + diagonal2
        return score
    def isgameover(self):
        """inarow=0
        diagonal1=0
        diagonal2=0
        jinarow=[]
        for i in range(0,4):
            inarow=0
            for j in range(0,4):
                jinarow.append(0)
                print("here")
                if not self.tilemap[hash(i,j)].peices==[]:
                    if(self.tilemap[hash(i,j)].peices[0].color == "blue"):
                        inarow+=1
                        jinarow[j]+=1
                        if(i==j):
                            diagonal1+=1
                        if (i==3-j):
                            diagonal2+=1
                    elif(self.tilemap[hash(i,j)].peices[0].color == "orange"):
                        inarow-=1
                        if(i==j):
                            diagonal1-=1
                        if (i==3-j):
                            diagonal2-=1
                        jinarow[j]-=1
            if inarow == 4:
                 return True,"human wins"
            elif inarow==-4:
                 return True, "comp wins"
            else:
                 return False, None"""
        for row in range(0,4):
            bcount=0
            ocount=0
            for column in range(0,4):
                if(self.tilemap[hash(row,column)].peices != [] and self.tilemap[hash(row,column)].peices[0].color == "blue"):
                     bcount+=1
                if(self.tilemap[hash(row,column)].peices != [] and self.tilemap[hash(row,column)].peices[0].color == "orange"):
                     bcount+=1
            if bcount == 4:
                return True,"human wins"
            elif ocount == 4:
                return True,"comp wins"
        for col in range(0,4):
            bcount=0
            ocount=0
            for r in range(0,4):
                if(self.tilemap[hash(r,col)].peices != [] and self.tilemap[hash(r,col)].peices[0].color == "blue"):
                     bcount+=1
                if(self.tilemap[hash(r,col)].peices != [] and self.tilemap[hash(r,col)].peices[0].color == "orange"):
                     bcount+=1
            if bcount == 4:
                return True,"human wins"
            elif ocount == 4:
                return True,"comp wins"
        if (self.tilemap[hash(0,0)].peices != [] and 
           self.tilemap[hash(1,1)].peices != [] and 
           self.tilemap[hash(2,2)].peices != [] and 
           self.tilemap[hash(3,3)].peices != []):
                if(self.tilemap[hash(0,0)].peices[0].color ==
                   self.tilemap[hash(1,1)].peices[0].color ==
                   self.tilemap[hash(2,2)].peices[0].color == 
                   self.tilemap[hash(3,3)].peices[0].color):
                        if self.tilemap[hash(0,0)].peices[0].color =="blue":
                            return True,"human wins"
                        else:
                            return True,"comp wins"
        if (self.tilemap[hash(0,3)].peices != [] and 
           self.tilemap[hash(1,2)].peices != [] and 
           self.tilemap[hash(2,1)].peices != [] and 
           self.tilemap[hash(0,3)].peices != []):
                if(self.tilemap[hash(0,3)].peices[0].color ==
                   self.tilemap[hash(1,2)].peices[0].color ==
                   self.tilemap[hash(2,1)].peices[0].color == 
                   self.tilemap[hash(0,3)].peices[0].color):
                        if self.tilemap[hash(0,3)].peices[0].color =="orange":
                            return True,"comp wins"
                        else:
                            return True,"human wins"
        return False, None
        """print(diagonal1,diagonal2)
        for num in jinarow:
            print(num)
        if(diagonal1==4 or diagonal2==4 or (4 in jinarow)):
            return True,"human wins"
        elif(diagonal1==-4 or diagonal2==-4 or (-4 in jinarow)):
            return Trure, "comp wins"
        else:
            return False, None"""
    def minmax(self, state, depth, maxdepth, turn):
        """if((depth == maxdepth)):
            chosen_score = state.score()
        else:
            state.findNext(turn)
            moves = state.moves.keys()
            if moves == []:
              chosen_score = state.score()
            else:
              for move in moves:                
                 new_state = state.moves[move]
                 if turn=="comp":
                     best_score = math.inf
                     new_result = self.minmax(new_state, depth+1, maxdepth, nextmove("human"))
                 else:
                     new_result = self.minmax(new_state, depth+1, maxdepth, nextmove("comp"))
                 if turn=="comp":
                     compare="min"
                 else:
                     compare="max"
                 if (scorecomparitor(compare,new_result[0],best_score)):
                     best_score = new_result[0]
                     best_move = self.movelookup[move]
              return best_score, best_move"""
        states = []
        tree=[]
        states.append([state,state.score(),turn])
        tree.append([state])
        while(states != [] and depth<=maxdepth):
            turn = nextmove(turn)
            curr=states.pop(0)
            tree.append([])
            curr[0].findNext(turn)
            children=curr[0].next
            depth+=1
            best_score=None
            for child in children:
                states.insert(0,[child,child.score(),turn])
                tree[depth].append(child)
                child.parent=curr[0]
                if turn=="comp":
                    if (best_score==None) or (child.score()==scorecomparitor("min",child.score(),best_score)):
                        best_score=child.score()
                        best=child
                        curr[0].nextbest=best
                        curr[0].nextbestmove=best.movefrom
                else:
                    if (best_score==None) or (child.score()==scorecomparitor("max",child.score(),best_score)):
                        best_score=child.score()
                        best=child
                        curr[0].nextbest=best
                        curr[0].nextbestmove=best.movefrom
        while (best.parent!=None):
            best=best.parent
            #print(best.print())
        level = 0
        """for l in tree:
            print(str(level), "--------------------------------------------------------------------------------")
            for s in l:
                s.print()
                print(s.score())
            level+=1"""
        #best.nextbest.print()
        #print(str(best.nextbestmove))
        return best.nextbest, best.nextbestmove
    """def alphabeta(self,state,depth,turn):
        if (turn=="comp"):
            return"""
def gobby(players, level):
    gametime=True
    if(players=="rh"):
        while(gametime):
            curr = State(game)
            #curr.print()
            game.compTurn2(level)
            if(curr.isgameover()[0]):
                #print(curr.isgameover()[1])
                break
            game.humanTurn()
            if(curr.isgameover()[0]):
                #print(curr.isgameover()[1])
                break
    if(players=="hr"):
        while(gametime):
            curr = State(game)
            #curr.print()
            game.humanTurn()
            if(curr.isgameover()[0]):
                #print(curr.isgameover()[1])
                break
            game.compTurn2(level)
            if(curr.isgameover()[0]):
                #print(curr.isgameover()[1])
                break
    if (players=="rr"):
        while(gametime):
            curr = State(game)
            #curr.print()
            game.compTurn3(level)
            curr = State(game)
            if(curr.isgameover()[0]):
                #print(curr.isgameover()[1])
                break
            game.compTurn2(level)
            curr = State(game)
            #print(str(curr.isgameover()))
            if(curr.isgameover()[0]):
                #print(curr.isgameover()[1])
                break
gametype = (input("Who's playing(human and robot or robot and robot):"))
if(gametype=="human and robot"):
    choice=input("Who goes first?(human or robot)")
    if choice == "robot":
        fchoice="rh"
    else:
        fchoice="hr"
else:
    fchoice="rr"
diff = input("Difficulty(easy, medium, hard):")
if diff=="easy":
    dep=2
elif diff=="medium":
    dep=3
else:
    dep=4
gamewin = GraphWin("Gobblet Board",400,550)
brown = color_rgb(222,184,135)
gamewin.setBackground(brown)
game = Game(gamewin)
gobby(fchoice, dep)

