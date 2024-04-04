import time
import threading
import networkx as nx
import matplotlib.pyplot as plt

class Task:
    def __init__(self, name="", reads=None, writes=None, run=None):
        self.name = name
        self.reads = reads or []
        self.writes = writes or []
        self.run = run

class TaskSystem:
    def __init__(self, task_system=[], dependencies={}):
        self.task_system = task_system or []
        self.dependencies = dependencies or {}
        Verification(self.task_system, self.dependencies)


def get_Dependencies(task_system, tache):
    dependencies = []
    for task, dependency_list in task_system.items():
        if task.name == tache.name:
            dependencies.extend(dependency_list)
    return [dependency.name for dependency in dependencies]
    

def runSeq(task_system):
    tache_exec = set()
    def exec_tache(task):
        if task.run:
            task.run()
            global start 
            start = time.perf_counter()
        tache_exec.add(task.name)
        print("La tache ", task.name,"vient d'etre executé.")
        time.sleep(1)
        global end
        end = time.perf_counter()

    while len(tache_exec) < len(task_system):
        for task, dependencies in task_system.items():
            if task.name not in tache_exec and all(dep.name in tache_exec for dep in dependencies):
                if dependencies:
                    print("La tache ", task.name, "est dependante de:", get_Dependencies(task_system, task))
                exec_tache(task)
    print ("temps d'execution", end-start)



def run(task_system):
    tache_exec = set()
    threads = []

    def exec_tache(task):
        if task.run:
            task.run()
        tache_exec.add(task.name)

    while len(tache_exec) < len(task_system):
        for task, dependencies in task_system.items():
            if task.name not in tache_exec and all(dep.name in tache_exec for dep in dependencies):
                if dependencies:
                    time.sleep(1)
                    print("La tache", task.name, "est dépendante de:", ", ".join(get_Dependencies(task_system, task)))
                thread = threading.Thread(target=exec_tache, args=(task,))
                threads.append(thread)
                thread.start()
                start = time.perf_counter()
                print("La tache", task.name, "vient d'etre executée.")
    for thread in threads:
        thread.join()
        end = time.perf_counter()
    print ("temps d'execution", end-start)
    
def Verification(task_system, dependencies):
    # Verification des noms de taches dupliqués
    task_names = [task.name for task in task_system]
    if len(task_names) != len(set(task_names)):
        raise ValueError("Erreur : Des noms de taches sont dupliques.")
    
    # Verification des taches inexistantes dans les dependances
    all_task_names = set(task.name for task in task_system)
    for task, dependency_list in dependencies.items():
        if task.name not in all_task_names:
            raise ValueError(f"Erreur : Tâche inexistante dans le système de tâches : {task}.")
        print(dependency_list)
        for dependency in dependency_list:
            if dependency.name not in all_task_names:
                raise ValueError(f"Erreur : Tâche inexistante dans les dépendances de la tâche {task} : {dependency}.")
    
    # Vérification de la cohérence des dépendances
    for task, dependency_list in dependencies.items():
        for dependency in dependency_list:
            if task == dependency:
                raise ValueError(f"Erreur : La tâche {task} ne peut pas dépendre d'elle-même.")
            if task in dependencies[dependency]:
                raise ValueError(f"Erreur : Il y a une boucle de dépendance entre {task} et {dependency}.")
    
    return True
def draw(task_system):
    G = nx.DiGraph()
    
    for task, dependency_list in task_system.items():
        for dependency in dependency_list:
            G.add_edge(dependency, task)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()
def errormessage(task_system):
    if len(task_system) != len(set(task_system)):
        print("duplicate found")
    else:
        print("duplicate not found")
    # Vérifier si toutes les tâches mentionnées dans le dictionnaire de précédence existent
