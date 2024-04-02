from bibli import *

X = None 
Y = None 
Z = None 
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
    "T1": [],
    "T2": ["T1"],
    "somme": ["T1", "T2"]
}


#get_Dependencies
tache="somme"
dependencies = get_Dependencies(task_system,tache)
print(dependencies)


#runSeq
runSeq(task_system)


#run
#run(task_system)

error_message(task_system,dependencies)