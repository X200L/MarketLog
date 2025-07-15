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
ticks = int(input('Enter amount of simulation ticks: '))
maprix, start = maptxt.readtxtmap()
ozon = obj.opzone(start[0], start[1])
for i in range(0, len(maprix)):
    for j in range(0, len(maprix[i])):
        if maprix[i][j] == '2':
            s.append(obj.shelf(i,j))
print(len(s))
for i in range(0, amount):
    r.append(obj.robot(int(input('start x: ')), int(input('start y: ')), maprix))
    #maprix = r[i].init(maprix)
print(r)
for m in range(0, ticks):
    for i in range(0, amount):
        if not(r[i].path):
            if r[i].cords == start or m == 0:
                r[i].task = random.randint(0, len(s))
                r[i].path = agent.drawagentmap(s[r[i].task].cords, [], maprix, r[i].cords,)
                #r[i].path.append(str(s[r[i].task].cords[0])+':'+str(s[r[i].task].cords[1]))
                print('Robot '+str(i)+' finished, taking new task: '+str(s[r[i].task].cords))
                print(r[i].path)
            else:
                r[i].task = len(s)+1
                r[i].path = agent.drawagentmap(ozon.cords, [], maprix, r[i].cords,)
                #r[i].path.append(str(ozon.cords[0])+':'+str(ozon.cords[1]))
                print('Robot '+str(i)+' took shelf, returning to start zone')
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
        for i in range(0, amount):
            maprix = r[i].move(r[i].path[-1], maprix)
        for i in range(0, len(maprix)):
            a = ''
            for j in range(0, len(maprix[i])):
                a = a + " " + maprix[i][j]
            print(a)
            out.write(a+"\n")
        out.write("- "*33+"\n")
        print('- '*33)
    else:
        break