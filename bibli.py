import time
import threading
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


def errormessage(task_system):
    if len(task_system) != len(set(task_system)):
        print("duplicate found")
    else:
        print("duplicate not found")
    # Vérifier si toutes les tâches mentionnées dans le dictionnaire de précédence existent
