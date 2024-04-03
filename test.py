from bibli import *

X = 0
Y = 0 
Z = 0 

def runT1():
    global X
    X = 1

def runT2():
    global Y
    Y = 2

def runTsomme():
    global X, Y, Z
    Z = X + Y

t1 = Task(name="T1", run=runT1, writes=[X])
t2 = Task(name="T2", run=runT2, writes=[Y])
tSomme = Task(name="somme", run=runTsomme, reads=["X", "Y"], writes=[Z])

task_system = {
    Task("T1", run=runT1): [],
    Task("somme", run=runTsomme): [Task("T1"), Task("T2")],
    Task("T2", run=runT2): [Task("T1")]
}

# Get dependencies for a specific task
tache = Task("somme", run=runTsomme)
dependencies = get_Dependencies(task_system, tache)
print(dependencies)


#runSeq
runSeq(task_system)


#run
#run(task_system)

errormessage(task_system)