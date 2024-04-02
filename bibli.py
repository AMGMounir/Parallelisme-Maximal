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



def get_Dependencies(task_system,tache):
    dependencies = {}
    for task, dependency_list in task_system.items():
        if task==tache:
            dependencies[tache] = []
            for dependency in dependency_list:
                if dependency in task_system:
                    dependencies[tache].append(dependency)
    return dependencies


def runSeq(task_system):
    for Task in task_system:
        print("Exécution de la tâche:", Task)
        time.sleep(1)


def error_message(task_system, dependencies):
    # Vérifier si les noms de tâches sont uniques
        
        print("Erreur: Les noms des tâches ne sont pas uniques")
        return False
    
    # Vérifier si toutes les tâches mentionnées dans le dictionnaire de précédence existent
