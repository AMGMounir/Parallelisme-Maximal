import time
import threading
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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
        self.start = 0
        self.end = 0


    def get_Dependencies(self, tache):
        dependencies = []
        for task, dependency_list in self.task_system.items():
            if task.name == tache.name:
                dependencies.extend(dependency_list)
        return [dependency.name for dependency in dependencies]
    
    def build_dependency_matrix(self):
        matrix_size = len(self.task_system)
        matrix = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]

        for i, task1 in enumerate(self.task_system):
            for j, task2 in enumerate(self.task_system):
                if i < j:
                    if set(task1.reads) & set(task2.writes) or set(task2.reads) & set(task1.writes) or set(task1.writes) & set(task2.writes):
                        matrix[i][j] = 1

        return matrix



    def runSeq(self):
        tache_exec = set()

        def exec_tache(task):
            if task.run:
                task.run()
                self.start = time.perf_counter()
            tache_exec.add(task.name)
            print(task.name, "a démarré.")
            self.end = time.perf_counter()
            print(task.name, "a fini de s'éxecuté.")

        while len(tache_exec) < len(self.task_system):
            for task, dependencies in self.task_system.items():
                if task.name not in tache_exec and all(dep.name in tache_exec for dep in dependencies):
                    exec_tache(task)

        print("Temps d'éxecution :", self.end - self.start)


    def run(self):
        tache_exec = set()
        threads = []
        print_lock = threading.Lock()

        def exec_tache(task):
            with print_lock:
                print(f"{task.name} a démarré.")
            if task.run:
                task.run()
            with print_lock:
                print(f"{task.name} a fini de s'éxecuter.")
            tache_exec.add(task)

        def execute_tasks(task_list):
            for task in task_list:
                thread = threading.Thread(target=exec_tache, args=(task,))
                threads.append(thread)
                thread.start()

        while len(tache_exec) < len(self.task_system):
            tasks_to_start = []

            for task, dependencies in self.task_system.items():
                if task not in tache_exec and all(dep in tache_exec for dep in dependencies):
                    tasks_to_start.append(task)

            if tasks_to_start:
                execute_tasks(tasks_to_start)
                
            for thread in threads:
                thread.join()

        print("temps d'execution", self.end - self.start)


    def parCost(self, nombrederun=3):
        t_runSeq=[]
        t_runPar=[]
        for i in range(nombrederun):
            tSeq=time.time()
            self.runSeq()
            t_runSeq.append(time.time() - tSeq)

            tPar=time.time()
            self.run()
            t_runPar.append(time.time() - tPar)
        moy_runSeq=sum(t_runSeq)/nombrederun
        moy_runPar=sum(t_runSeq)/nombrederun

        print(moy_runSeq)
        print(moy_runPar)


    def detTestRnd(self, nombrederun):
        test = []

        for i in range(nombrederun):
            self.tache_exec = set()
            self.run()
            test.append(self.tache_exec)

        deterministe = all(x == test[0] for x in test)

        if deterministe:
            print("Le graphe est determinié")
        else:
            print("Le graphe n'est pas determiné")

def update_task_system_from_matrix(task_system, dependency_matrix):
    new_task_system = task_system.copy()

    for task, dependencies in new_task_system.items():
        dependencies.clear()  # Clear existing dependencies
        for i in range(len(task_system)):
            if dependency_matrix[i][list(task_system.keys()).index(task)] == 1:
                dependencies.append(list(task_system.keys())[i])

    return new_task_system

    
def draw(task_system):
    G = nx.DiGraph()

    for task in task_system.keys():
        G.add_node(task.name)


    for task, dependencies in task_system.items():
        for dependency in dependencies:
            G.add_edge(dependency.name, task.name)

    for i, t1 in enumerate(task_system.keys()):
        for j, t2 in enumerate(task_system.keys()):
            if i >= j:
                continue
            if not set(t1.writes).intersection(t2.reads):
                continue
            if not set(t2.writes).intersection(t1.reads):
                continue
            if not set(t1.writes).intersection(t2.writes):
                G.add_edge(t1.name, t2.name)

    pos = nx.spring_layout(G,seed=27)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="red", font_size=10, font_weight="bold",style='dashed')
    plt.title("Graphe :")
    plt.show()


def domaines(task_system):
    for task, dependencies in task_system.items():
        reads = task.reads
        writes = task.writes
        print(f"Tache: {task.name}")
        print(f"Domaine de Lecture: {reads}")
        print(f"Domaine D'écriture: {writes}")
        print()

def create_schedule_matrix(task_system):
    task_list = list(task_system.keys())
    num_tasks = len(task_list)
    schedule_matrix = np.zeros((num_tasks, num_tasks), dtype=int)
    
    for i, task in enumerate(task_list):
        dependencies = task_system[task]
        for dep_task in dependencies:
            j = task_list.index(dep_task)
            schedule_matrix[i, j] = 1
    
    return schedule_matrix

def check_dependency(task1, task2):
    L1 = task1.reads
    E1 = task1.writes
    L2 = task2.reads
    E2 = task2.writes
    
    # Check if any intersection of read and write sets is non-empty
    if set(L1) & set(E2) or set(L2) & set(E1) or set(E1) & set(E2):
        return 1
    else:
        return 0
    







def error_message(task_system):
    # Vérifier si les noms de tâches sont uniques
    task_names = [t.name for t in task_system.keys()]
    if len(task_names) != len(set(task_names)):
        print("Erreur: Les noms des tâches ne sont pas uniques")
        return False
    
    # Vérifier si toutes les tâches mentionnées dans le dictionnaire de précédence existent
    allTask_names = set(task_names)
    for t, deps in task_system.items():
        if t.name not in allTask_names:  # Access the name attribute
            print(f"Erreur: La tâche {t.name} n'existe pas")  # Access the name attribute
            return False
        for dep in deps:
            if dep.name not in allTask_names:  # Access the name attribute
                print(f"Erreur: La tâche {dep.name} mentionnée comme dépendance de {t.name} est inexistante")  # Access the name attribute
                return False
    
    # Vérifier si le système de tâches est déterminé
    parcouru = set()
    for t in allTask_names:
        if t not in parcouru:
            deps = [dep.name for dep in task_system.get(t, [])]  # Access the name attribute
            parcouru.update(deps)
    if parcouru != allTask_names:
        print("Erreur: Le système de tâches est indéterminé")
        return False
    
    return True


