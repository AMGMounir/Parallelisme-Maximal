import time
import threading

class Task:
    def __init__(self, name="", reads=None, writes=None, run=None):
        self.name = name
        self.reads = reads or []
        self.writes = writes or []
        self.run = run

class TaskSystem:
    def __init__(self, ListeTaches=[Task], dict={}):
        self.ListeTaches = ListeTaches
        self.dict = dict

def get_dependencies(task_system):
    # Initialisation du dictionnaire qui va stocker les dépendances de chaque tâche
    dependencies = {}
    
    # Parcours de chaque tâche dans le système de tâches
    for task, dependency_list in task_system.items():
        # Initialisation de la liste des dépendances pour chaque tâche
        dependencies[task] = []
        
        # Parcours de chaque dépendance de la tâche actuelle
        for dependency in dependency_list:
            # Vérification si la dépendance est une tâche existante
            if dependency in task_system:
                # Ajout de la dépendance à la liste des dépendances de la tâche actuelle
                dependencies[task].append(dependency)
    
    # Retourner le dictionnaire des dépendances
    return dependencies

# Exemple d'utilisation
task_system = {
    "T1": [],
    "T2": ["T1"],
    "somme": ["T1", "T2"]
}

# Appel de la fonction pour obtenir les dépendances
dependencies = get_dependencies(task_system)

# Affichage du résultat
print(dependencies)

# Récuperer les noms des Tâches
def getTask(self, nomTache):
    for tache in self.lTask:
        if nomTache == tache.name:
            return tache  
