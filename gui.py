import customtkinter
from bibli import *
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import time
from PIL import Image

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

M1 = "M1"
M2 = "M2"
M3 = "M3"
M4 = "M4"
M5 = "M5"


def runT1():
    global M1, M2, M3
    M3 = M1 + M2
    time.sleep(1)

def runT2():
    global M1, M4
    M4 = M1
    time.sleep(1)

def runT3():
    global M3, M4, M1
    M1 = M3 + M4
    time.sleep(1)

def runT4():
    global M3, M4, M5
    M5 = M3 + M4
    time.sleep(1)

def runT5():
    global M4, M2
    M2 = M4
    time.sleep(1)

def runT6():
    global M5
    M5 = M5
    time.sleep(1)

def runT7():
    global M1, M2, M4
    M4 = M4 + M1 + M2
    time.sleep(1)

def runT8():
    global M1, M3, M5
    M5 = M1 + M3
    time.sleep(1)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Parallélisme Maximal.py")
        self.geometry(f"{775}x{610}")
        self.resizable(False, False)


        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=9, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        image_path = "Logo.png"
        image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(200, 90))

        image_label=customtkinter.CTkLabel(self.sidebar_frame, image= image, text='')
        image_label.place(x=15, y=520)

        #reset
        self.reset_button = customtkinter.CTkButton(master=self, text="Reset", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.reset_all)
        self.reset_button.place(x=250, y=575)


        self.ParalellismeMax = customtkinter.CTkLabel(self.sidebar_frame, text="Parallélisme Maximal", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ParalellismeMax.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.Mounir = customtkinter.CTkButton(self.sidebar_frame, text="Mounir", state='disabled')
        self.Mounir.grid(row=1, column=0, padx=20, pady=10)
        self.Kaoutar = customtkinter.CTkButton(self.sidebar_frame, text="Kaoutar", state='disabled')
        self.Kaoutar.grid(row=2, column=0, padx=20, pady=10)
        self.Imane = customtkinter.CTkButton(self.sidebar_frame, text="Imane", state='disabled')
        self.Imane.grid(row=3, column=0, padx=20, pady=10)

        self.dep_button = customtkinter.CTkButton(master=self, text="Créer", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.get_dependencies)
        self.dep_button.grid(row=8, column=2, padx=(5, 5), pady=(10, 10), sticky="se")

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")
        self.tabview.add("Parallélisme Maximal")
        
        self.graph_canvas = customtkinter.CTkFrame(self, width=400, height=300)
        self.graph_canvas.grid(row=0, column=1, columnspan=2, padx=10, pady=(50, 0),sticky='nsew')
        self.graph_canvas.grid_remove()  
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.fig = None
        self.draw_graph({}, [])

        self.scrollable_frame_left = customtkinter.CTkScrollableFrame(self, label_text="Taches")
        self.scrollable_frame_left.grid(row=1, column=1, padx=(20, 5), pady=(20, 0), sticky="nsew")
        self.scrollable_frame_left.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_left.grid_rowconfigure(0, weight=1)  
        self.scrollable_frame_left_buttons = []
        self.task_dependencies = {} 
        self.task_button_colors = {} 

        self.task_system = [
            {"name": "T1", "reads": [M1, M2], "writes": [M3], "run": runT1},
            {"name": "T2", "reads": [M1], "writes": [M4], "run": runT2},
            {"name": "T3", "reads": [M3, M4], "writes": [M1], "run": runT3},
            {"name": "T4", "reads": [M3, M4], "writes": [M5], "run": runT4},
            {"name": "T5", "reads": [M4], "writes": [M2], "run": runT5},
            {"name": "T6", "reads": [M5], "writes": [M5], "run": runT6},
            {"name": "T7", "reads": [M1, M2, M4], "writes": [M4], "run": runT7},
            {"name": "T8", "reads": [M1, M3], "writes": [M5], "run": runT8}
        ]

        for i, task_data in enumerate(self.task_system):
            task_name = task_data["name"]
            checkbox_var = customtkinter.StringVar(value="0")  
            checkbox = customtkinter.CTkCheckBox(master=self.scrollable_frame_left, text=task_name, variable=checkbox_var)
            checkbox.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")
            checkbox.bind("<Button-1>", lambda event, t=task_name: self.handle_task_click(t))
            self.scrollable_frame_left_buttons.append(checkbox)
            self.task_button_colors[checkbox] = checkbox.cget("fg_color")

        self.scrollable_frame_right = customtkinter.CTkScrollableFrame(self, label_text="Dépendances")
        self.scrollable_frame_right.grid(row=1, column=2, padx=(20, 50), pady=(20, 0), sticky="nsew")
        self.scrollable_frame_right.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_right.grid_rowconfigure(0, weight=1) 
        self.scrollable_frame_right_switches = []

    def handle_task_click(self, task):
        self.clear_right_panel()
        self.show_dependencies(task)

        for button in self.scrollable_frame_left_buttons:
            if button.cget("text") != task and button.cget("fg_color") != "green":
                button.configure(fg_color=self.task_button_colors[button])
                
    def show_dependencies(self, task):
        if task not in self.task_dependencies:
            self.task_dependencies[task] = []
        dependencies = self.task_dependencies[task]
        task_index = next((i for i, t in enumerate(self.task_system) if t["name"] == task), None)
        if task_index is not None:
            for i, dep_task in enumerate(self.task_system):
                dependency = dep_task["name"]
                state = "on" if dependency in dependencies else "off"
                switch_var = customtkinter.StringVar(value=state)
                switch = customtkinter.CTkSwitch(master=self.scrollable_frame_right, text=dependency, variable=switch_var, onvalue="on", offvalue="off")
                switch.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")
                switch.bind("<Button-1>", lambda event, t=task, d=dependency, var=switch_var: self.toggle_dependency(t, d, var))
                self.scrollable_frame_right_switches.append(switch)
                
        for button in self.scrollable_frame_left_buttons:
            if button.cget("text") == task:
                button.configure(fg_color=("green") if dependencies else self.task_button_colors[button])

                
    def toggle_dependency(self, task, dependency, var):
        dependencies = self.task_dependencies.get(task, []) 
        if var.get() == "on":
            if dependency not in dependencies:
                dependencies.append(dependency)
        else:
            try:
                dependencies.remove(dependency)
            except ValueError:
                print(f"la tache '{dependency}' ne dépend pas de '{task}'.")
                return 

        for button in self.scrollable_frame_left_buttons:
            if button.cget("text") == task:
                if dependencies:
                    button.configure(fg_color="green")
                else:
                    button.configure(fg_color=self.task_button_colors[button])

        self.task_dependencies[task] = dependencies

    def clear_right_panel(self):
        for switch in self.scrollable_frame_right_switches:
            switch.destroy()
        self.scrollable_frame_right_switches = []

    def get_dependencies(self):
        task_dependencies_names = {}
        tasks_to_remove = []

        for checkbox in self.scrollable_frame_left_buttons:
            task_name = checkbox.cget("text")
            checkbox_variable = checkbox.cget("variable")
            if checkbox_variable.get() == "1":
                task_dependencies_names[task_name] = []

        for task in self.task_dependencies:
            if task not in task_dependencies_names:
                tasks_to_remove.append(task)

        for task in tasks_to_remove:
            del self.task_dependencies[task]

        sys = self.task_dependencies
        print("Systeme de tache :")
        print(sys)


        matrice_dep = self.matriceDep(sys)
        print("Matrice de dependances:")
        for row in matrice_dep:
            print(row)
        
        paraMax = self.paralellisme(sys, matrice_dep)
        print("Parallélisme Maximal :")
        print(paraMax)

        redundant_edges = self.redondance(paraMax)
        print("Redundant Edges:")
        print(redundant_edges)

        for widget in self.graph_canvas.winfo_children():
            widget.destroy()

        self.draw_graph(paraMax, redundant_edges)

        return sys
    

    def redondance(self, graph):
        redundant_edges = []
        visited = set()

        def dfs(node, target, path):
            if node == target:
                return [path]
            visited.add(node)
            paths = []
            for neighbor in graph[node]:
                if neighbor not in visited:
                    new_path = path + [(node, neighbor)]
                    paths.extend(dfs(neighbor, target, new_path))
            visited.remove(node)
            return paths

        for start, edges in graph.items():
            for end in edges:
                paths = dfs(start, end, [])
                if len(paths) > 1:
                    redundant_edges.append((start, end))

        return redundant_edges


    def matriceDep(self, sys):
        num_tasks = len(self.task_system)
        matrice = [[0] * num_tasks for _ in range(num_tasks)]

        for i, task1 in enumerate(self.task_system):
            for j, task2 in enumerate(self.task_system):
                if i < len(sys) and j < len(sys): 
                    if i < j:
                        if set(task1["reads"]) & set(task2["writes"]) or set(task2["reads"]) & set(task1["writes"]) or set(task1["writes"]) & set(task2["writes"]):
                            matrice[i][j] = 1
        return matrice

    def paralellisme(self, task_system, matrice_dep):
        paraMax = task_system.copy()

        for task, dependencies in paraMax.items():
            dependencies.clear() 
            for i in range(len(task_system)):
                if matrice_dep[i][list(task_system.keys()).index(task)] == 1:
                    dependencies.append(list(task_system.keys())[i])

        return paraMax


    def on_close(self): #erreur rencontré avec la graphe de nx qui n'arrive pas a se fermer en meme temps que le gui
        try:
            if self.fig:
                plt.close(self.fig)
        except Exception as e:
            print("Cloture de la fenetre du graphe:", e)

        plt.close('fin')

        self.destroy()


    def draw_graph(self, dependencies, redundant_edges):
        G = nx.DiGraph()
        for task, deps in dependencies.items():
            for dep in deps:
                G.add_edge(dep, task)

        pos = nx.spring_layout(G, seed=42) 

        self.fig, ax = plt.subplots(figsize=(3, 2)) 
        edges = G.edges()

        for u, v in edges:
            edge_style = "solid"
            edge_color = "black"
            if (v, u) in redundant_edges:
                edge_style = "dashed"
                edge_color = "red"
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=edge_color, style=edge_style, ax=ax)

        nx.draw_networkx_labels(G, pos, font_size=12, ax=ax)
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500, ax=ax)

        canvas = FigureCanvasTkAgg(self.fig, master=self.graph_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.graph_canvas)
        toolbar.update()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        self.graph_canvas.grid() 


    def reset_all(self): #permet de reset les taches et dependences input par l'utilisateur

        for checkbox in self.scrollable_frame_left_buttons:
            checkbox.deselect()

        for switch in self.scrollable_frame_right_switches:
            switch.cget("variable").set("off")

        self.task_dependencies.clear()

        for widget in self.graph_canvas.winfo_children():
            widget.destroy()

        self.draw_graph({}, [])



        
if __name__ == "__main__":
    app = App()
    app.mainloop()
