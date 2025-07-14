import usr_lib.readmaptxt as maptxt
import usr_lib.objects as obj
import usr_lib.singleagentplanner as agent
import random
out = open('out.txt', 'w', encoding='utf-8')
s = []
r = []
collision = 0
pathmap = []
dist = 0
amount = 3
maprix = maptxt.readtxtmap()
for i in range(0, len(maprix)):
    for j in range(0, len(maprix[i])):
        if maprix[i][j] == '2':
            s.append(obj.shelf(i,j))
print(len(s))
for i in range(0, amount):
    r.append(obj.robot(int(input('start x: ')), int(input('start y: ')), maprix))
    #maprix = r[i].init(maprix)
print(r)
for i in range(0, amount):
    r[i].task = random.randint(0, len(s))
    print(s[r[i].task].cords)
    r[i].path = agent.drawagentmap(s[r[i].task].cords, [], maprix, r[i].cords,)
    print(r[i].path)
for i in range(0, amount):
    shortestpath = []
    for d in range(0, amount):
        if d!=i:
            if len(r[i].path)<len(r[d].path):
                shortestpath = r[i].path
            else:
                shortestpath = r[d].path
            for j in range(0,len(shortestpath)):
                if r[i].path[j]==r[d].path[j]:
                    collision = 1
                    colliders = [i,d]
                    crator = r[i].path[j]
                    print("collision detected at: "+crator+" beetween "+str(i)+" and "+str(d))
if collision == 0:
    for i in range(0, len(r)):
        for j in range(len(r[i].path)-2, -1, -1):
            maprix = r[i].move(r[i].path[j], maprix)
            r[i].path.pop(j)
            print(r[i].path[j])
            for b in range(0,len(maprix)):
                a = ''
                for d in range(0, len(maprix[b])):
                    a = a + " " + maprix[b][d]
                print(a)
                out.write(a+"\n")
            out.write("- "*33+"\n")