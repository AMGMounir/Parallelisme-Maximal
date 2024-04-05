import time
import threading
import networkx as nx
import matplotlib.pyplot as plt
import random


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
    
    def matriceDep(self):
        matrice_size = len(self.task_system)
        matrice = [[0 for _ in range(matrice_size)] for _ in range(matrice_size)]

        for i, task1 in enumerate(self.task_system):
            for j, task2 in enumerate(self.task_system):
                if i < j:
                    if set(task1.reads) & set(task2.writes) or set(task2.reads) & set(task1.writes) or set(task1.writes) & set(task2.writes):
                        matrice[i][j] = 1

        return matrice


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
            
            task.run()
            with print_lock:
                print(f"{task.name} a fini de s'éxecuter.")
            tache_exec.add(task)

        def execute_tache(task_list):
            for task in task_list:
                thread = threading.Thread(target=exec_tache, args=(task,))
                threads.append(thread)
                thread.start()

        while len(tache_exec) < len(self.task_system):
            tache_debute = []

            for task, dependencies in self.task_system.items():
                if task not in tache_exec and all(dep in tache_exec for dep in dependencies):
                    tache_debute.append(task)

            if tache_debute:
                execute_tache(tache_debute)
                
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


    def detTestRnd(self, num_executions=10):
        for _ in range(num_executions):
            M1 = random.randint(0, 100)
            M2 = random.randint(0, 100)
            M3 = random.randint(0, 100)
            M4 = random.randint(0, 100)
            M5 = random.randint(0, 100)
            self.run()


def paralellisme(task_system, matrice_dep):
    paraMax = task_system.copy()

    for task, dependencies in paraMax.items():
        dependencies.clear() 
        for i in range(len(task_system)):
            if matrice_dep[i][list(task_system.keys()).index(task)] == 1:
                dependencies.append(list(task_system.keys())[i])

    return paraMax


def redondance(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = redondance(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def draw(task_system):
    G = nx.DiGraph()

    for task in task_system.keys():
        G.add_node(task.name)

    for task, dependencies in task_system.items():
        for dependency in dependencies:
            G.add_edge(dependency.name, task.name)

    # Find all paths in the graph
    paths = {}
    for start in G.nodes():
        for end in G.nodes():
            if start != end:
                paths[(start, end)] = redondance(G, start, end)

    # Create a directed graph
    H = G.to_directed()

    pos = nx.spring_layout(H,seed=911811)
    # Draw edges
    for (start, end) in H.edges():
        path_count = len(paths[(start, end)])
        if path_count > 1:
            nx.draw_networkx_edges(H, pos, edgelist=[(start, end)], width=1, arrows=True, edge_color='black', style='dashed')
        else:
            nx.draw_networkx_edges(H, pos, edgelist=[(start, end)], width=1, arrows=True, edge_color='black')

    # Draw the graph
    nx.draw_networkx_nodes(H, pos, node_color='red', node_size=700)
    nx.draw_networkx_labels(H, pos, font_size=10, font_weight='bold')

    plt.title("Graph")
    plt.show()


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

def draw2(task_system):
    G = nx.DiGraph()

    for task in task_system.keys():
        G.add_node(task.name)


    for task, dependencies in task_system.items():
        for dependency in dependencies:
            G.add_edge(dependency.name, task.name)


    pos = nx.spring_layout(G,seed=9121837)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="red", font_size=10, font_weight="bold",style='dashed')
    plt.title("Graphe :")
    plt.show()