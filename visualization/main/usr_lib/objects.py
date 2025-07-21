mapsize = [7,8]
barricades = ['1','2','R','a']
barricades2 = ['1', 'R', 'a']
class robot:
    
    def __init__ (self, x,y, curmap):
        self.cords = [x,y]
        self.below = curmap[self.cords[0]][self.cords[1]]
        #print(self.below)
        self.trycords = [self.cords[0], self.cords[1]]
        self.withshelf = False
        self.task = 0
        self.path = []
    def init (self, curmap):
        curmap[self.cords[0]][self.cords[1]] = 'R'
        return curmap
    def move(self, moveto, curmap, symbol):
        if ':' in moveto:
            self.cords = [self.trycords[0], self.trycords[1]]
            self.trycords[0] = int(moveto.split(':')[0])
            self.trycords[1] = int(moveto.split(':')[1])
            #if curmap[self.trycords[0]][self.trycords[1]] == '0':
            curmap[self.cords[0]][self.cords[1]] = self.below
            self.below = curmap[self.trycords[0]][self.trycords[1]]
            curmap[self.trycords[0]][self.trycords[1]] = symbol
        else:
            print('skipped')
        self.path.pop()
        return curmap



class shelf:
    def __init__(self, x, y):
        self.cords = [x,y] 
        self.state = 0
        #0 - на месте, 1 - присвоен в качестве задания, 2 - взят роботом, 3 - везется роботом на место
        #print('shelf created at:'+str(self.x)+' '+str(self.y))
    def returninplace(self, curmap, replacement):
        curmap[self.cords[0]][self.cords[1]] = replacement
        #print('test')
        return curmap
    
class opzone:
    def __init__(self, x, y):
        self.cords = [x,y]