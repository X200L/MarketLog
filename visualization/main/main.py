import usr_lib.readmaptxt as maptxt
import usr_lib.objects as obj
import usr_lib.singleagentplanner as agent
import random
out = open('out.txt', 'w', encoding='utf-8')
s = []
r = []
agentspaths =[]
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
    shortestpath = []
    previousnodes = ['','']
    
    for i in range(0, amount):
        for b in range(0,amount):
            agentspaths.append(r[b].path)
        if not(r[i].path):
            if r[i].cords == start or m == 0:
                r[i].task = random.randint(0, len(s))
                r[i].path = agent.drawagentmap(s[r[i].task].cords, agentspaths, maprix, r[i].cords,i)
                r[i].path.insert(0, str(s[r[i].task].cords[0])+':'+str(s[r[i].task].cords[1]))
                #r[i].path.append(str(s[r[i].task].cords[0])+':'+str(s[r[i].task].cords[1]))
                print('Robot '+str(i)+' finished, taking new task: '+str(s[r[i].task].cords))
                print(r[i].path)
            else:
                r[i].task = len(s)
                r[i].path = agent.drawagentmap(ozon.cords, agentspaths, maprix, r[i].cords, i)
                r[i].path.insert(0, str(start[0])+':'+str(start[1]))
                #r[i].path.append(str(ozon.cords[0])+':'+str(ozon.cords[1]))
                print('Robot '+str(i)+' took shelf, returning to start zone')
                print(r[i].path)
            agentspaths = []
    for i in range(0, amount):
        for d in range(0, amount):
            if d!=i:
                if len(r[i].path)<len(r[d].path):
                    shortestpath = r[i].path
                else:
                    shortestpath = r[d].path
                for j in range(-1,-len(shortestpath), -1):
                    if r[i].path[-j]==r[d].path[-j]:
                        collision = 1
                        colliders = [i,d]
                        crator = [r[i].path[j]]
                        print("collision type 1 detected at node "+str(crator[0])+", between "+str(i)+" and "+str(d))
                    elif r[i].path[j]==previousnodes[1] and r[d].path==previousnodes[0]:
                        collision = 2
                        colliders = [i,d]
                        crator = [r[i].path[j], previousnodes[0]]
                        print('collision detected at ray '+str(crator[0])+'-'+str(crator[1]+' between '+str(i)+' and '+str(j)))
                    elif r[i].path[j]==previousnodes[1] or r[d].path==previousnodes[0]:
                        collision = 2
                        colliders = [i,d]
                        crator = [r[i].path[j], previousnodes[0]]
                        print('collision type 3 detected at node '+str(r[i].path[j])+' between '+str(i)+' and '+str(d))
                    previousnodes = [r[i].path[j], r[d].path[j]]
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
        print(m)
        break