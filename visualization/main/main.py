import usr_lib.graph_decoder as graph
import usr_lib.objects as obj
import random
#amount = int(input("Enter amount of robots:"))
c, obj.mapsize = graph.createmap()
s = graph.s
print(obj.mapsize)
a = []
for i in range(0,2):
    a.append(obj.robot(5,i,c))
    c = a[i].init(c)
    for i in range(0,len(c)):
        print(c[i])
        print("")
    print("-----------------------------------")
for j in range(0,10):
    for i in range(0,2):
        d = random.randint(0,3)
        c = a[i].move(d,c)
    for i in range(0,len(c)):
        print(c[i])
        print("")
    print("-----------------------------------")