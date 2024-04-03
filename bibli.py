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
    executed_tasks = set()
    while len(executed_tasks) < len(task_system):
        for task, dependencies in task_system.items():
            if task not in executed_tasks and all(dep in executed_tasks for dep in dependencies):
                print("Executing task:", task.name)
                if task.run:
                    task.run()
                executed_tasks.add(task)
                time.sleep(1)
            elif task not in executed_tasks:
                print("Task", task.name, "has dependencies:", [dep.name for dep in dependencies])
                for dependency in dependencies:
                    print("Executing dependency:", dependency.name)
                    if dependency.run:
                        dependency.run()
                    executed_tasks.add(dependency)
                    time.sleep(1)
                if all(dep in executed_tasks for dep in dependencies):
                    print("Executing task:", task.name)
                    if task.run:
                        task.run()
                    executed_tasks.add(task)
                    time.sleep(1)
            else:
                continue


def errormessage(task_system):
    if len(task_system) != len(set(task_system)):
        print("duplicate found")
    else:
        print("duplicate not found")
    # Vérifier si toutes les tâches mentionnées dans le dictionnaire de précédence existent
