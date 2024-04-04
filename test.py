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

# Création des tâches
t1 = Task(name="T1", run=runT1, writes=[X])
t2 = Task(name="T2", run=runT2, writes=[Y])
t3 = Task(name="T3", run=runT3, reads=["X", "Y"], writes=[Z])
t4 = Task(name="T4", run=runT4, writes=[W])
t5 = Task(name="T5", run=runT5, writes=[A])
t6 = Task(name="T6", run=runT6, reads=["W", "A"], writes=[B])
t7 = Task(name="T7", run=runT7, writes=[C])
t8 = Task(name="T8", run=runT8, writes=[D])
t9 = Task(name="T8", run=runT8, writes=[D])

# Définition des dépendances entre les tâches
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

# Appel de la fonction draw avec le dictionnaire de tâches et leurs dépendances
#draw(task_system)
TaskSystem([t1, t2, t3, t4, t5, t6, t7, t8, t9], task_system)
