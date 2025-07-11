mapsize = [7,8]
barricades = ['#','@','$','R','a']
barricades2 = ['#', 'R', 'a']
class robot:
    
    def __init__ (self, x,y, curmap):
        self.y = y
        self.x = x
        self.below = curmap[self.y][self.x]
        self.tryx = self.x
        self.tryy = self.y
        self.withshelf = False
    def init (self, curmap):
        curmap[self.y][self.x] = 'R'
        return curmap
    def settask(self, shelfID):
        self.task = shelfID
    def move(self, side, curmap):
        self.pastbelow = self.below
        self.pastx = self.x
        self.pasty = self.y
        if side == 0:
            self.tryy = self.y - 1
            self.tryx = self.x
        elif side == 1:
            self.tryx = self.x + 1
            self.tryy = self.y
        elif side == 2:
            self.tryy = self.y + 1
            self.tryx = self.x
        elif side == 3:
            self.tryx = self.x - 1
            self.tryy = self.y
        print('trying to move to:'+ str(self.tryx), str(self.tryy))
        if self.tryx >= 0 and self.tryy >= 0 and self.tryx < mapsize[0] and self.tryy < mapsize[1]:
            if self.withshelf == False and not(curmap[self.tryy][self.tryx] in barricades2):
                self.x = self.tryx
                self.y = self.tryy
                print('robot cords:'+ str(self.x) + str(self.y))
                curmap[self.pasty][self.pastx] = self.pastbelow
                self.below = curmap[self.y][self.x]
                curmap[self.y][self.x] = 'R'
                return curmap
            elif self.withshelf == True and not(curmap[self.tryy][self.tryx] in barricades):
                self.x = self.tryx
                self.y = self.tryy
                print('robot cords:'+ str(self.x) + str(self.y))
                curmap[self.pasty][self.pastx] = self.pastbelow
                self.below = curmap[self.y][self.x]
                curmap[self.y][self.x] = 'a'
                return curmap
            else:
                return curmap
        else:
            return curmap



class shelf:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        print('shelf created at:'+str(self.x)+' '+str(self.y))
    pass