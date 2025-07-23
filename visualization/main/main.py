import usr_lib.readmaptxt as maptxt
import usr_lib.objects as obj
import usr_lib.singleagentplanner as agent
import random
def shit(ticks, q, path):
    out = open('out.txt', 'w', encoding='utf-8')
    log = open('log.txt', 'w', encoding='utf-8')
    s = []
    r = []
    agentspaths =[]
    collision = 0
    pathmap = []
    dist = 0
    maprix, start = maptxt.readtxtmap(path)
    startcords = agent.startcords(maprix)
    amount = len(startcords)-q
    ozon = obj.opzone(start[0], start[1])
    for i in range(0, len(maprix)):
        for j in range(0, len(maprix[i])):
            if maprix[i][j] == '2':
                s.append(obj.shelf(i,j))
    #print(len(s))
    for i in range(0, amount):
        r.append(obj.robot(startcords[i][0], startcords[i][1], maprix))
        #maprix = r[i].init(maprix)
    #print(r)
    for m in range(0, ticks):
        shortestpath = []
        previousnodes = ['','']
        for i in range(0, amount):
            if not(r[i].path):
                for b in range(0,amount):
                    agentspaths.append(r[b].path)
                if m == 0:
                    print(r[i].trycords)
                    o = 1
                    while o:
                        r[i].task = random.randint(0, len(s)-1)
                        if s[r[i].task].state==0:
                            o = 0
                    s[r[i].task].state = 1
                    r[i].path = agent.drawagentmap(s[r[i].task].cords, agentspaths, maprix, r[i].trycords,i)
                    if not(r[i].path):
                        return 'error'
                    log.write(str(s[r[i].task].cords)+str(agentspaths)+str(r[i].trycords)+str(i)+'\n')
                    r[i].path.insert(0, str(s[r[i].task].cords[0])+':'+str(s[r[i].task].cords[1]))
                    maprix = s[r[i].task].returninplace(maprix, '2')
                    #r[i].path.append(str(s[r[i].task].cords[0])+':'+str(s[r[i].task].cords[1]))
                    #print(i)
                    print('Robot '+str(i)+' started, assigning new task: '+str(s[r[i].task].cords))
                    print(r[i].path)
                    #log.write(str(m)+'\n')
                    log.write('Robot '+str(i)+' started, assigning new task: '+str(s[r[i].task].cords)+"\n")
                    log.write(str(r[i].path)+"\n")
                else:
                    if r[i].trycords==s[r[i].task].cords and s[r[i].task].state == 1:
                        s[r[i].task].state = 2
                        r[i].path = agent.drawagentmap(ozon.cords, agentspaths, maprix, r[i].trycords, i)
                        print(r[i].path)
                        if not(r[i].path):
                            return 'error'
                        log.write(str(ozon.cords)+str(agentspaths)+str(r[i].trycords)+str(i))
                        r[i].path.insert(0, str(start[0])+':'+str(start[1]))
                        maprix = s[r[i].task].returninplace(maprix, '0')
                        r[i].below = '0'
                        maprix[start[0]][start[1]] = '%'
                        #r[i].path.append(str(ozon.cords[0])+':'+str(ozon.cords[1]))
                        print('Robot '+str(i)+' took shelf, returning to ozon')
                        log.write(str(m)+'\n')
                        log.write('Robot '+str(i)+' took shelf, returning to ozon'+"\n")
                        log.write(str(r[i].path)+"\n")
                        print(r[i].path)
                    elif r[i].trycords==s[r[i].task].cords and s[r[i].task].state == 3:
                        print(r[i].trycords)
                        s[r[i].task].state = 0
                        maprix = s[r[i].task].returninplace(maprix, '2')
                        r[i].below = '2'
                        for k in range(0, len(maprix)):
                            a = ''
                            for j in range(0, len(maprix[k])):
                                a = a + " " + maprix[k][j]
                            #print(a)
                        o = 1
                        while o:
                            r[i].task = random.randint(0, len(s)-1)
                            if s[r[i].task].state==0:
                                o = 0
                            else:
                                print('error')
                                log.write('error')
                        s[r[i].task].state = 1
                        r[i].path = agent.drawagentmap(s[r[i].task].cords, agentspaths, maprix, r[i].trycords,i)
                        if not(r[i].path):
                            return 'error'
                        log.write(str(s[r[i].task].cords)+str(agentspaths)+str(r[i].trycords)+str(i)+'\n')
                        r[i].path.insert(0, str(s[r[i].task].cords[0])+':'+str(s[r[i].task].cords[1]))
                        maprix = s[r[i].task].returninplace(maprix, '2')
                        #r[i].path.append(str(s[r[i].task].cords[0])+':'+str(s[r[i].task].cords[1]))
                        #print(i)
                        print('Robot '+str(i)+' finished, assigning new task: '+str(s[r[i].task].cords))
                        print(r[i].path)
                        #log.write(str(m)+'\n')
                        log.write('Robot '+str(i)+' finished, assigning new task: '+str(s[r[i].task].cords)+"\n")
                        log.write(str(r[i].path)+"\n")
                    elif r[i].trycords == start:
                        s[r[i].task].state = 3
                        r[i].path = agent.drawagentmap(s[r[i].task].cords, agentspaths, maprix, r[i].trycords,i)
                        if not(r[i].path):
                            return 'error'
                        log.write(str(s[r[i].task].cords)+str(agentspaths)+str(r[i].trycords)+str(i)+'\n')
                        r[i].path.insert(0, str(s[r[i].task].cords[0])+':'+str(s[r[i].task].cords[1]))
                        #r[i].path.append(str(s[r[i].task].cords[0])+':'+str(s[r[i].task].cords[1]))
                        #print(i)
                        print('Robot '+str(i)+' took shelf to ozon, returning it in place: '+str(s[r[i].task].cords))
                        print(r[i].path)
                        log.write(str(m)+'\n')
                        log.write('Robot '+str(i)+' took shelf to ozon, returning it in place: '+str(s[r[i].task].cords)+"\n")
                        log.write(str(r[i].path)+"\n")
                    else:
                        print('error at '+str(r[i].trycords[0])+':'+str(r[i].trycords[1]))
                        #print(s[r[i].task].cords)
                agentspaths = []
        for i in range(0, amount):
            """for d in range(0, amount):
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
                        previousnodes = [r[i].path[j], r[d].path[j]]"""
        if collision == 0:
            print(amount)
            for i in range(0, amount):
                if s[r[i].task].state == 2 or s[r[i].task].state == 3:
                    maprix = r[i].move(r[i].path[-1], maprix, 'S')
                    #print(r[i].trycords)
                    #print(s[r[i].task].state)
                    #print(r[i].task)
                    if r[i].below == 'S' or r[i].below == 'R':
                        if r[i].trycords == start:
                            r[i].below = '%'
                        else:
                            r[i].below = '0'
                else:
                    maprix = r[i].move(r[i].path[-1], maprix, 'R')
                    #print(r[i].cords)
                    #print(s[r[i].task].state)
                    #print(r[i].task)
                    if r[i].below == 'S' or r[i].below == 'R':
                        if r[i].trycords == start:
                            r[i].below = '%'
                        else:
                            r[i].below = '0'
            for i in range(0, len(maprix)):
                a = ''
                for j in range(0, len(maprix[i])):
                    a = a + " " + maprix[i][j]
                #print(a)
                out.write(a+"\n")
            out.write("- "*33+"\n")
            print('- '*33)
        else:
            print(m)
            break
    return 'success'
u = 'error'
q = 0
while u == 'error':
    u = shit(10,q, "../main/usr_lib/map.txt")
    q+=1
