from bibli import *

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