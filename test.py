from bibli import *



M1 = 5
M2 = 28
M3 = 301
M4 = 10
M5 = 0

def runT1():
    global M1, M4
    M1 = M4 /2
    time.sleep(1)

def runT2():
    global M1, M3, M4
    M1 = M3 - M4
    time.sleep(1)

def runT3():
    global M3, M4, M5
    M5 = M3 * M4
    time.sleep(1)

def runT4():
    global M2, M4, M5
    M2 = M4 + 5
    time.sleep(1)

def runT5():
    global M5
    M5 = M5 * 5
    time.sleep(1)

def runT6():
    global M5
    M4 = M1*M2 / 3
    time.sleep(1)


t1 = Task(name="T1", run=runT1, reads=[M1], writes=[M4])
t2 = Task(name="T2", run=runT2, reads=[M3, M4], writes=[M1])
t3 = Task(name="T3", run=runT3, reads=[M3, M4], writes=[M5])
t4 = Task(name="T4", run=runT4, reads=[M4], writes=[M2])
t5 = Task(name="T5", run=runT5, reads=[M5], writes=[M5])
t6 = Task(name="T6", run=runT6, reads=[M1,M2], writes=[M4])


task_system = {
    t1: [],
    t2: [t1],
    t3: [t1], 
    t4: [t2,t3],
    t5: [t3],
    t6: [t4,t5]  
}


s1=TaskSystem(task_system)

tache = Task("T5", run=runT5)
dependencies = s1.get_Dependencies(tache)
print("Les dependances de ", t5.name," sont : ",dependencies)


#runSeq
print("\nexecution sequentielle :\n")
#s1.runSeq()


#run
print("\nexecution parallele :\n")
s1.run()

#parCost
#s1.parCost(2)

#check si y a une exception à été rencontré
error_message(task_system)

#draw systeme de base
draw(task_system)

#detTestRnd
#s1.detTestRnd()    

#matrice de dep affichage
matrice_dep = s1.matriceDep()
for row in matrice_dep:
    print(row)

paraMax = paralellisme(task_system, matrice_dep)

# Print le nouveau systeme de tache en para maximal
for task, dependencies in paraMax.items():
    print(f"{task.name} depends on {[dep.name for dep in dependencies]}")

paraMax = paralellisme(task_system, matrice_dep)
#draw
draw(paraMax)
#draw2(task_system)
#draw2(paraMax)

#Gestion d'erreurs
error_message(paraMax)
