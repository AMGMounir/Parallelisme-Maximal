from bibli import *

X = 0
Y = 0 
Z = 0 
W = 0
A = 0
B = 0
C = 0
D = 0


def runT1():
    global X
    X = 1

def runT2():
    global Y
    Y = 2

def runT3():
    global Z
    Z = 3

def runT4():
    global W
    W = 3

def runT5():
    global A
    A = 3

def runT6():
    global B
    B = 3

def runT7():
    global C
    C = 3

def runT8():
    global D
    D = 3


t1 = Task(name="T1", run=runT1, writes=[X])
t2 = Task(name="T2", run=runT2, writes=[Y])
t3 = Task(name="t3", run=runT3, reads=["X", "Y"], writes=[Z])
t4 = Task(name="T4", run=runT4, writes=[W])
t5 = Task(name="T5", run=runT5, writes=[A])
t6 = Task(name="T6", run=runT6, reads=["W", "A"], writes=[B])
t7 = Task(name="T7", run=runT7, writes=[C])
t8 = Task(name="T8", run=runT8, writes=[D])

task_system = {
    Task("T1", run=runT1): [],
    Task("T3", run=runT3): [Task("T2")],
    Task("T2", run=runT2): [Task("T1")],
    Task("T5", run=runT5): [Task("T3"),Task("T4")],
    Task("T7", run=runT7): [Task("T5"), Task("T6")],
    Task("T8", run=runT8): [Task("T7")],
    Task("T6", run=runT6): [Task("T4")],
    Task("T4", run=runT4): [Task("T2")]
}

# Get dependencies for a specific task
tache = Task("T5", run=runT5)
dependencies = get_Dependencies(task_system, tache)
print("Les dependances de ", t5.name," sont : ",dependencies)


#runSeq
print("\nexecution sequentielle :\n")
runSeq(task_system)


#run
print("\nexecution parallele :\n")
run(task_system)

errormessage(task_system)