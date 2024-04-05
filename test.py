from bibli import *

M1 = 0
M2 = 0 
M3 = 0 
M4 = 0
M5 = 0



def runT1():
    global M1, M2, M3
    M3 = M1+M2
    time.sleep(1)

def runT2():
    global M1, M4
    M4 = M1
    time.sleep(1)

def runT3():
    global M3, M4, M1
    M1 = M3+M4
    time.sleep(1)

def runT4():
    global M3, M4, M5
    M5 = M3+M4
    time.sleep(1)

def runT5():
    global M4, M2
    M2 = M4
    time.sleep(1)

def runT6():
    global M5
    M5=M5
    time.sleep(1)

def runT7():
    global M1, M2, M4
    M4 = M4+ M1 + M2
    time.sleep(1)

def runT8():
    global M1, M3, M5
    M5=M1+M3
    time.sleep(1)


M1 = "M1"
M2 = "M2"
M3 = "M3"
M4 = "M4"
M5 = "M5"


t1 = Task(name="T1", run=runT1, reads=[M1, M2], writes=[M3])
t2 = Task(name="T2", run=runT2, reads=[M1], writes=[M4])
t3 = Task(name="T3", run=runT3, reads=[M3, M4], writes=[M1])
t4 = Task(name="T4", run=runT4, reads=[M3, M4], writes=[M5])
t5 = Task(name="T5", run=runT5, reads=[M4], writes=[M2])
t6 = Task(name="T6", run=runT6, reads=[M5], writes=[M5])
t7 = Task(name="T7", run=runT7, reads=[M1, M2, M4], writes=[M4])
t8 = Task(name="T8", run=runT8, reads=[M1, M3], writes=[M5])


task_system = {
    t1: [],
    t2: [t1],
    t3: [t2],
    t4: [t2],
    t5: [t3, t4],
    t6: [t4],
    t7: [t5, t6],
    t8: [t7]
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
#s1.run()

#parCost
#s1.parCost(2)

#detTestRnd
#s1.detTestRnd(2)

#draw
#draw(task_system)

#domaines(task_system)

#Gestion d'erreurs
#error_message(task_system)
dependency_matrix = s1.build_dependency_matrix()
for row in dependency_matrix:
    print(row)

new_task_system = update_task_system_from_matrix(task_system, dependency_matrix)

# Print the updated task system
for task, dependencies in new_task_system.items():
    print(f"{task.name} depends on {[dep.name for dep in dependencies]}")
